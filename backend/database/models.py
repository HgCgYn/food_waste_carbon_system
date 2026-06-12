"""ORM models for users, food factors, analysis records, and analysis items."""

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import relationship

from database.db import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    records = relationship("AnalysisRecord", back_populates="user")


class FoodCarbonFactor(Base):
    __tablename__ = "food_carbon_factors"

    food_id = Column(Integer, primary_key=True, index=True)
    yolo_label = Column(String(100), nullable=False, unique=True, index=True)
    food_name_zh = Column(String(100), nullable=False)
    category = Column(String(100), nullable=True)
    carbon_factor = Column(Numeric(10, 6), nullable=False, default=0)
    density_factor = Column(Numeric(10, 6), nullable=False, default=1)
    source = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class AnalysisRecord(Base):
    __tablename__ = "analysis_records"

    record_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    image_path = Column(Text, nullable=False)
    total_weight_g = Column(Float, nullable=False)
    total_carbon_emission_kg = Column(Numeric(12, 6), nullable=False, default=0)
    waste_percentage = Column(Float, nullable=False, default=0)
    model_used = Column(String(50), nullable=False, default="yolo")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User", back_populates="records")
    items = relationship("AnalysisItem", back_populates="record", cascade="all, delete-orphan")


class AnalysisItem(Base):
    __tablename__ = "analysis_items"

    item_id = Column(Integer, primary_key=True, index=True)
    record_id = Column(Integer, ForeignKey("analysis_records.record_id"), nullable=False)
    yolo_label = Column(String(100), nullable=False)
    food_name_zh = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    area = Column(Float, nullable=False)
    density_factor = Column(Numeric(10, 6), nullable=False, default=1)
    estimated_weight_g = Column(Float, nullable=False, default=0)
    carbon_factor = Column(Numeric(10, 6), nullable=False, default=0)
    carbon_emission_kg = Column(Numeric(12, 6), nullable=False, default=0)

    record = relationship("AnalysisRecord", back_populates="items")
