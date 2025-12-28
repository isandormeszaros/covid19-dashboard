from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

# Saját modulok importálása
from backend.models import database, tables
from backend.services.data_fetcher import WhoDataService

# Adatbázis inicializás
tables.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="COVID19 Dashboard API")
service = WhoDataService()

class DashboardMetrics(BaseModel):
    life_expectancy: float
    unemployment: str
    suicide_rate: str
    gdp_trend: str

class DashboardResponse(BaseModel):
    country: str
    metrics: DashboardMetrics
    charts: dict

# Adatbázis session kezelés
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINT ---

@app.get("/")
def read_root():
    return {"status": "running", "docs_url": "/docs"}

@app.get("/api/dashboard/{country_code}", response_model=DashboardResponse)
def get_dashboard(country_code: str, db: Session = Depends(get_db)):
    data = service.get_dashboard_data(country_code)
    
    if data is None:
        raise HTTPException(status_code=404, detail=f"Nincs adat a '{country_code}' országhoz.")
    
    try:
        stat = tables.CountryStat(
            country_code=country_code,
            life_expectancy=data["metrics"]["life_expectancy"],
            suicide_rate=data["metrics"]["suicide_rate"],
            unemployment=data["metrics"]["unemployment"],
            gdp_trend=data["metrics"]["gdp_trend"]
        )
        db.add(stat)
        db.commit()
    except Exception as e:
        print(f"DB Error: {e}") 

    return data