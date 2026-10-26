# -*- coding: utf-8 -*-
"""
CLI fuer den DACH Immobilien-AfA-, 5-%-Degressiv-Abschreibungs- & Mietrendite-Rechner 2026
"""

import argparse
import json
from .calculator import RealEstateAfaInput, calculate_real_estate_afa


def main():
    parser = argparse.ArgumentParser(
        description="DACH Immobilien-AfA-, 5-%-Degressiv-Abschreibungs- (§ 7 Abs. 5a EStG), Mietrendite- & Cashflow-Rechner 2026"
    )
    parser.add_argument("--country", default="DE", choices=["DE", "AT", "CH"], help="Land (DE, AT, CH)")
    parser.add_argument("--price", type=float, default=450_000.0, help="Kaufpreis Immobilie")
    parser.add_argument("--building-share", type=float, default=78.0, help="Gebaeudeanteil in Prozent (%%)")
    parser.add_argument("--mode", default="degressiv_5", help="AfA-Modus (degressiv_5, degressiv_7b, linear_3, linear_2, linear_25)")
    parser.add_argument("--rent", type=float, default=1_650.0, help="Monatliche Nettokaltmiete")
    parser.add_argument("--json", action="store_true", help="Ausgabe als JSON")

    args = parser.parse_args()
    inp = RealEstateAfaInput(
        country=args.country,
        purchase_price=args.price,
        building_share_pct=args.building_share,
        afa_mode=args.mode,
        monthly_cold_rent=args.rent,
    )
    res = calculate_real_estate_afa(inp)

    if args.json:
        print(json.dumps(res.__dict__, indent=2, ensure_ascii=False))
    else:
        print("=" * 76)
        print(f"DACH IMMOBILIEN-AFA- & MIETRENDITE-ANALYSE 2026 ({res.country} / {res.currency})")
        print("=" * 76)
        print(f"Gesamterwerbskosten        : {res.total_acquisition_cost:,.2f} {res.currency}")
        print(f"Gebaeude-AfA-Basis         : {res.afa_basis_building:,.2f} {res.currency}")
        print(f"Gebaeude-AfA im 1. Jahr    : {res.afa_year_1:,.2f} {res.currency} (Steuerschild: +{res.afa_tax_shield_year_1:,.2f} {res.currency})")
        print(f"Kumulierte AfA (10 Jahre)  : {res.afa_10_year_sum:,.2f} {res.currency} (Wechseljahr: {res.optimal_switch_year})")
        print(f"Mietrendite (Brutto/Netto) : {res.gross_rental_yield_pct:.2f} % / {res.net_rental_yield_pct:.2f} %")
        print(f"EK-Rendite nach Steuern    : {res.return_on_equity_after_tax_pct:.2f} % p.a.")
        print(f"Monatl. Cashflow n. Steuer : {res.after_tax_cashflow_monthly:+,.2f} {res.currency} / Monat")
        print("=" * 76)


if __name__ == "__main__":
    main()
