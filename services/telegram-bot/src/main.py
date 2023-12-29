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
from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, cast

import requests
from telegram import Bot, BotCommand, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

if TYPE_CHECKING:
    from telegram.ext import Application


def get_env_or_raise(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f'Environment variable "{name}" not set')
    return value

telegram_bot_token = get_env_or_raise('TELEGRAM_BOT_TOKEN')
telegram_bot_auth_user_id = get_env_or_raise('TELEGRAM_BOT_AUTH_USER_ID')

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class _BaseCommand:
    command: str
    description: str

    def to_bot_command(self) -> BotCommand:
        return BotCommand(self.command, self.description)

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        ...

class StartCommand(_BaseCommand):
    command = "start"
    description = "Starts the bot"

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not await is_user_authorized(update, context):
            return
        await update.message.reply_text("Welcome to TradeWiSE! Your trading assistant.")

class StockCommand(_BaseCommand):
    command = "stock"
    description = "Get stock price"

    @staticmethod
    async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not await is_user_authorized(update, context):
            return
        args = context.args
        if not args:
            await update.message.reply_text("Please provide a stock symbol. Usage: /stock <symbol>")
            return
        symbol = args[0]
        data = await StockCommand.get_stock_price(symbol)
        await update.message.reply_text(str(data))

    @staticmethod
    async def get_stock_price(symbol: str):
        response = requests.get(f'http://fugle-market-data:80/price/{symbol}')
        if response.status_code == 200:
            return response.json()
        else:
            return {'error': 'Unable to fetch data'}

_commands: list[_BaseCommand] = [StartCommand(), StockCommand()]


async def is_user_authorized(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != int(telegram_bot_auth_user_id):
        await update.message.reply_text("Sorry, you are not authorized to use this bot.")
        return False
    return True

async def post_init(application: Application) -> None:
    await cast(Bot, application.bot).set_my_commands(
        [cmd.to_bot_command() for cmd in _commands]
    )

def main():
    application = ApplicationBuilder().token(telegram_bot_token).post_init(post_init).build()

    # Register handlers
    for cmd in _commands:
        application.add_handler(CommandHandler(cmd.command, cmd.handle))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()
