# RealTimeMarketBot

A Telegram bot for fetching and displaying real-time stock market data. Users can select stocks and view their latest performance based on different time intervals.

## Features

- Select from a variety of popular stock symbols.
- Fetch stock data for intervals such as 1 minute, 5 minutes, 15 minutes, 30 minutes, 60 minutes, daily, weekly, and monthly.
- Interactive inline keyboard for easy navigation.

## Requirements

- Python 3.8+
- The following Python packages:
  - `python-telegram-bot`
  - `requests`
  - `configparser`

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/THEFZNKHAN/RealTimeMarketBot
   cd RealTimeMarketBot
    ```
2. **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Configure the bot:**
    - Create a configuration file config/config.ini with the following content
    ```bash
    [TelegramAPI]
    bot_token = YOUR_TELEGRAM_BOT_TOKEN
    bot_name = YOUR_BOT_NAME

    [StockAPI]
    api_key = YOUR_ALPHA_VANTAGE_API_KEY
    stock_url = https://www.alphavantage.co/query
    ```
5. **Running the Bot:**
    ```bash
    python -m main.py
    ```

## Contributing

Feel free to submit issues, fork the repository, and send pull requests. We welcome contributions from the community!

## Live Demo

[RealTimeMarketBot](https://t.me/RealTimeMarketBot)