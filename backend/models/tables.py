from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    iso3 = Column(String, unique=True, index=True)
    name = Column(String)
    data_points = relationship("DataPoint", back_populates="country")

class Indicator(Base):
    __tablename__ = "indicators"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    domain = Column(String)
    source = Column(String)
    data_points = relationship("DataPoint", back_populates="indicator")

class DataPoint(Base):
    __tablename__ = "data_points"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    value = Column(Float)
    country_id = Column(Integer, ForeignKey("countries.id"))
    indicator_id = Column(Integer, ForeignKey("indicators.id"))
    country = relationship("Country", back_populates="data_points")
    indicator = relationship("Indicator", back_populates="data_points")