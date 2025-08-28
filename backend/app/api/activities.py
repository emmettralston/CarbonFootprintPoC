from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db, Base, engine
from .. import models, schemas
from ..deps import get_org_id
from ..utils import validate_unit


# Create tables on startup (simplifies PoC)
Base.metadata.create_all(bind=engine)


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/", response_model=schemas.ActivityOut)
def create_activity(payload: schemas.ActivityCreate, db: Session = Depends(get_db), org_id: int = Depends(get_org_id)):
    if payload.org_id != org_id:
        raise HTTPException(status_code=403, detail="org mismatch")
    if not validate_unit(payload.unit):
        raise HTTPException(status_code=400, detail="unsupported unit")
    if payload.period_start > payload.period_end:
        raise HTTPException(status_code=400, detail="invalid period range")


    obj = models.Activity(
        org_id=payload.org_id,
        scope=models.ScopeEnum(payload.scope),
        category=payload.category,
        unit=payload.unit,
        quantity=payload.quantity,
        period_start=payload.period_start,
        period_end=payload.period_end,
        source_id=payload.source_id,
        notes=payload.notes,
        data_quality=payload.data_quality,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/")
def list_activities(db: Session = Depends(get_db), org_id: int = Depends(get_org_id)):
    q = db.query(models.Activity).filter(models.Activity.org_id == org_id).order_by(models.Activity.period_start.desc())
    return q.all()