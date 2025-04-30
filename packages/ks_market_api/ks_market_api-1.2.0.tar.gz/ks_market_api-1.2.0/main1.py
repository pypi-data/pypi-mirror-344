# todo!!! 处理unsubscribe,以及重复subscri
import ray
import setproctitle
import numpy as np
import talib
from ks_trade_api.constant import Adjustment, RET_OK, SUBSCRIBE_TYPE2INTERVAL, RET_ERROR, IndicatorColumn
from ks_trade_api.object import MyBookData, BarData, IndicatorData
from ks_futu_market_api import KsFutuMarketApi
from ks_trade_api.constant import SubscribeType, Interval, Indicator, Timing
from config import GATEWAY_CONFIG
import threading
from datetime import datetime
import time
import json
import pdb
from ks_utility.zmqs import ZmqPublisher, ZmqSubscriber
from ks_utility.logs import LoggerBase
from logger import Logger
import multiprocessing
import os
import sys

PARAMS2ENUM: dict = {
    'types': SubscribeType,
    'indicators': Indicator
}


# 定义布林带计算 Actor
@ray.remote
class BollingerCalculator:
    def __init__(self):
        self.interval_closes_map = {} # 存放各个周期的收盘价
        self.interval_datetimes_map = {} # 存放各个周期的结束时间

    def update_closes(self, interval: Interval, closes: {list[float]}, datetimes: list[datetime]):
        self.interval_closes_map[interval] = closes
        self.interval_datetimes_map[interval] = datetimes

    # todo!!! 一开始历史的bar不会推送，要一开始推送一次
    def add_data(self, bar: BarData):
        # 新bar开始，新增bar
        interval = bar.interval
        if not self.interval_datetimes_map.get(interval):
            return
        
        history_updated = False
        # print(self.interval_datetimes_map[interval][-1], bar.datetime)
        if self.interval_datetimes_map[interval][-1] < bar.datetime:
            print(f'[{bar.vt_symbol},{bar.interval}]history_updated!!!!!!!!!!!!!!@{self.interval_datetimes_map[interval][-1]}')
            self.interval_closes_map[interval].append(float(bar.close))
            self.interval_datetimes_map[interval].append(bar.datetime)

            # 需要存21个数据，因为要计算历史的数据
            self.interval_closes_map[interval] = self.interval_closes_map[interval][-21:]
            self.interval_datetimes_map[interval] = self.interval_datetimes_map[interval][-21:]
            history_updated = True
        # 更新实时bar
        else:
            self.interval_closes_map[interval][len(self.interval_closes_map[interval])-1] = float(bar.close)
        
        close_prices = np.array(self.interval_closes_map[interval])
        bars = []
        if history_updated:
            # todo! 为了性能考虑，先不要广播realtime_bar了
            # realtime_bar = {
            #     'symbol': bar.symbol, 
            #     'exchange': bar.exchange.value,
            #     'datetime': str(bar.datetime),
            #     'interval': interval.value, 
            #     'indicator': Indicator.BAR.value,
            #     'timing': Timing.REALTIME.value, 
            #     'data': {
            #         IndicatorColumn.BARCLOSE.name: close_prices[-1]
            #     }
            # }
            
            history_bar = {
                'symbol': bar.symbol, 
                'exchange': bar.exchange.value,
                'datetime': str(bar.datetime),
                'interval': interval.value, 
                'indicator': Indicator.BAR.value,
                'timing': Timing.HISTORY.value, 
                'data': {
                    IndicatorColumn.BARCLOSE.name: close_prices[-2]
                }
            }
            bars.append(history_bar)
            
            # pdb.set_trace()
            boll_band = talib.BBANDS(close_prices, timeperiod=20)
            realtime_boll = {
                'symbol': bar.symbol, 
                'exchange': bar.exchange.value,
                'datetime': str(bar.datetime),
                'interval': interval.value, 
                'indicator': Indicator.BOLL.value,
                'timing': Timing.REALTIME.value, 
                'data': {
                    IndicatorColumn.BOLLUPPER.name: boll_band[0][-1], 
                    IndicatorColumn.BOLLMIDDLE.name: boll_band[1][-1], 
                    IndicatorColumn.BOLLLOWER.name: boll_band[2][-1]
                }
            }
            history_boll = {
                'symbol': bar.symbol, 
                'exchange': bar.exchange.value,
                'datetime': str(bar.datetime),
                'interval': interval.value, 
                'indicator': Indicator.BOLL.value,
                'timing': Timing.HISTORY.value, 
                'data': {
                    IndicatorColumn.BOLLUPPER.name: boll_band[0][-2],
                    IndicatorColumn.BOLLMIDDLE.name: boll_band[1][-2], 
                    IndicatorColumn.BOLLLOWER.name: boll_band[2][-2]
                }
            }
            bars.append(realtime_boll)
            bars.append(history_boll)
        else:
            # pdb.set_trace()
            boll_band = talib.BBANDS(close_prices[-20:], timeperiod=20)
            realtime_boll = {
                'symbol': bar.symbol, 
                'exchange': bar.exchange.value,
                'datetime': str(bar.datetime),
                'interval': interval.value, 
                'indicator': Indicator.BOLL.value,
                'timing': Timing.REALTIME.value, 
                'data': {
                    IndicatorColumn.BOLLUPPER.name: boll_band[0][-1],
                    IndicatorColumn.BOLLMIDDLE.name: boll_band[1][-1],
                    IndicatorColumn.BOLLLOWER.name: boll_band[2][-1]
                }
            }
            bars.append(realtime_boll)
        return bars

class KsMarketApiServer(ZmqPublisher, ZmqSubscriber, Logger):
    gateway_name: str = 'ks_market_api'
    
    def __init__(self, setting: dict):
        ZmqPublisher.__init__(self, setting['zmq']['pub_address'], server=True)
        ZmqSubscriber.__init__(self, setting['zmq']['sub_address'], server=True)
        Logger.__init__(self)
        
        self.gateway_name = setting.get('gateway_name', self.gateway_name)

        # 使用 Ray 的任务列表来存储多个计算任务的句柄
        self.task_futures = {}
        self.calculators = {}

        self.task_index = 0

        # 初始化 Futu API
        api = KsFutuMarketApi(setting or GATEWAY_CONFIG['market_api']['setting'])
        self.market_api = api

        def on_bar_rt(bar: BarData):
            calculator = self.get_calculator(bar.vt_symbol)  # 使用 stock_symbol 获取对应的 Actor
            # 提交计算任务并记录任务句柄
            future = calculator.add_data.remote(bar)  # 将数据传递给 Actor
            self.task_futures[self.task_index] = future
            self.task_index += 1

        # 设置回调函数
        api.on_bar_rt = on_bar_rt


        # 启动后台线程运行主循环
        self.listener_thread = threading.Thread(target=self.main_loop)
        self.listener_thread.start()

    def on_message(self, topic, msg):
        msg_data = json.loads(msg)
        # todo 以后可能不是都传入list
        for param, value_list in msg_data.items():
            if param in PARAMS2ENUM:
                msg_data[param] = [PARAMS2ENUM[param](x) for x in value_list]
        return self.subscribe(**msg_data)

    def subscribe(
            self,
            vt_symbols: list[str] = [], 
            types: list[SubscribeType] = [], 
            indicators: list[Indicator] = [],
            data_time_types: list[Timing] = []
        ):
        api = self.market_api
        # 订阅市场数据
        api.subscribe(vt_symbols, types)
        for subscribe_type in types:
            for vt_symbol in vt_symbols:
                interval = SUBSCRIBE_TYPE2INTERVAL.get(subscribe_type)
                if not interval == Interval.TICK:
                    ret_k, data_k = api.query_history_n(vt_symbol, 20, interval=interval, adjustment=Adjustment.BACKWARD_ADJUSTMENT)
                    if ret_k == RET_OK:
                        self.log(f'{vt_symbol},{interval.value}历史bars查询成功')
                        calculator = self.get_calculator(vt_symbol)
                        calculator.update_closes.remote(Interval(data_k.interval.iloc[-1]), data_k.close.tolist(), data_k.datetime.tolist())

    def get_calculator(self, vt_symbol):
        if vt_symbol not in self.calculators:
            self.calculators[vt_symbol] = BollingerCalculator.remote()  # 创建新的 Actor
        return self.calculators[vt_symbol]

    # todo 这里不会抛出错误到调试器。例如传入enum给send，会报错，但是调试器不能捕捉
    def process_bollinger_results(self):
        # 遍历所有任务句柄并获取计算结果
        for task_index, future in list(self.task_futures.items()):
            if ray.wait([future], timeout=0)[0]:  # 非阻塞获取结果
                bars = ray.get(future)
                if bars:
                    for bar in bars:
                        bar['gateway_name'] = self.gateway_name
                        self.send('on_indicator', bar)
                del self.task_futures[task_index]  # 处理完毕，删除该任务句柄

    def main_loop(self):
        while True:
            # 定期调用 process_bollinger_results，假设每隔1秒调用一次
            self.process_bollinger_results()
            time.sleep(0.1)  # 每1秒调用一次
            
    def close(self):
        ZmqPublisher.stop(self)
        ZmqSubscriber.stop(self)
            
if __name__ == '__main__':
    print(sys.argv)
    
    # 需要跳过的 Ray 相关进程参数关键字
    ray_args_keywords = [
        "--gcs_server_port",  # GCS 服务器
        "--gcs-address",  # Dashboard 进程
        "--java_worker_command"  # 日志进程
    ]

    # 遍历 `sys.argv`，如果有关键参数，则跳过执行
    if not any(keyword in arg for keyword in ray_args_keywords for arg in sys.argv):
        ray.init(ignore_reinit_error=True, num_cpus=1, local_mode=True)
        
        from ks_trade_api.utility import get_file_path, load_json

        gateway_config_name = 'gateway_config.json'
        gateway_config_path = get_file_path(gateway_config_name)
        config = load_json(gateway_config_path)
        setting_client = config['ks_market_api']['setting']
        setting_server = setting_client.copy()
        setting_server['zmq'] = { 'sub_address': setting_client['zmq']['pub_address'], 'pub_address': setting_client['zmq']['sub_address']}
        print(setting_server)
        KsMarketApiServer(setting_server)

