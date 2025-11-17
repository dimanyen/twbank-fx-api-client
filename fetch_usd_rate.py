#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查詢台灣銀行美金即時匯率與歷史匯率資料
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import argparse
import pandas as pd
from io import StringIO

URL = "https://rate.bot.com.tw/xrt?Lang=zh-TW"


def fetch_usd_rate():
    """
    從台灣銀行網站查詢美金即時匯率
    
    Returns:
        dict: 包含現金買入、現金賣出、即期買入、即期賣出匯率的字典
    """
    try:
        r = requests.get(URL, timeout=10)
        r.raise_for_status()  # 檢查 HTTP 錯誤
        
        soup = BeautifulSoup(r.text, "html.parser")

        # 找「美金 (USD)」的那一列
        rows = soup.select("table tbody tr")
        for row in rows:
            if "美金" in row.text:
                tds = row.select("td")
                if len(tds) >= 5:
                    cash_buy = tds[1].text.strip()
                    cash_sell = tds[2].text.strip()
                    spot_buy = tds[3].text.strip()
                    spot_sell = tds[4].text.strip()
                    
                    return {
                        "currency": "USD",
                        "cash_buy": cash_buy,
                        "cash_sell": cash_sell,
                        "spot_buy": spot_buy,
                        "spot_sell": spot_sell,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
        
        return None
    except requests.RequestException as e:
        print(f"請求錯誤: {e}")
        return None
    except Exception as e:
        print(f"發生錯誤: {e}")
        return None


def fetch_bot_rates(currency="USD", query_type="l6m", date=None, rate_type="spot"):
    """
    依照輸入參數抓取臺灣銀行匯率資料。
    
    Args:
        currency (str): 幣別代碼，如 'USD'、'EUR' 等，預設為 'USD'。
        query_type (str): 查詢類型，可選值：
            - 'ltm': 最近三個月
            - 'l6m': 最近六個月
            - 'month': 單月查詢（需要 date 參數）
            - 'day': 單日查詢（需要 date 和 rate_type 參數）
        date (str, optional): 當 query_type 為 'month' 或 'day' 時，
            分別填入 'YYYY-MM' 或 'YYYY-MM-DD' 格式。
        rate_type (str, optional): 'spot' 或 'cash'，僅在日查詢時需要，預設為 'spot'。
    
    Returns:
        pandas.DataFrame: 含日期、現金買入、現金賣出、即期買入、即期賣出等欄位。
    """
    try:
        # 組合 URL
        base = "https://rate.bot.com.tw/xrt/quote"
        
        if query_type in ['ltm', 'l6m']:
            url = f"{base}/{query_type}/{currency}"
        elif query_type == 'month' and date:
            url = f"{base}/{date}/{currency}"
        elif query_type == 'day' and date:
            url = f"{base}/{date}/{currency}/{rate_type}"
        else:
            raise ValueError("無效的查詢條件：query_type 為 'month' 或 'day' 時必須提供 date 參數")
        
        # 送出請求並取得表格
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        
        # 使用 StringIO 包裝 HTML 字串以避免 FutureWarning
        tables = pd.read_html(StringIO(resp.text))
        
        if not tables:
            print("錯誤: 未找到任何表格")
            return None
        
        df = tables[0]
        
        # 處理 MultiIndex 欄位
        is_multiindex = isinstance(df.columns, pd.MultiIndex)
        if is_multiindex:
            if df.columns.nlevels >= 2:
                # 建立新的欄位名稱，結合第一層和第二層來識別欄位
                new_columns = []
                level0 = df.columns.get_level_values(0)
                level1 = df.columns.get_level_values(1)
                
                # 追蹤當前第一層的值（用於處理合併儲存格）
                current_level0 = None
                
                for i, (l0, l1) in enumerate(zip(level0, level1)):
                    l0_str = str(l0).strip()
                    l1_str = str(l1).strip()
                    
                    # 處理合併儲存格（Unnamed 或空值）
                    if 'unnamed' in l0_str.lower() or l0_str == '' or l0_str == 'NaN' or l0_str == 'nan':
                        # 如果第一層是 Unnamed，使用前一個非 Unnamed 的值
                        if current_level0:
                            l0_str = current_level0
                    else:
                        # 更新當前第一層的值
                        current_level0 = l0_str
                    
                    # 處理第二層的 Unnamed
                    if 'unnamed' in l1_str.lower() or l1_str == '' or l1_str == 'NaN' or l1_str == 'nan':
                        # 根據位置推斷：通常在即期匯率區塊，應該是「本行買入」或「本行賣出」
                        # 根據位置：索引 6, 7, 8 通常是即期匯率的買入和賣出
                        if i == 6:
                            l1_str = '本行買入'
                        elif i == 7:
                            l1_str = '本行賣出'
                        elif i == 8:
                            l1_str = '本行賣出'  # 可能是多餘的欄位
                    
                    # 組合欄位名稱：如果第一層有值且不是 Unnamed，則組合；否則只用第二層
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
                # 扁平化處理
                df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else str(col) for col in df.columns.values]
        
        # 根據不同查詢類型調整欄位名稱
        if query_type in ['ltm', 'l6m', 'month']:
            # 尋找日期欄位（通常是第一欄或包含"日期"、"掛牌"等關鍵字）
            date_col = None
            date_col_idx = 0
            for idx, col in enumerate(df.columns):
                col_str = str(col)
                if '日期' in col_str or '掛牌' in col_str:
                    date_col = col
                    date_col_idx = idx
                    break
            
            if not date_col and len(df.columns) > 0:
                date_col = df.columns[0]
                date_col_idx = 0
            
            # 尋找幣別欄位位置（用於排除）
            currency_col_idx = None
            for idx, col in enumerate(df.columns):
                if '幣別' in str(col):
                    currency_col_idx = idx
                    break
            
            # 根據欄位位置和名稱識別匯率欄位
            # 常見格式：日期、幣別、現金買入、現金賣出、即期買入、即期賣出
            # 或：掛牌日期、本行買入、幣別、本行賣出、本行買入、本行賣出...
            cash_buy_col = None
            cash_sell_col = None
            spot_buy_col = None
            spot_sell_col = None
            
            # 根據實際數據結構識別欄位
            # 實際結構是：
            # 索引 0: 日期
            # 索引 1: 幣別名稱（美金 (USD)）
            # 索引 2: 現金買入（數值）
            # 索引 3: 現金賣出（數值）
            # 索引 4: 即期買入（數值）
            # 索引 5: 即期賣出（數值）
            # 索引 6-8: 空的（NaN）
            
            # 根據實際數據結構，使用位置判斷（因為欄位名稱可能不準確）
            for idx, col in enumerate(df.columns):
                col_str = str(col)
                # 跳過日期和幣別欄位
                if idx == date_col_idx or idx == currency_col_idx:
                    continue
                
                # 如果欄位名稱包含「掛牌日期」，也應該跳過（索引 1 是幣別名稱）
                if '掛牌日期' in col_str:
                    continue
                
                # 根據實際數據結構，使用位置判斷
                if currency_col_idx == 2:
                    if idx == 2 and not cash_buy_col:
                        # 索引 2 是現金買入（雖然欄位名稱是「幣別_幣別」）
                        cash_buy_col = col
                    elif idx == 3 and not cash_sell_col:
                        # 索引 3 是現金賣出
                        cash_sell_col = col
                    elif idx == 4 and not spot_buy_col:
                        # 索引 4 是即期買入（雖然欄位名稱是「現金匯率_本行買入」）
                        spot_buy_col = col
                    elif idx == 5 and not spot_sell_col:
                        # 索引 5 是即期賣出（雖然欄位名稱是「現金匯率_本行賣出」）
                        spot_sell_col = col
                
                # 如果還沒識別，嘗試根據欄位名稱
                if '現金' in col_str:
                    if ('買入' in col_str or '本行買入' in col_str) and not cash_buy_col:
                        cash_buy_col = col
                    elif ('賣出' in col_str or '本行賣出' in col_str) and not cash_sell_col:
                        cash_sell_col = col
                elif '即期' in col_str:
                    if ('買入' in col_str or '本行買入' in col_str) and not spot_buy_col:
                        spot_buy_col = col
                    elif ('賣出' in col_str or '本行賣出' in col_str) and not spot_sell_col:
                        spot_sell_col = col
            
            # 如果無法透過名稱識別，根據位置推斷
            if not cash_buy_col or not cash_sell_col or not spot_buy_col or not spot_sell_col:
                if len(df.columns) >= 6 and currency_col_idx == 2:
                    # 格式：日期(0)、本行買入(1)、幣別(2)、本行賣出(3)、本行買入(4)、本行賣出(5)
                    # 通常：索引1是現金買入，索引3是現金賣出，索引4是即期買入，索引5是即期賣出
                    if not cash_buy_col and len(df.columns) > 1:
                        cash_buy_col = df.columns[1]
                    if not cash_sell_col and len(df.columns) > 3:
                        cash_sell_col = df.columns[3]
                    if not spot_buy_col and len(df.columns) > 4:
                        spot_buy_col = df.columns[4]
                    if not spot_sell_col and len(df.columns) > 5:
                        spot_sell_col = df.columns[5]
                elif len(df.columns) >= 6:
                    # 如果幣別不在索引 2，嘗試其他位置
                    # 假設：日期(0)、現金買入(1)、現金賣出(2)、即期買入(3)、即期賣出(4)
                    if not cash_buy_col and len(df.columns) > 1:
                        cash_buy_col = df.columns[1]
                    if not cash_sell_col and len(df.columns) > 2:
                        cash_sell_col = df.columns[2]
                    if not spot_buy_col and len(df.columns) > 3:
                        spot_buy_col = df.columns[3]
                    if not spot_sell_col and len(df.columns) > 4:
                        spot_sell_col = df.columns[4]
            
            # 建立新的 DataFrame，只包含需要的欄位
            # 使用位置索引而不是欄位名稱，避免重複欄位名稱的問題
            selected_indices = []
            new_col_names = []
            
            if date_col:
                date_idx = list(df.columns).index(date_col)
                selected_indices.append(date_idx)
                new_col_names.append("日期")
            
            if cash_buy_col:
                cash_buy_idx = list(df.columns).index(cash_buy_col)
                selected_indices.append(cash_buy_idx)
                new_col_names.append("現金買入")
            
            if cash_sell_col:
                cash_sell_idx = list(df.columns).index(cash_sell_col)
                selected_indices.append(cash_sell_idx)
                new_col_names.append("現金賣出")
            
            if spot_buy_col:
                spot_buy_idx = list(df.columns).index(spot_buy_col)
                selected_indices.append(spot_buy_idx)
                new_col_names.append("即期買入")
            
            if spot_sell_col:
                spot_sell_idx = list(df.columns).index(spot_sell_col)
                selected_indices.append(spot_sell_idx)
                new_col_names.append("即期賣出")
            
            # 確保選取的欄位索引和名稱數量一致
            if len(selected_indices) != len(new_col_names):
                # 使用位置推斷作為備用方案
                if len(df.columns) >= 6 and currency_col_idx == 2:
                    df = df.iloc[:, [0, 2, 3, 4, 5]].copy()
                    df.columns = ["日期", "現金買入", "現金賣出", "即期買入", "即期賣出"]
                elif len(df.columns) >= 5:
                    df = df.iloc[:, [0, 1, 2, 3, 4]].copy()
                    df.columns = ["日期", "現金買入", "現金賣出", "即期買入", "即期賣出"]
                else:
                    print(f"錯誤: 欄位數量不足: {len(df.columns)}")
                    return None
            elif selected_indices:
                # 使用位置索引選取欄位（避免重複欄位名稱的問題）
                df = df.iloc[:, selected_indices].copy()
                
                # 確保選取後的欄位數量和名稱數量一致
                if len(df.columns) != len(new_col_names):
                    # 使用位置推斷作為備用方案
                    if len(df.columns) >= 6 and currency_col_idx == 2:
                        df = df.iloc[:, [0, 2, 3, 4, 5]].copy()
                        df.columns = ["日期", "現金買入", "現金賣出", "即期買入", "即期賣出"]
                    else:
                        return None
                else:
                    df.columns = new_col_names
            else:
                # 如果找不到特定欄位，使用位置推斷（排除幣別欄位）
                if len(df.columns) >= 6 and currency_col_idx == 2:
                    df = df.iloc[:, [0, 2, 3, 4, 5]].copy()
                    df.columns = ["日期", "現金買入", "現金賣出", "即期買入", "即期賣出"]
                elif len(df.columns) >= 5:
                    df = df.iloc[:, [0, 1, 2, 3, 4]].copy()
                    df.columns = ["日期", "現金買入", "現金賣出", "即期買入", "即期賣出"]
                else:
                    print(f"錯誤: 欄位數量不足: {len(df.columns)}")
                    return None
                    
        elif query_type == 'day':
            # 單日查詢的欄位處理
            if len(df.columns) >= 2:
                df = df.iloc[:, :2].copy()
                df.columns = ["類型", "金額"]
            else:
                df.columns = ["類型", "金額"]
        
        return df
            
    except ValueError as e:
        print(f"錯誤: 參數錯誤: {e}")
        return None
    except requests.RequestException as e:
        print(f"錯誤: 請求失敗: {e}")
        return None
    except Exception as e:
        print(f"錯誤: 發生錯誤: {e}")
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="查詢台灣銀行匯率資料")
    parser.add_argument("--type", choices=["current", "historical"], default="current",
                       help="查詢類型：current (即時) 或 historical (歷史)")
    parser.add_argument("--query-type", choices=["ltm", "l6m", "month", "day"], default="l6m",
                       help="歷史查詢類型：ltm (近3個月), l6m (近6個月), month (單月), day (單日)")
    parser.add_argument("--date", type=str,
                       help="日期參數：month 查詢使用 'YYYY-MM'，day 查詢使用 'YYYY-MM-DD'")
    parser.add_argument("--rate-type", choices=["spot", "cash"], default="spot",
                       help="匯率類型：spot (即期) 或 cash (現金)，僅在 day 查詢時使用")
    parser.add_argument("--currency", type=str, default="USD", help="幣別代碼，預設為 USD")
    parser.add_argument("--output", choices=["json", "csv", "table"], default="table",
                       help="輸出格式：json, csv 或 table (表格格式)")
    parser.add_argument("--limit", type=int, help="限制顯示筆數")
    
    args = parser.parse_args()
    
    if args.type == "current":
        # 查詢即時匯率
        result = fetch_usd_rate()
        if result:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print("無法取得匯率資訊")
    elif args.type == "historical":
        # 歷史匯率查詢
        result = fetch_bot_rates(
            currency=args.currency,
            query_type=args.query_type,
            date=args.date,
            rate_type=args.rate_type
        )
        
        if result is None:
            print("無法取得歷史匯率資訊")
        else:
            # pandas DataFrame 輸出
            if args.limit:
                result = result.head(args.limit)
            
            if args.output == "json":
                print(result.to_json(orient="records", force_ascii=False, indent=2))
            elif args.output == "csv":
                print(result.to_csv(index=False))
            else:
                # 預設表格格式
                print(result.to_string(index=False))

