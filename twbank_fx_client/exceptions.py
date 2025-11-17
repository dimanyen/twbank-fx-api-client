#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
例外類別定義
"""


class TaiwanBankFXError(Exception):
    """基礎例外類別"""
    pass


class RequestError(TaiwanBankFXError):
    """請求錯誤"""
    pass


class ParseError(TaiwanBankFXError):
    """解析錯誤"""
    pass


class InvalidParameterError(TaiwanBankFXError):
    """無效的參數"""
    pass
