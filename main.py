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

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Welcome to {bot_name}! Please choose a stock:",
                                    reply_markup=stock_menu_keyboard())

# Main menu keyboard
def stock_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("AAPL", callback_data='AAPL')],
        [InlineKeyboardButton("GOOGL", callback_data='GOOGL')],
        [InlineKeyboardButton("MSFT", callback_data='MSFT')],
    ]
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
        [InlineKeyboardButton("1 Day", callback_data=f'{stock_symbol}_1d')],
        [InlineKeyboardButton("1 Week", callback_data=f'{stock_symbol}_1w')],
        [InlineKeyboardButton("1 Month", callback_data=f'{stock_symbol}_1m')],
    ]
    return InlineKeyboardMarkup(keyboard)

# Fetch and display stock data
async def fetch_stock_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    stock_symbol, duration = query.data.split('_')
    
    if duration == '1d':
        function = 'TIME_SERIES_INTRADAY'
        interval = '60min'
    elif duration == '1w':
        function = 'TIME_SERIES_DAILY'
    elif duration == '1m':
        function = 'TIME_SERIES_DAILY'
    
    params = {
        "function": function,
        "symbol": stock_symbol,
        "apikey": stock_api_key
    }
    
    if duration == '1d':
        params['interval'] = interval
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Error Message" in data:
        await query.edit_message_text("Invalid API call. Please try again later.")
        return

    if duration == '1d':
        time_series = data['Time Series (60min)']
    else:
        time_series = data['Time Series (Daily)']
    
    recent_date = list(time_series.keys())[0]
    recent_data = time_series[recent_date]
    high = recent_data['2. high']
    low = recent_data['3. low']
    close = recent_data['4. close']

    message = (f"Stock: {stock_symbol}\n"
               f"Date: {recent_date}\n"
               f"High: {high}\n"
               f"Low: {low}\n"
               f"Close: {close}")
    
    await query.edit_message_text(message)
    await query.message.reply_text("Choose another stock:", reply_markup=stock_menu_keyboard())

def main():
    # Create the application
    application = Application.builder().token(bot_token).build()

    print("Bot is starting...")

    # Handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(stock_selection, pattern='^(AAPL|GOOGL|MSFT)$'))
    application.add_handler(CallbackQueryHandler(fetch_stock_data, pattern='^(AAPL|GOOGL|MSFT)_(1d|1w|1m)$'))

    # Run the bot
    print("Polling...")
    application.run_polling()

if __name__ == "__main__":
    main()
