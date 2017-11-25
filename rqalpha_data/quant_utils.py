# -*- coding: UTF-8 -*-


def to_order_book_id(stocks):
    """增加股票代码后缀, 对应 to_pure_code()
    兼容米宽的代码
    order_book_id 证券代码
    证券的独特的标识符。应以'.XSHG'或'.XSHE'结尾，前者代表上证，后者代表深证
    """
    if not isinstance(stocks, str):
        rs = []
        for stock in stocks:
            rs.append(to_order_book_id(stock))
        return rs

    stock = stocks
    if len(stock) == 11:
        return stock

    c = stock[:1]
    if c == '0' or c == '3':
        return stock + '.XSHE'
    elif c == '6':
        return stock + '.XSHG'
    else:
        raise NameError(stock)


def to_pure_code(order_book_id):
    """返回去除后缀后的股票代码, 对应 to_order_book_id()
    兼容米宽的代码
    order_book_id 证券代码
    证券的独特的标识符。应以'.XSHG'或'.XSHE'结尾，前者代表上证，后者代表深证
    """
    if not isinstance(order_book_id, str):
        rs = []
        for stock in order_book_id:
            rs.append(to_pure_code(stock))
        return rs

    stock = order_book_id
    if len(stock) == 6:
        return stock

    return stock[:6]
