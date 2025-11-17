#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命令列介面
"""

import argparse
import json
import sys

from .client import TaiwanBankFXClient
from .exceptions import TaiwanBankFXError


def main():
    """命令列主程式"""
    parser = argparse.ArgumentParser(
        description="查詢台灣銀行匯率資料",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  # 查詢美金即時匯率
  %(prog)s --type current --currency USD

  # 查詢最近六個月的歐元歷史匯率
  %(prog)s --type historical --currency EUR --period l6m

  # 查詢特定月份的日圓匯率
  %(prog)s --type historical --currency JPY --period month --date 2025-01

  # 輸出為 JSON 格式
  %(prog)s --type current --currency USD --output json
        """
    )

    parser.add_argument(
        "--type",
        choices=["current", "historical"],
        default="current",
        help="查詢類型：current (即時匯率) 或 historical (歷史匯率)"
    )
    parser.add_argument(
        "--currency",
        type=str,
        default="USD",
        help="幣別代碼，預設為 USD"
    )
    parser.add_argument(
        "--period",
        choices=["ltm", "l6m", "month", "day"],
        default="l6m",
        help="歷史查詢期間：ltm (近3個月), l6m (近6個月), month (單月), day (單日)"
    )
    parser.add_argument(
        "--date",
        type=str,
        help="日期參數：month 查詢使用 'YYYY-MM'，day 查詢使用 'YYYY-MM-DD'"
    )
    parser.add_argument(
        "--rate-type",
        choices=["spot", "cash"],
        default="spot",
        help="匯率類型：spot (即期) 或 cash (現金)，僅在 day 查詢時使用"
    )
    parser.add_argument(
        "--output",
        choices=["json", "csv", "table"],
        default="table",
        help="輸出格式：json, csv 或 table (表格格式)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="限制顯示筆數（僅適用於歷史查詢）"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="請求超時時間（秒），預設為 10 秒"
    )

    args = parser.parse_args()

    try:
        client = TaiwanBankFXClient(timeout=args.timeout)

        if args.type == "current":
            # 查詢即時匯率
            result = client.get_current_rate(currency=args.currency)

            if args.output == "json":
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(f"\n{result['currency_name']} 即時匯率")
                print("=" * 50)
                print(f"現金買入: {result['cash_buy']}")
                print(f"現金賣出: {result['cash_sell']}")
                print(f"即期買入: {result['spot_buy']}")
                print(f"即期賣出: {result['spot_sell']}")
                print(f"查詢時間: {result['timestamp']}")

        elif args.type == "historical":
            # 查詢歷史匯率
            result = client.get_historical_rates(
                currency=args.currency,
                period=args.period,
                date=args.date,
                rate_type=args.rate_type
            )

            if args.limit:
                result = result.head(args.limit)

            if args.output == "json":
                print(result.to_json(orient="records", force_ascii=False, indent=2))
            elif args.output == "csv":
                print(result.to_csv(index=False))
            else:
                print(f"\n{args.currency} 歷史匯率")
                print("=" * 80)
                print(result.to_string(index=False))

        return 0

    except TaiwanBankFXError as e:
        print(f"錯誤: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n操作已取消", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"未預期的錯誤: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
