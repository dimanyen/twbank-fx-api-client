# Taiwan Bank FX API Client

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple and easy-to-use Python client for querying real-time and historical foreign exchange rates from Bank of Taiwan.

[中文說明](./README.md) | English

## Features

- **Real-time Exchange Rates**: Query current exchange rates for various currencies from Bank of Taiwan
- **Historical Rates**: Support for querying rates from the last 3 months, 6 months, specific months, or specific dates
- **Multiple Currencies**: Support for USD, EUR, JPY, GBP, and many other common currencies
- **Flexible Output**: Export data in JSON, CSV, or table format
- **Comprehensive Error Handling**: Detailed exception classes for easier error management
- **Pandas DataFrame Support**: Historical data returned as DataFrame for easy data analysis
- **Command-Line Tool**: Built-in CLI tool for querying rates directly from terminal
- **Context Manager Support**: Use with Python's `with` statement for automatic resource management

## Installation

### Install from GitHub

```bash
pip install git+https://github.com/dimanyen/twbank-fx-api-client.git
```

### Install from Source

```bash
git clone https://github.com/dimanyen/twbank-fx-api-client.git
cd twbank-fx-api-client
pip install -e .
```

## Quick Start

### Python API

```python
from twbank_fx_client import TaiwanBankFXClient

# Create client
client = TaiwanBankFXClient()

# Query current USD rate
usd_rate = client.get_current_rate("USD")
print(f"USD Spot Buy: {usd_rate['spot_buy']}")
print(f"USD Spot Sell: {usd_rate['spot_sell']}")

# Query historical rates for the last 6 months
df = client.get_historical_rates("USD", period="l6m")
print(df.head())
```

### Command-Line Tool

Query current rate:

```bash
twbank-fx --type current --currency USD
```

Query historical rates:

```bash
twbank-fx --type historical --currency EUR --period l6m --output table
```

Query specific month:

```bash
twbank-fx --type historical --currency JPY --period month --date 2025-01
```

## Usage Guide

### Query Current Rates

```python
from twbank_fx_client import TaiwanBankFXClient

client = TaiwanBankFXClient()

# Query USD rate
usd_rate = client.get_current_rate("USD")

# Returned data structure
{
    "currency": "USD",
    "currency_name": "美金 (USD)",
    "cash_buy": "31.235",      # Cash buying rate
    "cash_sell": "32.035",     # Cash selling rate
    "spot_buy": "31.635",      # Spot buying rate
    "spot_sell": "31.735",     # Spot selling rate
    "timestamp": "2025-01-15 10:30:00"
}
```

### Query Historical Rates

```python
# Query rates for the last 6 months
df = client.get_historical_rates("USD", period="l6m")

# Query rates for the last 3 months
df = client.get_historical_rates("EUR", period="ltm")

# Query rates for a specific month
df = client.get_historical_rates("JPY", period="month", date="2025-01")

# Query rates for a specific date
df = client.get_historical_rates("GBP", period="day", date="2025-01-15", rate_type="spot")
```

### Use Context Manager

```python
# Automatic resource management with 'with' statement
with TaiwanBankFXClient() as client:
    rate = client.get_current_rate("USD")
    print(rate)
```

### Error Handling

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
    print(f"Request error: {e}")
except ParseError as e:
    print(f"Parse error: {e}")
except TaiwanBankFXError as e:
    print(f"General error: {e}")
```

## Supported Currencies

- USD - US Dollar
- EUR - Euro
- JPY - Japanese Yen
- GBP - British Pound
- AUD - Australian Dollar
- CAD - Canadian Dollar
- SGD - Singapore Dollar
- CHF - Swiss Franc
- HKD - Hong Kong Dollar
- CNY - Chinese Yuan
- ZAR - South African Rand
- SEK - Swedish Krona
- NZD - New Zealand Dollar
- THB - Thai Baht
- KRW - Korean Won

For more currencies, please refer to the [Bank of Taiwan Exchange Rate website](https://rate.bot.com.tw/xrt?Lang=en-US).

## Example Programs

The project includes complete example programs in the [examples](./examples) directory:

### 1. Basic Usage ([basic_usage.py](./examples/basic_usage.py))

Demonstrates how to query current rates, historical rates, and perform basic data analysis.

```bash
python examples/basic_usage.py
```

### 2. Currency Converter ([currency_converter.py](./examples/currency_converter.py))

Shows how to build a simple currency converter and calculate exchange rate spreads.

```bash
python examples/currency_converter.py
```

### 3. Rate Monitor ([rate_monitor.py](./examples/rate_monitor.py))

Demonstrates how to monitor exchange rate changes and set alert thresholds.

```bash
python examples/rate_monitor.py
```

## Command-Line Tool

The `twbank-fx` command-line tool is automatically installed with the package.

### Query Current Rates

```bash
# Query current USD rate (default: table format)
twbank-fx --type current --currency USD

# Output in JSON format
twbank-fx --type current --currency EUR --output json
```

### Query Historical Rates

```bash
# Query USD rates for the last 6 months
twbank-fx --type historical --currency USD --period l6m

# Query EUR rates for the last 3 months
twbank-fx --type historical --currency EUR --period ltm

# Query JPY rates for a specific month
twbank-fx --type historical --currency JPY --period month --date 2025-01

# Output in CSV format
twbank-fx --type historical --currency USD --period l6m --output csv

# Limit number of results
twbank-fx --type historical --currency USD --period l6m --limit 10
```

### Complete Command-Line Arguments

```bash
usage: twbank-fx [-h] [--type {current,historical}] [--currency CURRENCY]
                 [--period {ltm,l6m,month,day}] [--date DATE]
                 [--rate-type {spot,cash}] [--output {json,csv,table}]
                 [--limit LIMIT] [--timeout TIMEOUT]

options:
  -h, --help            Show help message
  --type {current,historical}
                        Query type: current (real-time) or historical
  --currency CURRENCY   Currency code, default is USD
  --period {ltm,l6m,month,day}
                        Historical query period: ltm (last 3 months), l6m (last 6 months),
                        month (single month), day (single day)
  --date DATE           Date parameter: 'YYYY-MM' for month query, 'YYYY-MM-DD' for day query
  --rate-type {spot,cash}
                        Rate type: spot or cash, used only for day query
  --output {json,csv,table}
                        Output format: json, csv, or table
  --limit LIMIT         Limit number of results (for historical queries only)
  --timeout TIMEOUT     Request timeout in seconds, default is 10 seconds
```

## API Documentation

### TaiwanBankFXClient

Main client class for querying Bank of Taiwan exchange rates.

#### Initialization

```python
client = TaiwanBankFXClient(timeout=10)
```

**Parameters:**
- `timeout` (int): Request timeout in seconds, default is 10 seconds

#### get_current_rate()

Query current exchange rate for a specific currency.

```python
rate = client.get_current_rate(currency="USD")
```

**Parameters:**
- `currency` (str): Currency code, e.g., 'USD', 'EUR', 'JPY'

**Returns:**
- `dict`: Dictionary containing rate information

**Raises:**
- `RequestError`: When request fails
- `ParseError`: When data parsing fails

#### get_historical_rates()

Query historical exchange rate data.

```python
df = client.get_historical_rates(
    currency="USD",
    period="l6m",
    date=None,
    rate_type="spot"
)
```

**Parameters:**
- `currency` (str): Currency code
- `period` (str): Query period ('ltm', 'l6m', 'month', 'day')
- `date` (str, optional): Date parameter (format: 'YYYY-MM' or 'YYYY-MM-DD')
- `rate_type` (str): Rate type ('spot' or 'cash')

**Returns:**
- `pandas.DataFrame`: DataFrame containing historical rate data

**Raises:**
- `InvalidParameterError`: When parameters are invalid
- `RequestError`: When request fails
- `ParseError`: When data parsing fails

## Exception Classes

### TaiwanBankFXError

Base exception class. All other exception classes inherit from this class.

### RequestError

Raised when HTTP request fails.

### ParseError

Raised when parsing returned data fails.

### InvalidParameterError

Raised when provided parameters are invalid.

## Important Notes

1. **Rate Update Frequency**: Bank of Taiwan's rate data is updated periodically. Please avoid querying too frequently to prevent server overload.
2. **Network Connection**: This package requires an internet connection to function properly.
3. **Data Source**: All rate data comes from the official Bank of Taiwan website.
4. **Rate Types Explained**:
   - **Cash Rate**: Applies to physical cash transactions
   - **Spot Rate**: Applies to foreign currency deposits, remittances, etc.
   - **Buying Rate**: Rate at which the bank buys foreign currency (customer sells)
   - **Selling Rate**: Rate at which the bank sells foreign currency (customer buys)

## Project Structure

```
twbank-fx-api-client/
├── twbank_fx_client/         # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Client implementation
│   ├── cli.py                # Command-line tool
│   └── exceptions.py         # Exception class definitions
├── examples/                  # Example programs
│   ├── basic_usage.py        # Basic usage examples
│   ├── currency_converter.py # Currency converter example
│   └── rate_monitor.py       # Rate monitor example
├── setup.py                   # Package configuration
├── requirements.txt           # Dependencies
├── LICENSE                    # License
├── .gitignore                # Git ignore list
├── README.md                 # Documentation (Chinese)
└── README.en.md              # Documentation (English)
```

## Development

### Setup Development Environment

```bash
# Clone the project
git clone https://github.com/dimanyen/twbank-fx-api-client.git
cd twbank-fx-api-client

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### Run Examples

```bash
# Run basic usage example
python examples/basic_usage.py

# Run currency converter example
python examples/currency_converter.py

# Run rate monitor example
python examples/rate_monitor.py
```

## Dependencies

- Python >= 3.7
- requests >= 2.31.0
- beautifulsoup4 >= 4.12.0
- lxml >= 4.9.0
- pandas >= 2.0.0
- html5lib >= 1.1

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Issues and Pull Requests are welcome!

## Disclaimer

This package is for educational and personal use only. All exchange rate data comes from the official Bank of Taiwan website. Users should verify the accuracy of rate data themselves. The author is not responsible for any losses resulting from the use of this package.

## Related Links

- [Bank of Taiwan Exchange Rates](https://rate.bot.com.tw/xrt?Lang=en-US)
- [Bank of Taiwan](https://www.bot.com.tw/)

## Changelog

### v0.1.0 (2025-01-17)

- Initial release
- Support for current rate queries
- Support for historical rate queries
- Command-line tool included
- Complete example programs provided
