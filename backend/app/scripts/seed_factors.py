# backend/app/scripts/seed_factors.py
from sqlalchemy.orm import Session
from app.db import SessionLocal, engine
from app.models import EmissionFactor, Base

SEED = [
    # dataset, region, category, input_unit, factor_value (kgCO2e per unit), year, version
    ("EPA", "US", "electricity", "kWh", 0.386, 2022, "EPA-2022-US-avg"),
    ("EPA", "US", "diesel", "L", 2.68, 2022, "EPA-2022"),
    ("EPA", "US", "gasoline", "L", 2.31, 2022, "EPA-2022"),
    ("EPA", "US", "natural_gas", "therm", 5.31, 2022, "EPA-2022"),
]

def upsert_factor(db: Session, row):
    dataset, region, category, unit, value, year, version = row
    obj = (
        db.query(EmissionFactor)
        .filter(
            EmissionFactor.dataset == dataset,
            EmissionFactor.region == region,
            EmissionFactor.category == category,
            EmissionFactor.input_unit == unit,
            EmissionFactor.year == year,
        )
        .one_or_none()
    )
    if obj:
        obj.factor_value = value
        obj.version = version
    else:
        obj = EmissionFactor(
            dataset=dataset, region=region, category=category,
            input_unit=unit, factor_value=value, year=year, version=version
        )
        db.add(obj)

def main():
    # ensure table exists (safe if using Alembic already)
    Base.metadata.create_all(bind=engine, tables=[EmissionFactor.__table__])
    db = SessionLocal()
    try:
        for row in SEED:
            upsert_factor(db, row)
        db.commit()
        print(f"Seeded {len(SEED)} factors.")
    finally:
        db.close()

if __name__ == "__main__":
    main()

