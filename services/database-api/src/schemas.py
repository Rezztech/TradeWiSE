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

from pydantic import BaseModel # These pydantic model is for FastAPI
from datetime import date

class BalanceSheetSchema(BaseModel):
    ticker_symbol: str
    reporting_year: int
    reporting_season: int
    cash: int = 0
    fin_assets_fvpl_curr: int = 0
    fin_assets_fvoci_curr: int = 0
    fin_assets_amort_curr: int = 0
    hedging_assets_curr: int = 0
    net_receiv: int = 0
    receiv_related_net: int = 0
    receiv_other_related_net: int = 0
    inventory: int = 0
    other_curr_assets: int = 0
    total_curr_assets: int = 0
    fin_assets_fvpl_noncurr: int = 0
    fin_assets_fvoci_noncurr: int = 0
    fin_assets_amort_noncurr: int = 0
    equity_inv: int = 0
    ppe: int = 0
    rou_assets: int = 0
    intangible: int = 0
    deferred_tax_asset: int = 0
    other_noncurr_assets: int = 0
    total_noncurr_assets: int = 0
    total_assets: int = 0
    fin_liab_fvpl_curr: int = 0
    hedging_liab_curr: int = 0
    acct_payable: int = 0
    acct_payable_related: int = 0
    other_payables: int = 0
    tax_liab_curr: int = 0
    other_curr_liab: int = 0
    total_curr_liab: int = 0
    bonds_payable: int = 0
    lt_borrow: int = 0
    deferred_tax_liab: int = 0
    lease_liab_noncurr: int = 0
    other_noncurr_liab: int = 0
    total_noncurr_liab: int = 0
    total_liab: int = 0
    ord_share: int = 0
    total_share_cap: int = 0
    cap_res_premium: int = 0
    cap_res_diff_subsidiaries: int = 0
    cap_res_eq_changes_subs: int = 0
    cap_res_donated: int = 0
    cap_res_eq_method: int = 0
    cap_res_merger: int = 0
    cap_res_restricted_shares: int = 0
    total_cap_res: int = 0
    legal_res: int = 0
    special_res: int = 0
    unapp_retained_earn: int = 0
    total_retained_earn: int = 0
    total_other_eq: int = 0
    treasury_shares: int = 0
    total_eq_parent: int = 0
    non_ctrl_interests: int = 0
    total_eq: int = 0
    total_liab_eq: int = 0
    anticipate_stock_issue: int = 0
    treasury_shares_held: int = 0

    class Config:
        from_attributes = True

