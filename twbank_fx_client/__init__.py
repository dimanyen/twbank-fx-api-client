#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
twbank-fx-client - 台灣銀行外匯匯率查詢 API 客戶端

這個套件提供簡單易用的 API 介面來查詢台灣銀行的即時匯率和歷史匯率資料。
"""

__version__ = "0.1.0"
__author__ = "Your Name"

from .client import TaiwanBankFXClient
from .exceptions import (
    TaiwanBankFXError,
    RequestError,
    ParseError,
    InvalidParameterError
)

__all__ = [
    "TaiwanBankFXClient",
    "TaiwanBankFXError",
    "RequestError",
    "ParseError",
    "InvalidParameterError",
]
