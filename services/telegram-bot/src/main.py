#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyleft (ɔ) 2023 wildfootw <wildfootw@wildfoo.tw>
#
# Distributed under terms of the MIT license.

import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import os

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def get_stock_price(symbol: str):
    response = requests.get(f'http://fugle-market-data:80/price/{symbol}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Unable to fetch data'}

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to TradeWiSE! Your trading assistant.")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Please provide a stock symbol. Usage: /stock <symbol>")
        return
    symbol = args[0]
    data = await get_stock_price(symbol)
    await update.message.reply_text(str(data))

# Main function to setup the bot
#async def main():
if __name__ == '__main__':
    application = ApplicationBuilder().token(telegram_bot_token).build()

    # Register handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stock', stock))

    # Start the bot
    application.run_polling()
