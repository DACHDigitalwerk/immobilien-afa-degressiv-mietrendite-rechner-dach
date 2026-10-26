# -*- coding: utf-8 -*-
import pytest
from immobilien_afa_dach import RealEstateAfaInput, calculate_real_estate_afa


def test_default_de_degressive_5_afa():
    res = calculate_real_estate_afa(RealEstateAfaInput())
    assert res.country == "DE"
    assert res.currency == "EUR"
    # 450,000 * 1.085 = 488,250 * 0.78 = 380,835
    assert res.total_acquisition_cost == 488_250.0
    assert res.afa_basis_building == 380_835.0
    # 5% of 380,835 = 19,041.75
    assert res.afa_year_1 == 19_041.75
    assert res.optimal_switch_year == 11


def test_degressive_plus_7b_sonder_afa():
    inp = RealEstateAfaInput(afa_mode="degressiv_7b", living_area_sqm=95.0)
    res = calculate_real_estate_afa(inp)
    # 95 sqm * 4,000 = 380,000 cap -> 5% degressiv (19,041.75) + 5% of 380,000 (19,000) = 38,041.75
    assert res.afa_year_1 == 38_041.75
    assert res.afa_year_1 > calculate_real_estate_afa(RealEstateAfaInput(afa_mode="degressiv_5")).afa_year_1


def test_linear_2_and_3_and_25_modes():
    r2 = calculate_real_estate_afa(RealEstateAfaInput(afa_mode="linear_2"))
    r25 = calculate_real_estate_afa(RealEstateAfaInput(afa_mode="linear_25"))
    r3 = calculate_real_estate_afa(RealEstateAfaInput(afa_mode="linear_3"))
    assert r2.afa_year_1 == pytest.approx(380_835.0 * 0.02, abs=0.01)
    assert r25.afa_year_1 == pytest.approx(380_835.0 * 0.025, abs=0.01)
    assert r3.afa_year_1 == pytest.approx(380_835.0 * 0.03, abs=0.01)


def test_at_accelerated_building_afa():
    res = calculate_real_estate_afa(RealEstateAfaInput(country="AT"))
    # 4.5% in year 1
    assert res.afa_year_1 == pytest.approx(380_835.0 * 0.045, abs=0.05)
    assert res.optimal_switch_year == 3


def test_ch_art_32_dbg_maintenance_deduction():
    res = calculate_real_estate_afa(RealEstateAfaInput(country="CH", monthly_cold_rent=2_000.0))
    assert res.currency == "CHF"
    # 20% of 24,000 = 4,800
    assert res.afa_year_1 == 4_800.0


def test_tax_refund_on_book_loss_increases_after_tax_cashflow():
    res = calculate_real_estate_afa(RealEstateAfaInput())
    assert res.taxable_rental_income_vv < 0
    assert res.tax_effect_year_1 > 0
    assert res.after_tax_cashflow_annual > res.pre_tax_cashflow_annual


def test_gross_and_net_rental_yield_formulas():
    inp = RealEstateAfaInput(purchase_price=400_000.0, closing_cost_pct=10.0, monthly_cold_rent=2_000.0, monthly_non_recoverable_cost=200.0)
    res = calculate_real_estate_afa(inp)
    # Gross = 24,000 / 400,000 = 6.0%
    assert res.gross_rental_yield_pct == 6.0
    # Net = (24,000 - 2,400) / 440,000 = 21,600 / 440,000 = 4.91%
    assert res.net_rental_yield_pct == pytest.approx(4.91, abs=0.02)


def test_higher_building_share_increases_afa_shield():
    low = calculate_real_estate_afa(RealEstateAfaInput(building_share_pct=60.0))
    high = calculate_real_estate_afa(RealEstateAfaInput(building_share_pct=85.0))
    assert high.afa_year_1 > low.afa_year_1
    assert high.afa_tax_shield_year_1 > low.afa_tax_shield_year_1


def test_return_on_equity_calculation():
    res = calculate_real_estate_afa(RealEstateAfaInput())
    expected_roe = ((res.after_tax_cashflow_annual + res.annual_repayment) / 88_250.0) * 100.0
    assert res.return_on_equity_after_tax_pct == pytest.approx(expected_roe, abs=0.05)


def test_invalid_inputs_raise():
    with pytest.raises(ValueError):
        calculate_real_estate_afa(RealEstateAfaInput(country="NL"))
    with pytest.raises(ValueError):
        calculate_real_estate_afa(RealEstateAfaInput(building_share_pct=99.0))
    with pytest.raises(ValueError):
        calculate_real_estate_afa(RealEstateAfaInput(afa_mode="unknown"))
