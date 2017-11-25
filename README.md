# RQAlpha-Data

[![PyPI Version](https://img.shields.io/pypi/v/rqalpha-data.svg)](https://pypi.python.org/pypi/rqalpha-data)

## Overview
A utility for RQAlpha to directly use data.

不需要在回测里而是直接调用 RQAlpha 的数据。



对 history_bars 函数进行一定包装后变成 get_bars 函数，以便直接在 Jupyter 中直接使用！

匆忙写就，欢迎各位提问题以便改进它，当然更欢迎给我加个 Star。

最终效果：

![img](https://pic3.zhimg.com/50/v2-6cdf9e049c3d738cace34500537008ee.jpg)

### 常用的函数：

* is_trading_date 判断是否是交易日

* get_trading_dates - 交易日列表

* get_previous_trading_date - 上一交易日

* get_next_trading_date - 下一交易日

* is_suspended - 全天停牌判断

* is_st_stock - ST股判断​

* get_prev_close

* get_bar 和RQAlpha兼容

* history 和RQAlpha兼容

* history_bars 和RQAlpha兼容

* get_bars 推荐使用

  （注意：如果中间有停牌日期，则自动跳过，保证最后数据行数为 bar_count = 5 个）

  | field          | 字段名  |
  | -------------- | ---- |
  | open           | 开盘价  |
  | high           | 最高价  |
  | low            | 最低价  |
  | close          | 收盘价  |
  | volume         | 成交量  |
  | total_turnover | 成交额  |
  | datetime       | 时间   |



```
get_bars(order_book_id,
        dt,
        bar_count=1,
        frequency='1d',
        fields=None,
        skip_suspended=True,
        include_now=False,
        adjust_type='pre',
        adjust_orig=None,
        convert_to_dataframe=False)
```

## Install

#### Install rqalpha
```bash
$ pip install rqalpha
```

#### Install rqalpha-data
```bash
$ pip install rqalpha-data
```

## Quick Start

### 数据更新

如果第一次使用或想要更新数据，请调用 update 方法

```python
from rqalpha_data import datasource
datasource.update()
```

### get_bars

1. 获取单支股票，返回格式为数组

```python
from rqalpha_data import *

df = get_bars('600469.XSHG', '2017-11-01', 5, fields=['datetime', 'open', 'close'])
print(df)
```

输出（注意：如果中间有停牌日期，则自动跳过，保证最后数据行数为 bar_count = 5 个）

```python
[(20171025000000L, 8.09, 8.16) (20171026000000L, 8.16, 8.18)
 (20171027000000L, 8.17, 8.11) (20171030000000L, 8.11, 7.98)
 (20171101000000L, 7.88, 7.44)]
```



2. 获取单支股票，返回格式为DataFrame

```python
from rqalpha_data import *

df = get_bars('600469.XSHG', '2017-11-01', 5, fields=['datetime', 'open', 'close'], convert_to_dataframe=True)
print(df)
```

输出（注意：如果中间有停牌日期，则自动跳过，保证最后数据行数为 bar_count = 5 个）

```python
            open  close
                       
2017-10-25  8.09   8.16
2017-10-26  8.16   8.18
2017-10-27  8.17   8.11
2017-10-30  8.11   7.98
2017-11-01  7.88   7.44
```



### 如何在 Jupyter 中使用 rqalpha 进行回测
有的朋友可能不知道如何在 Jupyter 中使用 rqalpha 进行回测

1. 用 %reload_ext rqalpha 命令加载 %%rqalpha命令

2. 用 %%rqalpha 命令运行回测

   ![img](https://pic1.zhimg.com/50/v2-8ce420194c0627d5eff59913c0b513f0.jpg)

## License

[MIT](https://tldrlegal.com/license/mit-license)

