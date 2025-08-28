from pydantic import BaseModel, Field
from datetime import date
from typing import Dict, List, Optional


class ActivityCreate(BaseModel):
    org_id: int
    scope: str = Field(pattern=r"^(1|2|3)$")
    category: str
    unit: str
    quantity: float
    period_start: date
    period_end: date
    source_id: Optional[int] = None
    notes: Optional[str] = None
    data_quality: Optional[str] = "actual"


class ActivityOut(ActivityCreate):
    id: int
    class Config:
        from_attributes = True

class EmissionLineItem(BaseModel):
    activity_id: int
    category: str
    scope: str
    unit: str
    quantity: float
    factor_value: float
    factor_unit: str
    dataset: str
    region: Optional[str] = None
    year: Optional[int] = None
    version: Optional[str] = None
    co2e_kg: float

class CalculationResult(BaseModel):
    org_id: int
    period_start: date
    period_end: date
    total_kg: float
    by_scope: Dict[str, float]
    by_category: Dict[str, float]
    items: List[EmissionLineItem]