# -*- coding: UTF-8 -*-

if __name__ == '__main__':
    from rqalpha_data import *

    # df = get_bar('000001.XSHG', '2017-11-24')
    df = get_bars('600469.XSHG', '2017-11-01', 5, fields=['datetime', 'open', 'close'])
    df = get_bars('600469.XSHG', '2017-11-01', 5, convert_to_dataframe=True)
    # df = get_bars('600469.XSHG', '2017-11-01', 5, fields=['open', 'close'], convert_to_dataframe=True)
    print(df)

    # df = get_bars('000001.XSHG', 2, '2017-11-24')
    # print(df)


