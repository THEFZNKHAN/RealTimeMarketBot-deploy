import configparser
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Load configuration
config = configparser.ConfigParser()
config.read("config/config.ini")
bot_token = config["TelegramAPI"]["bot_token"]
bot_name = config["TelegramAPI"]["bot_name"]
stock_api_key = config["StockAPI"]["api_key"]
BASE_URL = config["StockAPI"]["stock_url"]

# List of essential stocks
STOCKS = [
    "AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA",
    "JPM", "GS", "BAC", "WFC", "C", "JNJ", "PFE", "MRK", "UNH",
    "ABBV", "PG", "KO", "PEP", "NKE", "WMT", "XOM", "CVX", "COP",
    "BP", "RDS.A", "RDS.B", "DUK", "D", "NEE", "SO", "ED", "HD",
    "COST", "TGT", "T", "VZ", "CMCSA", "DIS", "NFLX"
]

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Welcome to {bot_name}! Please choose a stock:",
                                    reply_markup=stock_menu_keyboard())

# Main menu keyboard
def stock_menu_keyboard():
    keyboard = []
    for i in range(0, len(STOCKS), 3):
        row = [
            InlineKeyboardButton(STOCKS[i], callback_data=STOCKS[i]) if i < len(STOCKS) else None,
            InlineKeyboardButton(STOCKS[i+1], callback_data=STOCKS[i+1]) if i+1 < len(STOCKS) else None,
            InlineKeyboardButton(STOCKS[i+2], callback_data=STOCKS[i+2]) if i+2 < len(STOCKS) else None
        ]
        keyboard.append([btn for btn in row if btn is not None])
    return InlineKeyboardMarkup(keyboard)

# Callback query handler
async def stock_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    stock_symbol = query.data
    await query.edit_message_text(f"Selected {stock_symbol}. Choose a duration:",
                                  reply_markup=duration_menu_keyboard(stock_symbol))

# Duration menu keyboard
def duration_menu_keyboard(stock_symbol):
    keyboard = [
        [InlineKeyboardButton("1 minute", callback_data=f'{stock_symbol}_1min')],
        [InlineKeyboardButton("5 minutes", callback_data=f'{stock_symbol}_5min')],
        [InlineKeyboardButton("15 minutes", callback_data=f'{stock_symbol}_15min')],
        [InlineKeyboardButton("30 minutes", callback_data=f'{stock_symbol}_30min')],
        [InlineKeyboardButton("60 minutes", callback_data=f'{stock_symbol}_60min')],
        [InlineKeyboardButton("Daily", callback_data=f'{stock_symbol}_daily')],
        [InlineKeyboardButton("Weekly", callback_data=f'{stock_symbol}_weekly')],
        [InlineKeyboardButton("Monthly", callback_data=f'{stock_symbol}_monthly')],
    ]
    return InlineKeyboardMarkup(keyboard)

# Fetch and display stock data
async def fetch_stock_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    stock_symbol, duration = query.data.split('_')
    
    function_mapping = {
        "1min": "TIME_SERIES_INTRADAY",
        "5min": "TIME_SERIES_INTRADAY",
        "15min": "TIME_SERIES_INTRADAY",
        "30min": "TIME_SERIES_INTRADAY",
        "60min": "TIME_SERIES_INTRADAY",
        "daily": "TIME_SERIES_DAILY",
        "weekly": "TIME_SERIES_WEEKLY",
        "monthly": "TIME_SERIES_MONTHLY"
    }
    
    interval_mapping = {
        "1min": "1min",
        "5min": "5min",
        "15min": "15min",
        "30min": "30min",
        "60min": "60min"
    }
    
    function = function_mapping[duration]
    params = {
        "function": function,
        "symbol": stock_symbol,
        "apikey": stock_api_key
    }
    
    if duration in interval_mapping:
        params["interval"] = interval_mapping[duration]
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Error Message" in data:
        await query.edit_message_text("Invalid API call. Please try again later.")
        return
    
    time_series_key = {
        "1min": "Time Series (1min)",
        "5min": "Time Series (5min)",
        "15min": "Time Series (15min)",
        "30min": "Time Series (30min)",
        "60min": "Time Series (60min)",
        "daily": "Time Series (Daily)",
        "weekly": "Weekly Time Series",
        "monthly": "Monthly Time Series"
    }[duration]
    
    time_series = data[time_series_key]
    recent_date = list(time_series.keys())[0]
    recent_data = time_series[recent_date]
    open_stock = recent_data['1. open']
    high = recent_data['2. high']
    low = recent_data['3. low']
    close = recent_data['4. close']
    volume = recent_data['5. volume']
    
    message = (f"Stock: {stock_symbol}\n"
               f"Date: {recent_date}\n"
               f"Open: {open_stock}\n"
               f"High: {high}\n"
               f"Low: {low}\n"
               f"Close: {close}\n"
               f"Volume: {volume}")
    
    await query.edit_message_text(message)
    await query.message.reply_text("Choose another stock:", reply_markup=stock_menu_keyboard())

def main():
    # Create the application
    app = Application.builder().token(bot_token).build()

    print("Bot is starting...")

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(stock_selection, pattern='^(AAPL|GOOGL|MSFT|AMZN|TSLA|META|NVDA|JPM|GS|BAC|WFC|C|JNJ|PFE|MRK|UNH|ABBV|PG|KO|PEP|NKE|WMT|XOM|CVX|COP|BP|RDS.A|RDS.B|DUK|D|NEE|SO|ED|HD|COST|TGT|T|VZ|CMCSA|DIS|NFLX)$'))
    app.add_handler(CallbackQueryHandler(fetch_stock_data, pattern='^(AAPL|GOOGL|MSFT|AMZN|TSLA|META|NVDA|JPM|GS|BAC|WFC|C|JNJ|PFE|MRK|UNH|ABBV|PG|KO|PEP|NKE|WMT|XOM|CVX|COP|BP|RDS.A|RDS.B|DUK|D|NEE|SO|ED|HD|COST|TGT|T|VZ|CMCSA|DIS|NFLX)_(1min|5min|15min|30min|60min|daily|weekly|monthly)$'))

    # Run the bot
    print("Polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
