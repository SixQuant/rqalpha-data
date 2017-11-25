# -*- coding: UTF-8 -*-

import os
import datetime
import pandas as pd
from rqalpha.data.data_proxy import DataProxy
from rqalpha.utils.datetime_func import convert_int_to_datetime

from rqalpha_data.datetime_utils import to_date_object
from rqalpha_data.quant_utils import to_order_book_id


class DataSource(DataProxy):
    """
    直接使用RQAlpha的全部数据
    """

    def __init__(self, data_bundle_path=None):
        default_bundle_path = os.path.abspath(os.path.expanduser('~/.rqalpha'))
        if data_bundle_path is None:
            data_bundle_path = default_bundle_path
        else:
            data_bundle_path = os.path.abspath(os.path.join(data_bundle_path, '.'))

        data_bundle_path = data_bundle_path + '/bundle'

        self._data_bundle_path = data_bundle_path

        # basic_system_log.debug('rqalpha data bundle path: ' + data_bundle_path)
        if not os.path.exists(data_bundle_path):
            self.update(skip_last_date_check=True)

        from rqalpha.data.base_data_source import BaseDataSource
        data_source = BaseDataSource(data_bundle_path)
        super(DataSource, self).__init__(data_source)

        self._last_date_date = None
        self.get_data_last_date()
        # basic_system_log.debug('rqalpha data bundle date: ' + self._last_date_date.strftime('%Y-%m-%d'))

    def get_data_last_date(self):
        """返回最新数据日期"""
        if self._last_date_date is not None:
            return self._last_date_date

        d = self._data_source

        instrument = self.instruments('000001.XSHG')
        raw = d._all_day_bars_of(instrument)
        df = pd.DataFrame.from_dict(raw)
        df['datetime'] = df['datetime'].map(lambda x: pd.to_datetime(str(x)[:8]))

        self._last_date_date = df['datetime'].max().date()

        del df, raw, instrument, d

        return self._last_date_date

    def get_last_trading_day(self):
        """返回最后交易日期"""
        date = datetime.date.today()
        while not self.is_trading_date(date):
            date = date + datetime.timedelta(days=-1)
        return date

    def update(self, skip_last_date_check=False):
        """
        更新最新的远程数据到本地
        """
        if not skip_last_date_check:
            last_trading_day = self.get_last_trading_day()

            data_bundle_path = self._data_bundle_path
            if os.path.exists(data_bundle_path):
                date = self.get_data_last_date()
                if date == last_trading_day:
                    return date  # 数据已经是最新无需下载
                    # basic_system_log.debug('need update data bundle to ' + date.strftime('%Y-%m-%d'))

        data_bundle_path = self._data_bundle_path
        data_bundle_path = data_bundle_path[:len(data_bundle_path) - len('/bundle')]
        from rqalpha import main
        main.update_bundle(data_bundle_path=data_bundle_path)

        if not skip_last_date_check:
            date = self.get_data_last_date()
            return date

    def get_bar(self, order_book_id, dt, frequency='1d'):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)
        return super(DataSource, self).get_bar(order_book_id=order_book_id, dt=dt, frequency=frequency)

    def history_bars(self,
                     order_book_id,
                     bar_count,
                     frequency,
                     field,
                     dt,
                     skip_suspended=True, include_now=False,
                     adjust_type='pre', adjust_orig=None):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)
        bars = super(DataSource, self).history_bars(order_book_id=order_book_id,
                                                    bar_count=bar_count,
                                                    frequency=frequency,
                                                    field=field,
                                                    dt=dt,
                                                    skip_suspended=skip_suspended,
                                                    include_now=include_now,
                                                    adjust_type=adjust_type,
                                                    adjust_orig=adjust_orig)
        return bars

    def get_bars(self,
                 order_book_id,
                 dt,
                 bar_count=1,
                 frequency='1d',
                 fields=None,
                 skip_suspended=True,
                 include_now=False,
                 adjust_type='pre',
                 adjust_orig=None,
                 convert_to_dataframe=False):
        order_book_id = to_order_book_id(order_book_id)
        dt = to_date_object(dt)

        if fields is None:
            fields = ['datetime', 'open', 'high', 'low', 'close', 'volume', 'total_turnover']

        bars = super(DataSource, self).history_bars(order_book_id=order_book_id,
                                                    bar_count=bar_count,
                                                    frequency=frequency,
                                                    field=fields,
                                                    dt=dt,
                                                    skip_suspended=skip_suspended,
                                                    include_now=include_now,
                                                    adjust_type=adjust_type,
                                                    adjust_orig=adjust_orig)
        if convert_to_dataframe:
            df = pd.DataFrame.from_dict(bars)
            if 'datetime' in df.columns:
                df['datetime'] = df['datetime'].map(lambda x: convert_int_to_datetime(x))
                df.set_index('datetime', inplace=True)
                df.index.name = ''
            return df

        return bars


datasource = DataSource()


def is_trading_date(date):
    datasource.is_trading_date(date)


def get_bar(order_book_id, dt, frequency='1d'):
    return datasource.get_bar(order_book_id=order_book_id, dt=dt, frequency=frequency)


def history_bars(
        order_book_id,
        bar_count,
        frequency,
        field,
        dt,
        skip_suspended=True,
        include_now=False,
        adjust_type='pre',
        adjust_orig=None):
    return datasource.history_bars(order_book_id=order_book_id,
                                   bar_count=bar_count,
                                   frequency=frequency,
                                   field=field,
                                   dt=dt,
                                   skip_suspended=skip_suspended,
                                   include_now=include_now,
                                   adjust_type=adjust_type,
                                   adjust_orig=adjust_orig)


def get_bars(order_book_id,
             dt,
             bar_count=1,
             frequency='1d',
             fields=None,
             skip_suspended=True,
             include_now=False,
             adjust_type='pre',
             adjust_orig=None,
             convert_to_dataframe=False):
    return datasource.get_bars(order_book_id=order_book_id,
                               bar_count=bar_count,
                               dt=dt,
                               frequency=frequency,
                               fields=fields,
                               skip_suspended=skip_suspended,
                               include_now=include_now,
                               adjust_type=adjust_type,
                               adjust_orig=adjust_orig,
                               convert_to_dataframe=convert_to_dataframe)
