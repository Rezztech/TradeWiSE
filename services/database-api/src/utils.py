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

from models import BalanceSheet

def convert_schema_to_db_model(company_id, balance_sheet_schema):
    return BalanceSheet(
        # ... all the field mappings as shown previously
        company_id=company_id,
        reporting_year=balance_sheet_schema.reporting_year,
        reporting_season=balance_sheet_schema.reporting_season,
        cash=balance_sheet_schema.cash,
        fin_assets_fvpl_curr=balance_sheet_schema.fin_assets_fvpl_curr,
        fin_assets_fvoci_curr=balance_sheet_schema.fin_assets_fvoci_curr,
        fin_assets_amort_curr=balance_sheet_schema.fin_assets_amort_curr,
        hedging_assets_curr=balance_sheet_schema.hedging_assets_curr,
        net_receiv=balance_sheet_schema.net_receiv,
        receiv_related_net=balance_sheet_schema.receiv_related_net,
        receiv_other_related_net=balance_sheet_schema.receiv_other_related_net,
        inventory=balance_sheet_schema.inventory,
        other_curr_assets=balance_sheet_schema.other_curr_assets,
        total_curr_assets=balance_sheet_schema.total_curr_assets,
        fin_assets_fvpl_noncurr=balance_sheet_schema.fin_assets_fvpl_noncurr,
        fin_assets_fvoci_noncurr=balance_sheet_schema.fin_assets_fvoci_noncurr,
        fin_assets_amort_noncurr=balance_sheet_schema.fin_assets_amort_noncurr,
        equity_inv=balance_sheet_schema.equity_inv,
        ppe=balance_sheet_schema.ppe,
        rou_assets=balance_sheet_schema.rou_assets,
        intangible=balance_sheet_schema.intangible,
        deferred_tax_asset=balance_sheet_schema.deferred_tax_asset,
        other_noncurr_assets=balance_sheet_schema.other_noncurr_assets,
        total_noncurr_assets=balance_sheet_schema.total_noncurr_assets,
        total_assets=balance_sheet_schema.total_assets,
        fin_liab_fvpl_curr=balance_sheet_schema.fin_liab_fvpl_curr,
        hedging_liab_curr=balance_sheet_schema.hedging_liab_curr,
        acct_payable=balance_sheet_schema.acct_payable,
        acct_payable_related=balance_sheet_schema.acct_payable_related,
        other_payables=balance_sheet_schema.other_payables,
        tax_liab_curr=balance_sheet_schema.tax_liab_curr,
        other_curr_liab=balance_sheet_schema.other_curr_liab,
        total_curr_liab=balance_sheet_schema.total_curr_liab,
        bonds_payable=balance_sheet_schema.bonds_payable,
        lt_borrow=balance_sheet_schema.lt_borrow,
        deferred_tax_liab=balance_sheet_schema.deferred_tax_liab,
        lease_liab_noncurr=balance_sheet_schema.lease_liab_noncurr,
        other_noncurr_liab=balance_sheet_schema.other_noncurr_liab,
        total_noncurr_liab=balance_sheet_schema.total_noncurr_liab,
        total_liab=balance_sheet_schema.total_liab,
        ord_share=balance_sheet_schema.ord_share,
        total_share_cap=balance_sheet_schema.total_share_cap,
        cap_res_premium=balance_sheet_schema.cap_res_premium,
        cap_res_diff_subsidiaries=balance_sheet_schema.cap_res_diff_subsidiaries,
        cap_res_eq_changes_subs=balance_sheet_schema.cap_res_eq_changes_subs,
        cap_res_donated=balance_sheet_schema.cap_res_donated,
        cap_res_eq_method=balance_sheet_schema.cap_res_eq_method,
        cap_res_merger=balance_sheet_schema.cap_res_merger,
        cap_res_restricted_shares=balance_sheet_schema.cap_res_restricted_shares,
        total_cap_res=balance_sheet_schema.total_cap_res,
        legal_res=balance_sheet_schema.legal_res,
        special_res=balance_sheet_schema.special_res,
        unapp_retained_earn=balance_sheet_schema.unapp_retained_earn,
        total_retained_earn=balance_sheet_schema.total_retained_earn,
        total_other_eq=balance_sheet_schema.total_other_eq,
        treasury_shares=balance_sheet_schema.treasury_shares,
        total_eq_parent=balance_sheet_schema.total_eq_parent,
        non_ctrl_interests=balance_sheet_schema.non_ctrl_interests,
        total_eq=balance_sheet_schema.total_eq,
        total_liab_eq=balance_sheet_schema.total_liab_eq,
        anticipate_stock_issue=balance_sheet_schema.anticipate_stock_issue,
        treasury_shares_held=balance_sheet_schema.treasury_shares_held
    )
