from fastapi import FastAPI
from backend.services.data_fetcher import AthenaAPI

app = FastAPI(title="WHO Athena API Dashboard")

athena = AthenaAPI()

@app.get("/")
def root():
    return {"message": "WHO Athena API is running"}

"""Elérhető indikátorok listája"""
@app.get("/api/indicators")
def get_indicators():
    data = athena.fetch_indicator_list()
    return {"count": len(data), "indicators": data} 

"""Elérhető indikátorok az adott országra"""
@app.get("/api/available/{country_code}")
def get_available_indicators(country_code: str):
    all_indicators = athena.fetch_indicator_list()
    available = []

    for code, name in all_indicators[:40]:
        df = athena.fetch_country_data(code, country_code)
        if not df.empty:
            available.append({"code": code, "name": name, "records": len(df)})

    return {
        "country": country_code,
        "available_indicators_count": len(available),
        "indicators": available
    }

"""Adott ország és indikátor adatai"""
@app.get("/api/country/{country_code}/indicator/{indicator_code}")
def get_country_indicator(country_code: str, indicator_code: str):
    df = athena.fetch_country_data(indicator_code, country_code)
    if df.empty:
        return {"error": f"Nincs adat az indikátorhoz: {indicator_code} az országra: {country_code}"}
    return df.to_dict(orient="records")