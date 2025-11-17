#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣銀行外匯匯率 API 客戶端
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from io import StringIO

from .exceptions import RequestError, ParseError, InvalidParameterError


class TaiwanBankFXClient:
    """
    台灣銀行外匯匯率查詢客戶端

    提供即時匯率和歷史匯率的查詢功能。

    Examples:
        >>> client = TaiwanBankFXClient()
        >>> # 查詢美金即時匯率
        >>> rate = client.get_current_rate("USD")
        >>> print(rate)
        >>> # 查詢歷史匯率
        >>> history = client.get_historical_rates("USD", period="l6m")
        >>> print(history)
    """

    BASE_URL = "https://rate.bot.com.tw/xrt"
    QUOTE_BASE_URL = "https://rate.bot.com.tw/xrt/quote"

    def __init__(self, timeout=10):
        """
        初始化客戶端

        Args:
            timeout (int): 請求超時時間（秒），預設為 10 秒
        """
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_current_rate(self, currency="USD"):
        """
        查詢指定幣別的即時匯率

        Args:
            currency (str): 幣別代碼，如 'USD'、'EUR'、'JPY' 等，預設為 'USD'

        Returns:
            dict: 包含匯率資訊的字典，包含以下欄位：
                - currency: 幣別代碼
                - currency_name: 幣別名稱（中文）
                - cash_buy: 現金買入匯率
                - cash_sell: 現金賣出匯率
                - spot_buy: 即期買入匯率
                - spot_sell: 即期賣出匯率
                - timestamp: 查詢時間

        Raises:
            RequestError: 當請求失敗時
            ParseError: 當解析資料失敗時

        Examples:
            >>> client = TaiwanBankFXClient()
            >>> usd_rate = client.get_current_rate("USD")
            >>> print(f"美金即期買入: {usd_rate['spot_buy']}")
        """
        try:
            url = f"{self.BASE_URL}?Lang=zh-TW"
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            rows = soup.select("table tbody tr")

            # 支援的幣別名稱對照
            currency_names = {
                "USD": "美金",
                "EUR": "歐元",
                "JPY": "日圓",
                "GBP": "英鎊",
                "AUD": "澳幣",
                "CAD": "加拿大幣",
                "SGD": "新加坡幣",
                "CHF": "瑞士法郎",
                "HKD": "港幣",
                "CNY": "人民幣",
                "ZAR": "南非幣",
                "SEK": "瑞典幣",
                "NZD": "紐西蘭幣",
                "THB": "泰幣",
                "KRW": "韓元",
            }

            currency_name = currency_names.get(currency.upper(), currency.upper())

            for row in rows:
                row_text = row.text
                # 檢查是否包含目標幣別和幣別代碼
                if currency_name in row_text and f"({currency.upper()})" in row_text:
                    tds = row.select("td")
                    if len(tds) >= 5:
                        return {
                            "currency": currency.upper(),
                            "currency_name": tds[0].text.strip(),
                            "cash_buy": tds[1].text.strip(),
                            "cash_sell": tds[2].text.strip(),
                            "spot_buy": tds[3].text.strip(),
                            "spot_sell": tds[4].text.strip(),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

            raise ParseError(f"找不到 {currency} 的匯率資訊")

        except requests.RequestException as e:
            raise RequestError(f"請求失敗: {e}")
        except Exception as e:
            if isinstance(e, (RequestError, ParseError)):
                raise
            raise ParseError(f"解析資料時發生錯誤: {e}")

    def get_historical_rates(self, currency="USD", period="l6m", date=None, rate_type="spot"):
        """
        查詢歷史匯率資料

        Args:
            currency (str): 幣別代碼，如 'USD'、'EUR' 等，預設為 'USD'
            period (str): 查詢期間，可選值：
                - 'ltm': 最近三個月
                - 'l6m': 最近六個月（預設）
                - 'month': 單月查詢（需要 date 參數）
                - 'day': 單日查詢（需要 date 和 rate_type 參數）
            date (str, optional): 日期參數：
                - period='month' 時，格式為 'YYYY-MM'
                - period='day' 時，格式為 'YYYY-MM-DD'
            rate_type (str): 匯率類型，'spot'（即期）或 'cash'（現金），預設為 'spot'
                僅在 period='day' 時使用

        Returns:
            pandas.DataFrame: 包含歷史匯率資料的 DataFrame，欄位包括：
                - 日期: 日期
                - 現金買入: 現金買入匯率
                - 現金賣出: 現金賣出匯率
                - 即期買入: 即期買入匯率
                - 即期賣出: 即期賣出匯率

        Raises:
            InvalidParameterError: 當參數無效時
            RequestError: 當請求失敗時
            ParseError: 當解析資料失敗時

        Examples:
            >>> client = TaiwanBankFXClient()
            >>> # 查詢最近六個月的美金匯率
            >>> df = client.get_historical_rates("USD", period="l6m")
            >>> print(df.head())
            >>>
            >>> # 查詢特定月份的歐元匯率
            >>> df = client.get_historical_rates("EUR", period="month", date="2025-01")
            >>> print(df)
        """
        try:
            # 驗證參數
            if period in ['month', 'day'] and not date:
                raise InvalidParameterError(
                    f"period='{period}' 時必須提供 date 參數"
                )

            # 組合 URL
            if period in ['ltm', 'l6m']:
                url = f"{self.QUOTE_BASE_URL}/{period}/{currency}"
            elif period == 'month':
                url = f"{self.QUOTE_BASE_URL}/{date}/{currency}"
            elif period == 'day':
                url = f"{self.QUOTE_BASE_URL}/{date}/{currency}/{rate_type}"
            else:
                raise InvalidParameterError(
                    f"無效的 period 參數: {period}，可選值為 'ltm', 'l6m', 'month', 'day'"
                )

            # 發送請求
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # 解析表格
            tables = pd.read_html(StringIO(response.text))

            if not tables:
                raise ParseError("未找到任何表格資料")

            df = tables[0]

            # 處理欄位名稱
            df = self._process_dataframe_columns(df, period)

            return df

        except ValueError as e:
            raise InvalidParameterError(f"參數錯誤: {e}")
        except requests.RequestException as e:
            raise RequestError(f"請求失敗: {e}")
        except Exception as e:
            if isinstance(e, (InvalidParameterError, RequestError, ParseError)):
                raise
            raise ParseError(f"解析資料時發生錯誤: {e}")

    def _process_dataframe_columns(self, df, period):
        """
        處理 DataFrame 的欄位名稱

        Args:
            df (pandas.DataFrame): 原始 DataFrame
            period (str): 查詢期間類型

        Returns:
            pandas.DataFrame: 處理後的 DataFrame
        """
        # 處理 MultiIndex 欄位
        if isinstance(df.columns, pd.MultiIndex):
            if df.columns.nlevels >= 2:
                new_columns = []
                level0 = df.columns.get_level_values(0)
                level1 = df.columns.get_level_values(1)
                current_level0 = None

                for i, (l0, l1) in enumerate(zip(level0, level1)):
                    l0_str = str(l0).strip()
                    l1_str = str(l1).strip()

                    if 'unnamed' in l0_str.lower() or l0_str in ['', 'NaN', 'nan']:
                        if current_level0:
                            l0_str = current_level0
                    else:
                        current_level0 = l0_str

                    if 'unnamed' in l1_str.lower() or l1_str in ['', 'NaN', 'nan']:
                        if i == 6:
                            l1_str = '本行買入'
                        elif i in [7, 8]:
                            l1_str = '本行賣出'

                    if l0_str and 'unnamed' not in l0_str.lower() and l0_str != 'NaN':
                        if l1_str and 'unnamed' not in l1_str.lower():
                            new_col = f"{l0_str}_{l1_str}"
                        else:
                            new_col = l0_str
                    else:
                        new_col = l1_str if l1_str else f"Column_{i}"

                    new_columns.append(new_col)

                df.columns = new_columns
            else:
                df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else str(col)
                             for col in df.columns.values]

        # 根據查詢類型處理欄位
        if period in ['ltm', 'l6m', 'month']:
            # 找出日期欄位
            date_col_idx = 0
            for idx, col in enumerate(df.columns):
                if '日期' in str(col) or '掛牌' in str(col):
                    date_col_idx = idx
                    break

            # 找出幣別欄位
            currency_col_idx = None
            for idx, col in enumerate(df.columns):
                if '幣別' in str(col):
                    currency_col_idx = idx
                    break

            # 根據欄位位置選取資料
            if currency_col_idx == 2 and len(df.columns) >= 6:
                # 格式：日期、本行買入、幣別、本行賣出、本行買入、本行賣出
                df = df.iloc[:, [0, 2, 3, 4, 5]].copy()
            elif len(df.columns) >= 5:
                # 格式：日期、現金買入、現金賣出、即期買入、即期賣出
                df = df.iloc[:, [0, 1, 2, 3, 4]].copy()

            df.columns = ["日期", "現金買入", "現金賣出", "即期買入", "即期賣出"]

        elif period == 'day':
            # 單日查詢
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
            df.columns = ["類型", "匯率"]

        return df

    def __enter__(self):
        """支援 context manager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """關閉 session"""
        self.session.close()
