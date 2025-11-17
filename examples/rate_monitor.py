#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
匯率監控範例

這個範例展示如何使用 twbank-fx-client 監控匯率變化。
"""

import time
from datetime import datetime
from twbank_fx_client import TaiwanBankFXClient


class RateMonitor:
    """匯率監控器"""

    def __init__(self, currency="USD", threshold=0.1):
        """
        初始化監控器

        Args:
            currency (str): 要監控的幣別
            threshold (float): 警示門檻（匯率變化超過此值時發出警示）
        """
        self.client = TaiwanBankFXClient()
        self.currency = currency
        self.threshold = threshold
        self.last_rate = None

    def check_rate(self):
        """檢查目前匯率"""
        rate_info = self.client.get_current_rate(self.currency)
        current_rate = float(rate_info['spot_buy'])

        result = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "currency": self.currency,
            "rate": current_rate,
            "cash_buy": rate_info['cash_buy'],
            "cash_sell": rate_info['cash_sell'],
            "spot_buy": rate_info['spot_buy'],
            "spot_sell": rate_info['spot_sell'],
            "change": None,
            "change_percentage": None,
            "alert": False
        }

        if self.last_rate is not None:
            change = current_rate - self.last_rate
            change_percentage = (change / self.last_rate) * 100

            result["change"] = change
            result["change_percentage"] = change_percentage

            # 檢查是否超過門檻
            if abs(change) >= self.threshold:
                result["alert"] = True

        self.last_rate = current_rate

        return result

    def monitor(self, interval=300, duration=3600):
        """
        持續監控匯率

        Args:
            interval (int): 檢查間隔（秒），預設 300 秒（5 分鐘）
            duration (int): 監控持續時間（秒），預設 3600 秒（1 小時）
        """
        print(f"開始監控 {self.currency} 匯率")
        print(f"檢查間隔: {interval} 秒")
        print(f"警示門檻: {self.threshold}")
        print("=" * 80)
        print()

        start_time = time.time()

        try:
            while True:
                # 檢查是否超過監控時間
                elapsed = time.time() - start_time
                if elapsed >= duration:
                    print(f"\n監控時間已達 {duration} 秒，結束監控")
                    break

                # 檢查匯率
                result = self.check_rate()

                # 顯示資訊
                print(f"[{result['timestamp']}] {result['currency']}")
                print(f"  即期買入: {result['spot_buy']} / 即期賣出: {result['spot_sell']}")
                print(f"  現金買入: {result['cash_buy']} / 現金賣出: {result['cash_sell']}")

                if result['change'] is not None:
                    change_symbol = "▲" if result['change'] > 0 else "▼"
                    print(f"  變化: {change_symbol} {result['change']:+.4f} ({result['change_percentage']:+.2f}%)")

                    if result['alert']:
                        print(f"  ⚠️  警示: 匯率變化超過門檻 {self.threshold}")

                print()

                # 等待下次檢查
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n監控已中斷")


def compare_multiple_currencies():
    """比較多種幣別的匯率"""
    print("=" * 80)
    print("多幣別匯率比較")
    print("=" * 80)
    print()

    client = TaiwanBankFXClient()
    currencies = ["USD", "EUR", "JPY", "GBP", "AUD", "HKD", "CNY"]

    print(f"{'幣別':<8} {'即期買入':>10} {'即期賣出':>10} {'現金買入':>10} {'現金賣出':>10}")
    print("-" * 80)

    for currency in currencies:
        try:
            rate = client.get_current_rate(currency)
            print(f"{currency:<8} {rate['spot_buy']:>10} {rate['spot_sell']:>10} "
                  f"{rate['cash_buy']:>10} {rate['cash_sell']:>10}")
        except Exception as e:
            print(f"{currency:<8} 查詢失敗: {e}")

    print()


def rate_alert_example():
    """匯率警示範例"""
    print("=" * 80)
    print("匯率警示範例")
    print("=" * 80)
    print()

    client = TaiwanBankFXClient()

    # 設定目標匯率
    target_currency = "USD"
    target_buy_rate = 31.5  # 假設目標買入匯率
    target_sell_rate = 32.0  # 假設目標賣出匯率

    print(f"監控幣別: {target_currency}")
    print(f"目標買入匯率: {target_buy_rate}")
    print(f"目標賣出匯率: {target_sell_rate}")
    print()

    # 查詢目前匯率
    rate = client.get_current_rate(target_currency)
    current_buy = float(rate['spot_buy'])
    current_sell = float(rate['spot_sell'])

    print(f"目前買入匯率: {current_buy:.4f}")
    print(f"目前賣出匯率: {current_sell:.4f}")
    print()

    # 檢查是否達到目標
    if current_buy <= target_buy_rate:
        print(f"✓ 買入匯率已達目標！({current_buy:.4f} <= {target_buy_rate})")
        print("  建議: 可以考慮將台幣換成外幣")
    else:
        print(f"✗ 買入匯率尚未達標 ({current_buy:.4f} > {target_buy_rate})")
        print(f"  距離目標: {current_buy - target_buy_rate:.4f}")

    print()

    if current_sell >= target_sell_rate:
        print(f"✓ 賣出匯率已達目標！({current_sell:.4f} >= {target_sell_rate})")
        print("  建議: 可以考慮將外幣換回台幣")
    else:
        print(f"✗ 賣出匯率尚未達標 ({current_sell:.4f} < {target_sell_rate})")
        print(f"  距離目標: {target_sell_rate - current_sell:.4f}")

    print()


def main():
    """主程式"""
    # 範例 1: 比較多種幣別
    compare_multiple_currencies()

    # 範例 2: 匯率警示
    rate_alert_example()

    # 範例 3: 持續監控（註解掉，避免長時間執行）
    # 如果要執行監控，請取消註解以下程式碼
    """
    print("=" * 80)
    print("持續監控範例")
    print("=" * 80)
    print()

    monitor = RateMonitor(currency="USD", threshold=0.05)

    # 監控 1 小時，每 5 分鐘檢查一次
    monitor.monitor(interval=300, duration=3600)
    """

    print("範例執行完成！")
    print()
    print("提示: 如要執行持續監控，請編輯程式碼取消註解相關區塊")


if __name__ == "__main__":
    main()
