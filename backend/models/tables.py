from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class CountryStat(Base):
    __tablename__ = "country_stats"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    life_expectancy = Column(Float)
    suicide_rate = Column(String)
    unemployment = Column(String)
    gdp_trend = Column(String)