#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
貨幣轉換器範例

這個範例展示如何使用 twbank-fx-client 建立一個簡單的貨幣轉換器。
"""

from twbank_fx_client import TaiwanBankFXClient


class CurrencyConverter:
    """貨幣轉換器"""

    def __init__(self):
        self.client = TaiwanBankFXClient()

    def twd_to_foreign(self, currency, amount, use_cash=False):
        """
        將台幣轉換為外幣（銀行買入外幣）

        Args:
            currency (str): 外幣幣別代碼
            amount (float): 台幣金額
            use_cash (bool): 是否使用現金匯率

        Returns:
            dict: 包含轉換結果的字典
        """
        rate_info = self.client.get_current_rate(currency)

        # 銀行買入外幣（我們賣出外幣給銀行），使用買入匯率
        if use_cash:
            rate = float(rate_info['cash_buy'])
            rate_type = "現金匯率"
        else:
            rate = float(rate_info['spot_buy'])
            rate_type = "即期匯率"

        foreign_amount = amount / rate

        return {
            "from_currency": "TWD",
            "to_currency": currency,
            "from_amount": amount,
            "to_amount": foreign_amount,
            "rate": rate,
            "rate_type": rate_type,
            "description": f"銀行買入 {currency}（客戶賣出）"
        }

    def foreign_to_twd(self, currency, amount, use_cash=False):
        """
        將外幣轉換為台幣（銀行賣出外幣）

        Args:
            currency (str): 外幣幣別代碼
            amount (float): 外幣金額
            use_cash (bool): 是否使用現金匯率

        Returns:
            dict: 包含轉換結果的字典
        """
        rate_info = self.client.get_current_rate(currency)

        # 銀行賣出外幣（我們買入外幣），使用賣出匯率
        if use_cash:
            rate = float(rate_info['cash_sell'])
            rate_type = "現金匯率"
        else:
            rate = float(rate_info['spot_sell'])
            rate_type = "即期匯率"

        twd_amount = amount * rate

        return {
            "from_currency": currency,
            "to_currency": "TWD",
            "from_amount": amount,
            "to_amount": twd_amount,
            "rate": rate,
            "rate_type": rate_type,
            "description": f"銀行賣出 {currency}（客戶買入）"
        }

    def calculate_spread(self, currency, use_cash=False):
        """
        計算買賣價差

        Args:
            currency (str): 幣別代碼
            use_cash (bool): 是否使用現金匯率

        Returns:
            dict: 包含價差資訊的字典
        """
        rate_info = self.client.get_current_rate(currency)

        if use_cash:
            buy_rate = float(rate_info['cash_buy'])
            sell_rate = float(rate_info['cash_sell'])
            rate_type = "現金匯率"
        else:
            buy_rate = float(rate_info['spot_buy'])
            sell_rate = float(rate_info['spot_sell'])
            rate_type = "即期匯率"

        spread = sell_rate - buy_rate
        spread_percentage = (spread / buy_rate) * 100

        return {
            "currency": currency,
            "buy_rate": buy_rate,
            "sell_rate": sell_rate,
            "spread": spread,
            "spread_percentage": spread_percentage,
            "rate_type": rate_type
        }


def main():
    """主程式"""
    converter = CurrencyConverter()

    print("=" * 70)
    print("貨幣轉換器範例")
    print("=" * 70)
    print()

    # 範例 1: 台幣轉美金
    print("範例 1: 將 10,000 台幣轉換為美金")
    print("-" * 70)
    result = converter.twd_to_foreign("USD", 10000)
    print(f"台幣金額: NT$ {result['from_amount']:,.2f}")
    print(f"美金金額: $ {result['to_amount']:.2f}")
    print(f"使用匯率: {result['rate']:.4f} ({result['rate_type']})")
    print(f"說明: {result['description']}")
    print()

    # 範例 2: 美金轉台幣
    print("範例 2: 將 500 美金轉換為台幣")
    print("-" * 70)
    result = converter.foreign_to_twd("USD", 500)
    print(f"美金金額: $ {result['from_amount']:,.2f}")
    print(f"台幣金額: NT$ {result['to_amount']:,.2f}")
    print(f"使用匯率: {result['rate']:.4f} ({result['rate_type']})")
    print(f"說明: {result['description']}")
    print()

    # 範例 3: 使用現金匯率
    print("範例 3: 使用現金匯率將 10,000 台幣轉換為美金")
    print("-" * 70)
    result = converter.twd_to_foreign("USD", 10000, use_cash=True)
    print(f"台幣金額: NT$ {result['from_amount']:,.2f}")
    print(f"美金金額: $ {result['to_amount']:.2f}")
    print(f"使用匯率: {result['rate']:.4f} ({result['rate_type']})")
    print(f"說明: {result['description']}")
    print()

    # 範例 4: 計算買賣價差
    print("範例 4: 計算美金的買賣價差")
    print("-" * 70)
    currencies = ["USD", "EUR", "JPY", "GBP"]

    for currency in currencies:
        try:
            spread = converter.calculate_spread(currency)
            print(f"{currency} ({spread['rate_type']})")
            print(f"  買入匯率: {spread['buy_rate']:.4f}")
            print(f"  賣出匯率: {spread['sell_rate']:.4f}")
            print(f"  價差: {spread['spread']:.4f} ({spread['spread_percentage']:.2f}%)")
            print()
        except Exception as e:
            print(f"{currency} 查詢失敗: {e}")
            print()

    # 範例 5: 旅遊預算計算
    print("範例 5: 計算日本旅遊預算")
    print("-" * 70)
    print("假設預算: NT$ 50,000")
    print()

    # 現金匯率（適合出國旅遊）
    result = converter.twd_to_foreign("JPY", 50000, use_cash=True)
    print(f"可換日圓: ¥ {result['to_amount']:,.2f}")
    print(f"使用匯率: {result['rate']:.4f} ({result['rate_type']})")
    print()

    # 計算剩餘日圓換回台幣
    print("假設旅遊結束後剩餘 ¥ 10,000")
    result = converter.foreign_to_twd("JPY", 10000, use_cash=True)
    print(f"可換回台幣: NT$ {result['to_amount']:,.2f}")
    print(f"使用匯率: {result['rate']:.4f} ({result['rate_type']})")
    print()


if __name__ == "__main__":
    main()
