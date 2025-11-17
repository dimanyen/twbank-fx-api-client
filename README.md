# Taiwan Bank FX API Client

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

台灣銀行外匯匯率查詢 API 客戶端 - 一個簡單易用的 Python 套件，用於查詢台灣銀行的即時匯率和歷史匯率資料。

中文說明 | [English](./README.en.md)

## 特色功能

- **即時匯率查詢**：查詢台灣銀行提供的各種外幣即時匯率
- **歷史匯率查詢**：支援查詢最近三個月、六個月、特定月份或特定日期的歷史匯率
- **多幣別支援**：支援美金、歐元、日圓、英鎊等多種常見外幣
- **資料格式靈活**：可輸出為 JSON、CSV 或表格格式
- **完整的錯誤處理**：提供詳細的例外類別，方便錯誤處理
- **支援 Pandas DataFrame**：歷史匯率資料以 DataFrame 格式回傳，便於進行資料分析
- **命令列工具**：提供 CLI 工具，可直接在終端機中查詢匯率

## 安裝

### 使用 pip 安裝（從 GitHub）

```bash
pip install git+https://github.com/dimanyen/twbank-fx-api-client.git
```

### 從原始碼安裝

```bash
git clone https://github.com/dimanyen/twbank-fx-api-client.git
cd twbank-fx-api-client
pip install -e .
```

## 快速開始

### Python API 使用

```python
from twbank_fx_client import TaiwanBankFXClient

# 建立客戶端
client = TaiwanBankFXClient()

# 查詢美金即時匯率
usd_rate = client.get_current_rate("USD")
print(f"美金即期買入: {usd_rate['spot_buy']}")
print(f"美金即期賣出: {usd_rate['spot_sell']}")

# 查詢最近六個月的歷史匯率
df = client.get_historical_rates("USD", period="l6m")
print(df.head())
```

### 命令列工具使用

查詢即時匯率：

```bash
twbank-fx --type current --currency USD
```

查詢歷史匯率：

```bash
twbank-fx --type historical --currency EUR --period l6m --output table
```

查詢特定月份匯率：

```bash
twbank-fx --type historical --currency JPY --period month --date 2025-01
```

## 詳細使用說明

### 查詢即時匯率

```python
from twbank_fx_client import TaiwanBankFXClient

client = TaiwanBankFXClient()

# 查詢美金匯率
usd_rate = client.get_current_rate("USD")

# 回傳的資料結構
{
    "currency": "USD",
    "currency_name": "美金 (USD)",
    "cash_buy": "31.235",      # 現金買入匯率
    "cash_sell": "32.035",     # 現金賣出匯率
    "spot_buy": "31.635",      # 即期買入匯率
    "spot_sell": "31.735",     # 即期賣出匯率
    "timestamp": "2025-01-15 10:30:00"
}
```

### 查詢歷史匯率

```python
# 查詢最近六個月的匯率
df = client.get_historical_rates("USD", period="l6m")

# 查詢最近三個月的匯率
df = client.get_historical_rates("EUR", period="ltm")

# 查詢特定月份的匯率
df = client.get_historical_rates("JPY", period="month", date="2025-01")

# 查詢特定日期的匯率
df = client.get_historical_rates("GBP", period="day", date="2025-01-15", rate_type="spot")
```

### 使用 Context Manager

```python
# 使用 with 語句自動管理資源
with TaiwanBankFXClient() as client:
    rate = client.get_current_rate("USD")
    print(rate)
```

### 錯誤處理

```python
from twbank_fx_client import TaiwanBankFXClient
from twbank_fx_client.exceptions import (
    TaiwanBankFXError,
    RequestError,
    ParseError,
    InvalidParameterError
)

client = TaiwanBankFXClient()

try:
    rate = client.get_current_rate("USD")
except RequestError as e:
    print(f"請求錯誤: {e}")
except ParseError as e:
    print(f"解析錯誤: {e}")
except TaiwanBankFXError as e:
    print(f"一般錯誤: {e}")
```

## 支援的幣別

- USD - 美金
- EUR - 歐元
- JPY - 日圓
- GBP - 英鎊
- AUD - 澳幣
- CAD - 加拿大幣
- SGD - 新加坡幣
- CHF - 瑞士法郎
- HKD - 港幣
- CNY - 人民幣
- ZAR - 南非幣
- SEK - 瑞典幣
- NZD - 紐西蘭幣
- THB - 泰幣
- KRW - 韓元

更多幣別請參考[台灣銀行牌告匯率網站](https://rate.bot.com.tw/xrt?Lang=zh-TW)。

## 範例程式

專案包含完整的範例程式，位於 [examples](./examples) 目錄：

### 1. 基本使用範例 ([basic_usage.py](./examples/basic_usage.py))

展示如何查詢即時匯率、歷史匯率，以及進行基本的資料分析。

```bash
python examples/basic_usage.py
```

### 2. 貨幣轉換器 ([currency_converter.py](./examples/currency_converter.py))

展示如何建立一個簡單的貨幣轉換器，計算匯率價差。

```bash
python examples/currency_converter.py
```

### 3. 匯率監控器 ([rate_monitor.py](./examples/rate_monitor.py))

展示如何監控匯率變化，並設定警示門檻。

```bash
python examples/rate_monitor.py
```

## 命令列工具

安裝後會自動安裝 `twbank-fx` 命令列工具。

### 查詢即時匯率

```bash
# 查詢美金即時匯率（預設為表格格式）
twbank-fx --type current --currency USD

# 以 JSON 格式輸出
twbank-fx --type current --currency EUR --output json
```

### 查詢歷史匯率

```bash
# 查詢最近六個月的美金匯率
twbank-fx --type historical --currency USD --period l6m

# 查詢最近三個月的歐元匯率
twbank-fx --type historical --currency EUR --period ltm

# 查詢特定月份的日圓匯率
twbank-fx --type historical --currency JPY --period month --date 2025-01

# 以 CSV 格式輸出
twbank-fx --type historical --currency USD --period l6m --output csv

# 限制顯示筆數
twbank-fx --type historical --currency USD --period l6m --limit 10
```

### 完整的命令列參數

```bash
usage: twbank-fx [-h] [--type {current,historical}] [--currency CURRENCY]
                 [--period {ltm,l6m,month,day}] [--date DATE]
                 [--rate-type {spot,cash}] [--output {json,csv,table}]
                 [--limit LIMIT] [--timeout TIMEOUT]

options:
  -h, --help            顯示幫助訊息
  --type {current,historical}
                        查詢類型：current (即時匯率) 或 historical (歷史匯率)
  --currency CURRENCY   幣別代碼，預設為 USD
  --period {ltm,l6m,month,day}
                        歷史查詢期間：ltm (近3個月), l6m (近6個月), month (單月), day (單日)
  --date DATE           日期參數：month 查詢使用 'YYYY-MM'，day 查詢使用 'YYYY-MM-DD'
  --rate-type {spot,cash}
                        匯率類型：spot (即期) 或 cash (現金)，僅在 day 查詢時使用
  --output {json,csv,table}
                        輸出格式：json, csv 或 table (表格格式)
  --limit LIMIT         限制顯示筆數（僅適用於歷史查詢）
  --timeout TIMEOUT     請求超時時間（秒），預設為 10 秒
```

## API 文件

### TaiwanBankFXClient

主要的客戶端類別，用於查詢台灣銀行匯率。

#### 初始化

```python
client = TaiwanBankFXClient(timeout=10)
```

**參數:**
- `timeout` (int): 請求超時時間（秒），預設為 10 秒

#### get_current_rate()

查詢指定幣別的即時匯率。

```python
rate = client.get_current_rate(currency="USD")
```

**參數:**
- `currency` (str): 幣別代碼，如 'USD'、'EUR'、'JPY' 等

**回傳:**
- `dict`: 包含匯率資訊的字典

**例外:**
- `RequestError`: 當請求失敗時
- `ParseError`: 當解析資料失敗時

#### get_historical_rates()

查詢歷史匯率資料。

```python
df = client.get_historical_rates(
    currency="USD",
    period="l6m",
    date=None,
    rate_type="spot"
)
```

**參數:**
- `currency` (str): 幣別代碼
- `period` (str): 查詢期間（'ltm', 'l6m', 'month', 'day'）
- `date` (str, optional): 日期參數（格式：'YYYY-MM' 或 'YYYY-MM-DD'）
- `rate_type` (str): 匯率類型（'spot' 或 'cash'）

**回傳:**
- `pandas.DataFrame`: 包含歷史匯率資料的 DataFrame

**例外:**
- `InvalidParameterError`: 當參數無效時
- `RequestError`: 當請求失敗時
- `ParseError`: 當解析資料失敗時

## 例外類別

### TaiwanBankFXError

基礎例外類別，所有其他例外類別都繼承自此類別。

### RequestError

當 HTTP 請求失敗時拋出。

### ParseError

當解析回傳的資料失敗時拋出。

### InvalidParameterError

當提供的參數無效時拋出。

## 注意事項

1. **匯率更新頻率**：台灣銀行的匯率資料會定期更新，建議不要過於頻繁地查詢，以免對伺服器造成負擔。
2. **網路連線**：此套件需要網路連線才能正常運作。
3. **資料來源**：所有匯率資料來自台灣銀行官方網站。
4. **匯率說明**：
   - **現金匯率**：適用於實體現鈔的買賣
   - **即期匯率**：適用於外匯存款、匯款等
   - **買入匯率**：銀行買入外幣的匯率（客戶賣出外幣）
   - **賣出匯率**：銀行賣出外幣的匯率（客戶買入外幣）

## 專案結構

```
twbank-fx-api-client/
├── twbank_fx_client/         # 主要套件目錄
│   ├── __init__.py           # 套件初始化
│   ├── client.py             # 客戶端實作
│   ├── cli.py                # 命令列工具
│   └── exceptions.py         # 例外類別定義
├── examples/                  # 範例程式
│   ├── basic_usage.py        # 基本使用範例
│   ├── currency_converter.py # 貨幣轉換器範例
│   └── rate_monitor.py       # 匯率監控範例
├── setup.py                   # 套件設定檔
├── requirements.txt           # 相依套件清單
├── LICENSE                    # 授權條款
├── .gitignore                # Git 忽略清單
└── README.md                 # 說明文件
```

## 開發

### 安裝開發環境

```bash
# Clone 專案
git clone https://github.com/yourusername/twbank-fx-api-client.git
cd twbank-fx-api-client

# 安裝相依套件
pip install -r requirements.txt

# 以開發模式安裝套件
pip install -e .
```

### 執行範例

```bash
# 執行基本使用範例
python examples/basic_usage.py

# 執行貨幣轉換器範例
python examples/currency_converter.py

# 執行匯率監控範例
python examples/rate_monitor.py
```

## 相依套件

- Python >= 3.7
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- pandas >= 2.0.0
- html5lib >= 1.1

## 授權條款

本專案採用 MIT 授權條款。詳見 [LICENSE](LICENSE) 檔案。

## 貢獻

歡迎提交 Issue 和 Pull Request！

## 免責聲明

本套件僅供學習和個人使用，所有匯率資料來自台灣銀行官方網站。使用者應自行確認匯率資料的正確性，作者不對任何因使用本套件而產生的損失負責。

## 相關連結

- [台灣銀行牌告匯率](https://rate.bot.com.tw/xrt?Lang=zh-TW)
- [台灣銀行](https://www.bot.com.tw/)

## 變更紀錄

### v0.1.0 (2025-11-17)

- 初始版本發布
- 支援即時匯率查詢
- 支援歷史匯率查詢
- 提供命令列工具
- 包含完整範例程式
