# 變更紀錄

所有重要的專案變更都會記錄在這個檔案中。

## [0.1.0] - 2025-01-17

### 新增
- 重構專案為標準 Python 套件結構
- 建立 `TaiwanBankFXClient` 類別作為主要 API 介面
- 新增完整的例外處理機制（`RequestError`, `ParseError`, `InvalidParameterError`）
- 新增命令列工具 `twbank-fx`
- 建立三個完整的範例程式：
  - `basic_usage.py` - 基本使用範例
  - `currency_converter.py` - 貨幣轉換器
  - `rate_monitor.py` - 匯率監控器
- 支援 Context Manager 用法
- 新增完整的 API 文件
- 建立 setup.py 以支援 pip 安裝
- 新增 MIT 授權條款
- 建立完整的 README.md 說明文件

### 改進
- 優化 HTTP 請求處理，加入 Session 管理
- 改進錯誤處理機制
- 優化資料解析邏輯
- 加入自定義 User-Agent
- 改進歷史匯率欄位名稱處理

### 文件
- 建立完整的 README.md
- 新增詳細的 API 文件
- 提供豐富的使用範例
- 新增命令列工具使用說明

## [舊版本]

### 原始版本
- 基本的匯率查詢功能
- 支援即時匯率和歷史匯率查詢
- 簡單的命令列介面
