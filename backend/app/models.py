from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from .db import Base

# Reusable ENUM; don't auto-create in SQLAlchemy at import time
SCOPE_ENUM = PGEnum('1', '2', '3', name='scopeenum', create_type=False)

class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True)
    type = Column(String, nullable=False)  # manual|csv|invoice
    filename = Column(String)
    storage_uri = Column(String)
    status = Column(String, default="uploaded")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, index=True)
    scope = Column(SCOPE_ENUM, nullable=False)   # ← stores '1' / '2' / '3'
    category = Column(String, nullable=False)
    unit = Column(String, nullable=False)        # kWh|therm|L|gal|mi|km|kg|USD
    quantity = Column(Float, nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    source_id = Column(Integer, ForeignKey("sources.id"))
    notes = Column(Text)
    data_quality = Column(String, default="actual")  # actual|estimate|default

    source = relationship("Source")

class EmissionFactor(Base):
    __tablename__ = "emission_factors"
    id = Column(Integer, primary_key=True, index=True)
    dataset = Column(String, nullable=False)        # e.g., "EPA", "DEFRA", "IEA"
    region = Column(String, nullable=True)          # e.g., "US", "CA-ON"
    category = Column(String, nullable=False)       # e.g., "electricity", "diesel"
    input_unit = Column(String, nullable=False)     # unit the factor expects, e.g., "kWh", "L"
    factor_value = Column(Float, nullable=False)    # kgCO2e per input_unit
    year = Column(Integer, nullable=True)           # reference year
    version = Column(String, nullable=True)         # dataset version tag

