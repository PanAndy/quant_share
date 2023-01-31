from datetime import timedelta
from typing import List, Optional
from pytz import timezone
import traceback

import pandas as pd
from tqsdk import TqApi, TqAuth

from vnpy.trader.datafeed import BaseDatafeed
from vnpy.trader.setting import SETTINGS
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import BarData, HistoryRequest


INTERVAL_VT2TQ = {
    Interval.MINUTE: 60,
    Interval.HOUR: 60 * 60,
    Interval.DAILY: 60 * 60 * 24,
    Interval.TICK: 0
}

CHINA_TZ = timezone("Asia/Shanghai")

MAIN_SUFFIX = "888"
INDEX_SUFFIX = "999"
MAIN_SUFFIX_OLD = "L"
INDEX_SUFFIX_OLD = "I"

class TqsdkDatafeed(BaseDatafeed):
    """天勤TQsdk数据服务接口"""

    def __init__(self):
        """"""
        self.username: str = SETTINGS["datafeed.username"]
        self.password: str = SETTINGS["datafeed.password"]

    def query_bar_history(self, req: HistoryRequest) -> Optional[List[BarData]]:
        """查询k线数据"""
        # 初始化API
        try:
            api = TqApi(auth=TqAuth(self.username, self.password))
        except Exception:
            traceback.print_exc()
            return None

        # 查询数据
        if MAIN_SUFFIX in req.symbol:
            req_symbol = req.symbol.replace(MAIN_SUFFIX, "")
            if req.exchange is Exchange.CZCE:
                tq_symbol = "KQ.m@{}.{}".format(req.exchange.value, req_symbol.upper())
            else:
                tq_symbol = "KQ.m@{}.{}".format(req.exchange.value, req_symbol.lower())
        elif INDEX_SUFFIX in req.symbol:
            req_symbol = req.symbol.replace(INDEX_SUFFIX, "")
            if req.exchange is Exchange.CZCE:
                tq_symbol = "KQ.i@{}.{}".format(req.exchange.value, req_symbol.upper())
            else:
                tq_symbol = "KQ.i@{}.{}".format(req.exchange.value, req_symbol.lower())
        else:
            tq_symbol = f"{req.exchange.value}.{req.symbol}"

        data_length = int((req.end - req.start).total_seconds() / INTERVAL_VT2TQ[req.interval])
        df: pd.DataFrame = api.get_kline_serial(
            symbol=tq_symbol,
            duration_seconds=INTERVAL_VT2TQ[req.interval],
            data_length=data_length
        )

        # 关闭API
        api.close()

        # 解析数据
        bars: List[BarData] = []

        if df is not None:
            for tp in df.itertuples():
                # 天勤时间为与1970年北京时间相差的秒数，需要加上8小时差
                dt = pd.Timestamp(tp.datetime).to_pydatetime() + timedelta(hours=8)

                bar = BarData(
                    symbol=req.symbol,
                    exchange=req.exchange,
                    interval=req.interval,
                    datetime=CHINA_TZ.localize(dt),
                    open_price=tp.open,
                    high_price=tp.high,
                    low_price=tp.low,
                    close_price=tp.close,
                    volume=tp.volume,
                    open_interest=tp.open_oi,
                    gateway_name="TQ",
                )
                bars.append(bar)

        return bars
