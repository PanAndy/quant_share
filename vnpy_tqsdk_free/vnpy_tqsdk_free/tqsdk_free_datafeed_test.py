# 配置好vt_setting.json里的datafeed字段后，运行测试
from vnpy_tqsdk_free.vnpy_tqsdk_free.tqsdk_free_datafeed import TqsdkDatafeed
from vnpy.trader.object import HistoryRequest
from vnpy.trader.constant import Exchange, Interval
from datetime import datetime, timedelta

test_day_len = 1000


def main():
    data_feed = TqsdkDatafeed()
    req = HistoryRequest(symbol="rb2201",
                         exchange=Exchange.SHFE,
                         start=datetime.now() - timedelta(days=test_day_len),
                         end=datetime.now(),
                         interval=Interval.DAILY)

    bars = data_feed.query_bar_history(req=req)

    for bar in bars:
        print(bar)


if __name__ == "__main__":
    main()
