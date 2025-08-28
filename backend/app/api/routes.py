from fastapi import APIRouter, Depends, HTTPException, Query, Body
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from datetime import date

from app.db import get_db
from app import models, schemas
from app.utils.units import convert_to_canonical
from app.models import EmissionFactor
from app.services.calc import run_calculation

api_router = APIRouter()

@api_router.get("/activities", response_model=List[schemas.ActivityOut])
def list_activities(
    org_id: Optional[int] = Query(None),
    category: Optional[str] = Query(None),
    scope: Optional[str] = Query(None, pattern=r"^(1|2|3)$"),
    period_start: Optional[date] = Query(None),
    period_end: Optional[date] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    q = db.query(models.Activity)
    if org_id is not None:
        q = q.filter(models.Activity.org_id == org_id)
    if category:
        q = q.filter(models.Activity.category == category)
    if scope:
        q = q.filter(models.Activity.scope == scope)
    if period_start:
        q = q.filter(models.Activity.period_end >= period_start)
    if period_end:
        q = q.filter(models.Activity.period_start <= period_end)

    rows = q.order_by(models.Activity.period_start.desc()).offset(offset).limit(limit).all()
    return [schemas.ActivityOut.model_validate(r) for r in rows]

@api_router.post("/activities", response_model=schemas.ActivityOut)
def create_activity(payload: schemas.ActivityCreate, db: Session = Depends(get_db)):
    if payload.period_start > payload.period_end:
        raise HTTPException(status_code=400, detail="Invalid period range")
    try:
        can_unit, can_qty, note = convert_to_canonical(payload.category, payload.unit, payload.quantity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    obj = models.Activity(
        org_id=payload.org_id,
        scope=payload.scope,
        category=payload.category,
        unit=can_unit,
        quantity=can_qty,
        period_start=payload.period_start,
        period_end=payload.period_end,
        # append conversion note (optional)
        notes=(payload.notes + " | " if payload.notes else "") + (note or ""),
        data_quality=payload.data_quality,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return schemas.ActivityOut.model_validate(obj)

@api_router.get("/factors")
def list_factors(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    dataset: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(EmissionFactor)
    if category: q = q.filter(EmissionFactor.category == category)
    if region: q = q.filter(EmissionFactor.region == region)
    if dataset: q = q.filter(EmissionFactor.dataset == dataset)
    return [  # plain dicts OK here
        {
            "id": f.id,
            "dataset": f.dataset,
            "region": f.region,
            "category": f.category,
            "input_unit": f.input_unit,
            "factor_value": f.factor_value,
            "year": f.year,
            "version": f.version,
        }
        for f in q.order_by(EmissionFactor.category, EmissionFactor.region).all()
    ]
@api_router.get("/calculate/run", response_model=schemas.CalculationResult)
def calculate_run(
    org_id: int = Query(..., ge=1),
    period_start: date = Query(...),
    period_end: date = Query(...),
    region: Optional[str] = Query("US"),
    db: Session = Depends(get_db),
):
    if period_start > period_end:
        raise HTTPException(status_code=400, detail="Invalid period range")

    items, by_scope, by_category = run_calculation(
        db=db,
        org_id=org_id,
        period_start=period_start,
        period_end=period_end,
        region=region,
    )
    total_kg = sum(i.co2e_kg for i in items)
    return schemas.CalculationResult(
        org_id=org_id,
        period_start=period_start,
        period_end=period_end,
        total_kg=total_kg,
        by_scope=by_scope,
        by_category=by_category,
        items=[schemas.EmissionLineItem(**i.__dict__) for i in items],
    )

@api_router.get("/emissions/summary")
def emissions_summary(
    org_id: int = Query(..., ge=1),
    period_start: date = Query(...),
    period_end: date = Query(...),
    group_by: str = Query("scope", pattern="^(scope|category)$"),
    region: Optional[str] = Query("US"),
    db: Session = Depends(get_db),
) -> Dict[str, float]:
    if period_start > period_end:
        raise HTTPException(status_code=400, detail="Invalid period range")

    items, by_scope, by_category = run_calculation(
        db=db,
        org_id=org_id,
        period_start=period_start,
        period_end=period_end,
        region=region,
    )
    return by_scope if group_by == "scope" else by_category