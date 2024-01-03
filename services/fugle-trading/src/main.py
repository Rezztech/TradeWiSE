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
from configparser import ConfigParser
from enum import Enum
from pathlib import Path

import fugle_trade.constant
import fugle_trade.order
import keyring
from fastapi import FastAPI
from fugle_trade.sdk import SDK
from keyrings.cryptfile.cryptfile import CryptFileKeyring
from pydantic import BaseModel


def get_env_or_raise(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise ValueError(f'Environment variable "{name}" not set')
    return value

fugle_trading_config_path = get_env_or_raise("FUGLE_TRADING_CONFIG")
fugle_trading_account_password = get_env_or_raise("FUGLE_TRADING_PASSWORD")
fugle_trading_cert_password = get_env_or_raise("FUGLE_TRADING_CERT_PASSWORD")
keyring_encryption_key = get_env_or_raise("KEYRING_ENCRYPTION_KEY")

_logger = logging.getLogger(__name__)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


# --- Fugle trading client ---

class FugleTrading:
    _singleton: FugleTrading | None = None
    _initailized: bool = False

    _sdk: SDK

    @classmethod
    @property
    def sdk(cls) -> SDK:
        return cls()._sdk

    def __new__(cls) -> FugleTrading:
        if cls._singleton is None:
            cls._singleton = super().__new__(cls)

        return cls._singleton

    def __init__(
        self,
        config_path: str = fugle_trading_config_path,
        keyring_key: str = keyring_encryption_key,
        account_password: str = fugle_trading_account_password,
        cert_password: str = fugle_trading_cert_password,
    ) -> None:
        if type(self)._initailized:
            return
        type(self)._initailized = True

        config = ConfigParser()
        if not config.read(config_path):
            raise FileNotFoundError(f'Failed to read "{config_path}"')
        # Resolve relative paths
        config["Cert"]["Path"] = str(
            Path(config_path).parent.joinpath(config["Cert"]["Path"]).resolve()
        )

        self.setup_crypt_file_keyring(keyring_key)
        keyring.set_password("fugle_trade_sdk:account", config["User"]["Account"], account_password)
        keyring.set_password("fugle_trade_sdk:cert", config["User"]["Account"], cert_password)

        self._sdk = SDK(config)
        self._sdk.login()

    @staticmethod
    def setup_crypt_file_keyring(keyring_key: str):
        """Setup the keyring as a encrypted file-based keyring with a custom encryption key"""

        _logger.info("Setting up keyring")

        kr = CryptFileKeyring()

        # Ensure a fresh new keyring file
        kr_file_path = Path(kr.file_path)
        if kr_file_path.exists():
            kr_file_path.unlink()

        kr.keyring_key = keyring_key

        # set as the global keyring
        keyring.set_keyring(kr)

class Action(str, Enum):
    BUY = "buy"
    SELL = "sell"

    def to_fugle(self) -> fugle_trade.constant.Action:
        return {
            self.BUY: fugle_trade.constant.Action.Buy,
            self.SELL: fugle_trade.constant.Action.Sell
        }[self]

class Market(str, Enum):
    COMMON = "common"
    """整股"""

    AFTER_MARKET = "afterMarket"
    """盤後"""

    ODD = "odd"
    """盤後零股"""

    EMG = "emerging"
    """興櫃"""

    INTRADAY_ODD = "intradayOdd"
    """盤中零股"""

    def to_fugle(self) -> fugle_trade.constant.APCode:
        return {
            self.COMMON: fugle_trade.constant.APCode.Common,
            self.AFTER_MARKET: fugle_trade.constant.APCode.AfterMarket,
            self.ODD: fugle_trade.constant.APCode.Odd,
            self.EMG: fugle_trade.constant.APCode.Emg,
            self.INTRADAY_ODD: fugle_trade.constant.APCode.IntradayOdd,
        }[self]

class ActionFlag(str, Enum):
    ROD = "ROD"
    """Rest of Day"""

    IOC = "IOC"
    """Immediate or cancel"""

    FOK = "FOK"
    """Fill or kill"""

    def to_fugle(self) -> fugle_trade.constant.BSFlag:
        return {
            self.ROD: fugle_trade.constant.BSFlag.ROD,
            self.IOC: fugle_trade.constant.BSFlag.IOC,
            self.FOK: fugle_trade.constant.BSFlag.FOK,
        }[self]

class PriceFlag(str, Enum):
    LIMIT = "limit"
    """限價"""

    FLAT = "flat"
    """平盤"""

    LIMIT_DOWN = "limitDown"
    """跌停"""

    LIMIT_UP = "limitUp"
    """漲停"""

    MARKET = "market"
    """市價"""

    def to_fugle(self) -> fugle_trade.constant.PriceFlag:
        return {
            self.LIMIT: fugle_trade.constant.PriceFlag.Limit,
            self.FLAT: fugle_trade.constant.PriceFlag.Flat,
            self.LIMIT_DOWN: fugle_trade.constant.PriceFlag.LimitDown,
            self.LIMIT_UP: fugle_trade.constant.PriceFlag.LimitUp,
            self.MARKET: fugle_trade.constant.PriceFlag.Market,
        }[self]

class TradeType(str, Enum):
    CASH = "cash"
    """現股"""

    MARGIN = "margin"
    """融資"""

    SHORT_SELL = "shortSell"
    """融券"""

    DAY_TRADING_SELL = "dayTradingSell"
    """現股當沖賣"""

    def to_fugle(self) -> fugle_trade.constant.Trade:
        return {
            self.CASH: fugle_trade.constant.Trade.Cash,
            self.MARGIN: fugle_trade.constant.Trade.Margin,
            self.SHORT_SELL: fugle_trade.constant.Trade.Short,
            self.DAY_TRADING_SELL: fugle_trade.constant.Trade.DayTradingSell,
        }[self]

class Order(BaseModel):
    action: Action
    price: float
    stock_no: str
    quantity: int
    market: Market = Market.COMMON
    action_flag: ActionFlag = ActionFlag.ROD
    price_flag: PriceFlag = PriceFlag.LIMIT
    trade_type: TradeType = TradeType.CASH

    def to_fugle(self) -> fugle_trade.order.OrderObject:
        return fugle_trade.order.OrderObject(
            buy_sell=self.action.to_fugle(),
            price=self.price,
            stock_no=self.stock_no,
            quantity=self.quantity,
            ap_code=self.market.to_fugle(),
            bs_flag=self.action_flag.to_fugle(),
            price_flag=self.price_flag.to_fugle(),
            trade=self.trade_type.to_fugle(),
        )


# --- FastAPI server ---

app = FastAPI()

@app.post("/place_order")
async def place_order(order: Order):
    try:
        return FugleTrading.sdk.place_order(order.to_fugle())
    except (ValueError, TypeError) as e:
        return {"error": str(e)}
