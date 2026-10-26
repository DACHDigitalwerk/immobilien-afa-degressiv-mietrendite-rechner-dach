# -*- coding: utf-8 -*-
"""
Steuer- und finanzmathematisches Kernmodul fuer den
DACH Immobilien-AfA-, 5-%-Degressiv-Abschreibungs- (§ 7 Abs. 5a EStG), Mietrendite- & Cashflow-Rechner 2026.

Rechtlicher Hinweis (§ 2 RDG / § 5 StBerG / § 34c GewO):
Rein mathematische Orientierungsrechnung ohne Steuer-, Rechts- oder Anlageberatung.
"""

from dataclasses import dataclass


@dataclass
class RealEstateAfaInput:
    country: str = "DE"
    purchase_price: float = 450_000.0
    closing_cost_pct: float = 8.5
    building_share_pct: float = 78.0
    living_area_sqm: float = 95.0
    afa_mode: str = "degressiv_5"  # degressiv_5, degressiv_7b, linear_3, linear_2, linear_25
    marginal_tax_rate_pct: float = 42.0
    monthly_cold_rent: float = 1_650.0
    monthly_non_recoverable_cost: float = 190.0
    equity_invested: float = 88_250.0
    loan_interest_pct: float = 3.65
    loan_repayment_pct: float = 2.0


@dataclass
class RealEstateAfaResult:
    country: str
    currency: str
    total_acquisition_cost: float
    afa_basis_building: float
    loan_amount: float
    afa_year_1: float
    afa_10_year_sum: float
    optimal_switch_year: int
    afa_tax_shield_year_1: float
    annual_cold_rent: float
    net_operating_income: float
    annual_interest: float
    annual_repayment: float
    pre_tax_cashflow_annual: float
    taxable_rental_income_vv: float
    tax_effect_year_1: float
    after_tax_cashflow_annual: float
    after_tax_cashflow_monthly: float
    gross_rental_yield_pct: float
    net_rental_yield_pct: float
    return_on_equity_after_tax_pct: float


def calculate_real_estate_afa(inp: RealEstateAfaInput) -> RealEstateAfaResult:
    c = inp.country.upper().strip()
    if c not in ("DE", "AT", "CH"):
        raise ValueError(f"Unsupported country '{inp.country}'. Choose from DE, AT, CH.")
    if inp.purchase_price <= 0:
        raise ValueError("purchase_price must be positive")
    if not (10.0 <= inp.building_share_pct <= 95.0):
        raise ValueError("building_share_pct must be between 10 and 95")
    if inp.equity_invested <= 0:
        raise ValueError("equity_invested must be positive")

    currency = "CHF" if c == "CH" else "EUR"
    price = float(inp.purchase_price)
    closing_costs = price * (max(0.0, float(inp.closing_cost_pct)) / 100.0)
    total_cost = price + closing_costs
    afa_base = total_cost * (float(inp.building_share_pct) / 100.0)
    loan = max(0.0, total_cost - float(inp.equity_invested))

    annual_rent = max(0.0, float(inp.monthly_cold_rent)) * 12.0
    annual_non_rec = max(0.0, float(inp.monthly_non_recoverable_cost)) * 12.0

    afa_yr1 = 0.0
    afa_10yr = 0.0
    switch_year = 0

    if c == "AT":
        # AT § 8 Abs. 1a / § 16 Abs. 1 Z 8 EStG: 4.5% Yr1, 3.0% Yr2, 1.5% Yr3+
        afa_yr1 = afa_base * 0.045
        afa_10yr = afa_base * (0.045 + 0.030 + 8 * 0.015)
        switch_year = 3
    elif c == "CH":
        # CH Art. 32 DBG 20% flat maintenance deduction on gross rental income
        afa_yr1 = annual_rent * 0.20
        afa_10yr = afa_yr1 * 10.0
    else:
        mode = inp.afa_mode.strip().lower()
        if mode in ("degressiv_5", "degressiv_7b"):
            sonder_7b_base = min(afa_base, max(1.0, float(inp.living_area_sqm)) * 4_000.0) if mode == "degressiv_7b" else 0.0
            rest = afa_base
            lin_floor = afa_base * 0.03
            for y in range(1, 36):
                deg_amt = rest * 0.05
                sonder_amt = (sonder_7b_base * 0.05) if (mode == "degressiv_7b" and y <= 4) else 0.0
                if switch_year == 0 and y > 4 and lin_floor >= deg_amt:
                    switch_year = y
                yr_amt = lin_floor if (switch_year > 0 and y >= switch_year) else (deg_amt + sonder_amt)
                if y == 1:
                    afa_yr1 = yr_amt
                if y <= 10:
                    afa_10yr += yr_amt
                rest = max(0.0, rest - yr_amt)
        elif mode == "linear_3":
            afa_yr1 = afa_base * 0.03
            afa_10yr = afa_yr1 * 10.0
        elif mode == "linear_25":
            afa_yr1 = afa_base * 0.025
            afa_10yr = afa_yr1 * 10.0
        elif mode == "linear_2":
            afa_yr1 = afa_base * 0.02
            afa_10yr = afa_yr1 * 10.0
        else:
            raise ValueError(f"Unsupported afa_mode '{inp.afa_mode}'")

    noi = annual_rent - annual_non_rec
    annual_interest = loan * (max(0.0, float(inp.loan_interest_pct)) / 100.0)
    annual_repayment = loan * (max(0.0, float(inp.loan_repayment_pct)) / 100.0)
    pre_tax_cf = noi - annual_interest - annual_repayment

    tax_rate = max(0.0, min(60.0, float(inp.marginal_tax_rate_pct))) / 100.0
    taxable_vv = noi - annual_interest - afa_yr1
    tax_effect = -taxable_vv * tax_rate
    afa_tax_shield = afa_yr1 * tax_rate

    after_tax_cf_annual = pre_tax_cf + tax_effect
    after_tax_cf_monthly = after_tax_cf_annual / 12.0

    gross_yield = (annual_rent / price) * 100.0
    net_yield = (noi / total_cost) * 100.0
    roe_after_tax = ((after_tax_cf_annual + annual_repayment) / float(inp.equity_invested)) * 100.0

    return RealEstateAfaResult(
        country=c,
        currency=currency,
        total_acquisition_cost=round(total_cost, 2),
        afa_basis_building=round(afa_base, 2),
        loan_amount=round(loan, 2),
        afa_year_1=round(afa_yr1, 2),
        afa_10_year_sum=round(afa_10yr, 2),
        optimal_switch_year=switch_year,
        afa_tax_shield_year_1=round(afa_tax_shield, 2),
        annual_cold_rent=round(annual_rent, 2),
        net_operating_income=round(noi, 2),
        annual_interest=round(annual_interest, 2),
        annual_repayment=round(annual_repayment, 2),
        pre_tax_cashflow_annual=round(pre_tax_cf, 2),
        taxable_rental_income_vv=round(taxable_vv, 2),
        tax_effect_year_1=round(tax_effect, 2),
        after_tax_cashflow_annual=round(after_tax_cf_annual, 2),
        after_tax_cashflow_monthly=round(after_tax_cf_monthly, 2),
        gross_rental_yield_pct=round(gross_yield, 2),
        net_rental_yield_pct=round(net_yield, 2),
        return_on_equity_after_tax_pct=round(roe_after_tax, 2),
    )
