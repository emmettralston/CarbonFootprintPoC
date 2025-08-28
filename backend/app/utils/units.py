# backend/app/utils/units.py
from typing import Tuple
from pint import UnitRegistry

ureg = UnitRegistry(autoconvert_offset_to_baseunit=True)
Q_ = ureg.Quantity

# Canonical units per category
CANONICAL = {
    "electricity": "kWh",
    "diesel": "L",
    "gasoline": "L",
    "natural_gas": "therm",   # or "kWh" if you want energy basis
    "distance": "km",
    "freight_distance": "ton_km",
    "refrigerant": "kg",
    "spend": "USD",
}

# Map common aliases so users can post flexible units
ALIASES = {
    "kwh": "kWh", "mwh": "MWh", "gwh": "GWh",
    "l": "L", "liter": "L", "litre": "L",
    "gal": "gal", "gallon": "gal",
    "km": "km", "mi": "mile", "miles": "mile",
    "lb": "pound", "lbs": "pound", "kg": "kg",
    "usd": "USD", "eur": "EUR",
    "therm": "therm", "therms": "therm",
}

def canonical_unit_for(category: str) -> str:
    cat = (category or "").lower()
    return CANONICAL.get(cat, "unit")  # fallback; you may want to be strict

def normalize_unit_str(unit: str) -> str:
    u = (unit or "").strip()
    key = u.lower()
    return ALIASES.get(key, u)

def convert_to_canonical(category: str, unit: str, quantity: float) -> Tuple[str, float, str]:
    """
    Returns (canonical_unit, canonical_quantity, note)
    Note describes the conversion done, useful to stash in Activity.notes
    """
    can = canonical_unit_for(category)
    u_in = normalize_unit_str(unit)
    if can == "unit" or u_in == can:
        return can, float(quantity), ""

    # special composites not native to pint
    if can == "ton_km":
        # expect inputs like ("ton_km"), ("t*km"), or ("kg","km") not supported here
        # If user posted "ton_km" already, pass through
        if u_in in ("ton_km", "t*km", "tkm"):
            return "ton_km", float(quantity), ""
        raise ValueError(f"Unsupported composite unit conversion to {can}")

    try:
        q = Q_(quantity, u_in)
        q_can = q.to(can)
        note = f"normalized {quantity} {u_in} → {q_can.magnitude:.6g} {can}"
        return can, float(q_can.magnitude), note
    except Exception as e:
        raise ValueError(f"Cannot convert {quantity} {u_in} to {can}: {e}")
