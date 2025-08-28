# backend/app/services/calc.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models import Activity, EmissionFactor
from sqlalchemy import or_


@dataclass
class LineItem:
    activity_id: int
    category: str
    scope: str
    unit: str
    quantity: float
    factor_value: float
    factor_unit: str
    dataset: str
    region: Optional[str]
    year: Optional[int]
    version: Optional[str]
    co2e_kg: float

def _pick_factor(db, category: str, unit: str, region: Optional[str] = None):
    q = db.query(EmissionFactor).filter(
        EmissionFactor.category == category,
        EmissionFactor.input_unit == unit,
    )
    if region:
        q = q.filter(or_(EmissionFactor.region == region, EmissionFactor.region.is_(None)))
    # if no region provided, don't constrain by region at all

    # prefer most recent then highest id
    q = q.order_by(EmissionFactor.year.desc().nullslast(), EmissionFactor.id.desc())
    return q.first()

def run_calculation(
    db: Session,
    org_id: int,
    period_start,
    period_end,
    region: Optional[str] = "US"
) -> Tuple[List[LineItem], Dict[str, float], Dict[str, float]]:
    activities = (
        db.query(Activity)
        .filter(
            Activity.org_id == org_id,
            Activity.period_end >= period_start,
            Activity.period_start <= period_end,
        )
        .all()
    )

    items: List[LineItem] = []
    by_scope: Dict[str, float] = {"1": 0.0, "2": 0.0, "3": 0.0}
    by_category: Dict[str, float] = {}

    for a in activities:
        factor = _pick_factor(db, a.category, a.unit, region=region)
        if not factor:
            # skip unmapped for now; later we can return a warnings list
            continue
        co2e_kg = float(a.quantity) * float(factor.factor_value)

        li = LineItem(
            activity_id=a.id,
            category=a.category,
            scope=str(a.scope),
            unit=a.unit,
            quantity=float(a.quantity),
            factor_value=float(factor.factor_value),
            factor_unit=factor.input_unit,
            dataset=factor.dataset,
            region=factor.region,
            year=factor.year,
            version=factor.version,
            co2e_kg=co2e_kg,
        )
        items.append(li)
        by_scope[str(a.scope)] = by_scope.get(str(a.scope), 0.0) + co2e_kg
        by_category[a.category] = by_category.get(a.category, 0.0) + co2e_kg

    return items, by_scope, by_category
