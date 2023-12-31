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
from pathlib import Path
from typing import Annotated

import keyring
from fastapi import Body, FastAPI
from fugle_trade.constant import Action, APCode, BSFlag, PriceFlag, Trade
from fugle_trade.order import OrderObject
from fugle_trade.sdk import SDK
from keyrings.cryptfile.cryptfile import CryptFileKeyring


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


# --- FastAPI server ---

app = FastAPI()

@app.post("/place_order")
async def place_order(
    buy_sell: Annotated[Action, Body()],
    price: Annotated[float, Body()],
    stock_no: Annotated[str, Body()],
    quantity: Annotated[int, Body()],
    ap_code: Annotated[APCode, Body()] = APCode.Common,
    bs_flag: Annotated[BSFlag, Body()] = BSFlag.ROD,
    price_flag: Annotated[PriceFlag, Body()] = PriceFlag.Limit,
    trade: Annotated[Trade, Body()] = Trade.Cash,
):
    try:
        return FugleTrading.sdk.place_order(
            OrderObject(
                buy_sell=buy_sell,
                price=price,
                stock_no=stock_no,
                quantity=quantity,
                ap_code=ap_code,
                bs_flag=bs_flag,
                price_flag=price_flag,
                trade=trade,
            )
        )
    except (ValueError, TypeError) as e:
        return {"error": str(e)}
