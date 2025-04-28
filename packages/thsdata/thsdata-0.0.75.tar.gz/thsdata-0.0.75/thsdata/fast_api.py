import pandas as pd

from thsdata.quote import Quote, Adjust, Interval

global_quote = Quote()


def download(code: str, start=None, end=None, adjust=Adjust.NONE, period="max", interval=Interval.DAY,
             count=-1) -> pd.DataFrame:
    """获取历史k线数据。

   :param period:  str max
   :param code: 证券代码，支持格式
                    6位数字代码:600519;
                    8位缩写市场和数字代码:sh600519;
                    9位缩写尾部市场和数字代码:600519.sh
                    10个字符标准ths格式代码(前4位指定市场market，比如并以'USHA'或'USZA'开头):USHA600519
   :param count: 需要的数量，推荐使用此参数
   :param start: 开始时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
   :param end: 结束时间，格式取决于周期。对于日级别，使用日期（例如，20241224）。对于分钟级别，使用时间戳。
   :param adjust: 复权类型，必须是有效的复权值之一。
   :param interval: 周期类型，必须是有效的周期值之一。

   :return: pandas.DataFrame

    Example::

            time    close   volume    turnover     open     high      low
        2024-01-02  1685.01  3215644  5440082500  1715.00  1718.19  1678.10
        2024-01-03  1694.00  2022929  3411400700  1681.11  1695.22  1676.33
        2024-01-04  1669.00  2155107  3603970100  1693.00  1693.00  1662.93
    """
    data = global_quote.download(code, start, end, adjust, period, interval, count)
    # Check if data is empty
    if data.empty:
        print("No data returned. Reconnecting...")
        global_quote.main_quote.disconnect()  # Reconnect to the server
        global_quote.main_quote.connect()  # Reconnect to the server

    return data
