#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# TradeWiSE Project
#
# This file is part of the TradeWiSE project, an automated trading and financial analysis platform.
# It is licensed under the Mozilla Public License 2.0 (MPL 2.0), which allows for wide use and modification
# while ensuring that enhancements and modifications remain available to the community.
#
# You can find the MPL 2.0 license in the root directory of the project or at https://www.mozilla.org/MPL/2.0/.
#
# Copyright (c) 2023 by wildfootw <wildfootw@wildfoo.tw>
#

import logging
import os

import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_bot_auth_user_id = os.getenv('TELEGRAM_BOT_AUTH_USER_ID')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def is_user_authorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != int(telegram_bot_auth_user_id):
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return False
    return True

async def get_stock_price(symbol: str):
    response = requests.get(f'http://fugle-market-data:80/price/{symbol}')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'Unable to fetch data'}

# Define command handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_authorized(update, context):
        return
    await update.message.reply_text("Welcome to TradeWiSE! Your trading assistant.")

async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_user_authorized(update, context):
        return
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
