# -*- coding: utf-8 -*-
"""
DACH Immobilien-AfA-, 5-%-Degressiv-Abschreibungs- (§ 7 Abs. 5a EStG), Mietrendite- & Cashflow-Rechner 2026
"""

from .calculator import (
    RealEstateAfaInput,
    RealEstateAfaResult,
    calculate_real_estate_afa,
)

__all__ = [
    "RealEstateAfaInput",
    "RealEstateAfaResult",
    "calculate_real_estate_afa",
]
