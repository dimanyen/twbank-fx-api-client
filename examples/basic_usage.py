#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本使用範例

這個範例展示如何使用 twbank-fx-client 來查詢台灣銀行的匯率資料。
"""

from twbank_fx_client import TaiwanBankFXClient


def example_current_rate():
    """範例 1: 查詢即時匯率"""
    print("=" * 60)
    print("範例 1: 查詢美金即時匯率")
    print("=" * 60)

    # 建立客戶端
    client = TaiwanBankFXClient()

    # 查詢美金即時匯率
    usd_rate = client.get_current_rate("USD")

    print(f"幣別: {usd_rate['currency_name']}")
    print(f"現金買入: {usd_rate['cash_buy']}")
    print(f"現金賣出: {usd_rate['cash_sell']}")
    print(f"即期買入: {usd_rate['spot_buy']}")
    print(f"即期賣出: {usd_rate['spot_sell']}")
    print(f"查詢時間: {usd_rate['timestamp']}")
    print()


def example_multiple_currencies():
    """範例 2: 查詢多種幣別的即時匯率"""
    print("=" * 60)
    print("範例 2: 查詢多種幣別的即時匯率")
    print("=" * 60)

    client = TaiwanBankFXClient()

    # 查詢多種幣別
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD"]

    for currency in currencies:
        try:
            rate = client.get_current_rate(currency)
            print(f"{rate['currency_name']:12} 即期買入: {rate['spot_buy']:8} 即期賣出: {rate['spot_sell']:8}")
        except Exception as e:
            print(f"{currency} 查詢失敗: {e}")

    print()


def example_historical_rates():
    """範例 3: 查詢歷史匯率"""
    print("=" * 60)
    print("範例 3: 查詢最近六個月的美金歷史匯率")
    print("=" * 60)

    client = TaiwanBankFXClient()

    # 查詢最近六個月的美金匯率
    df = client.get_historical_rates("USD", period="l6m")

    # 顯示前 10 筆資料
    print(df.head(10))
    print(f"\n總共 {len(df)} 筆資料")
    print()


def example_monthly_rates():
    """範例 4: 查詢特定月份的歷史匯率"""
    print("=" * 60)
    print("範例 4: 查詢 2025 年 1 月的歐元匯率")
    print("=" * 60)

    client = TaiwanBankFXClient()

    # 查詢特定月份
    df = client.get_historical_rates("EUR", period="month", date="2025-01")

    print(df)
    print()


def example_context_manager():
    """範例 5: 使用 context manager"""
    print("=" * 60)
    print("範例 5: 使用 context manager")
    print("=" * 60)

    # 使用 with 語句自動管理資源
    with TaiwanBankFXClient() as client:
        rate = client.get_current_rate("USD")
        print(f"美金即期買入: {rate['spot_buy']}")
        print(f"美金即期賣出: {rate['spot_sell']}")

    print()


def example_error_handling():
    """範例 6: 錯誤處理"""
    print("=" * 60)
    print("範例 6: 錯誤處理")
    print("=" * 60)

    from twbank_fx_client.exceptions import (
        TaiwanBankFXError,
        RequestError,
        ParseError,
        InvalidParameterError
    )

    client = TaiwanBankFXClient()

    try:
        # 嘗試查詢不存在的幣別
        rate = client.get_current_rate("XXX")
    except ParseError as e:
        print(f"解析錯誤: {e}")
    except RequestError as e:
        print(f"請求錯誤: {e}")
    except TaiwanBankFXError as e:
        print(f"一般錯誤: {e}")

    try:
        # 嘗試使用無效參數查詢歷史匯率
        df = client.get_historical_rates("USD", period="month")  # 缺少 date 參數
    except InvalidParameterError as e:
        print(f"參數錯誤: {e}")

    print()


def example_data_analysis():
    """範例 7: 資料分析"""
    print("=" * 60)
    print("範例 7: 計算最近六個月美金匯率的統計資訊")
    print("=" * 60)

    client = TaiwanBankFXClient()

    # 取得歷史資料
    df = client.get_historical_rates("USD", period="l6m")

    # 轉換為數值型態
    df['即期買入'] = pd.to_numeric(df['即期買入'], errors='coerce')
    df['即期賣出'] = pd.to_numeric(df['即期賣出'], errors='coerce')

    # 計算統計資訊
    print("即期買入匯率統計:")
    print(f"  平均值: {df['即期買入'].mean():.4f}")
    print(f"  最高值: {df['即期買入'].max():.4f}")
    print(f"  最低值: {df['即期買入'].min():.4f}")
    print(f"  標準差: {df['即期買入'].std():.4f}")
    print()

    print("即期賣出匯率統計:")
    print(f"  平均值: {df['即期賣出'].mean():.4f}")
    print(f"  最高值: {df['即期賣出'].max():.4f}")
    print(f"  最低值: {df['即期賣出'].min():.4f}")
    print(f"  標準差: {df['即期賣出'].std():.4f}")
    print()


if __name__ == "__main__":
    import pandas as pd

    # 執行所有範例
    example_current_rate()
    example_multiple_currencies()
    example_historical_rates()
    example_monthly_rates()
    example_context_manager()
    example_error_handling()
    example_data_analysis()

    print("所有範例執行完成！")
