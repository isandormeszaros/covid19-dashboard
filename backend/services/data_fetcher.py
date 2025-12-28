import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import random
import logging  
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class WhoDataService:
    WHO_API_URL = os.getenv("WHO_API_URL")
    WORLDBANK_API_URL = os.getenv("WORLDBANK_API_URL")
    
    COUNTRY_MAP = {
        "HUN": "Hungary",
        "USA": "United States",
        "GBR": "United Kingdom",
        "DEU": "Germany",
        "AUT": "Austria",
        "FRA": "France",
    }

    def get_dashboard_data(self, country_code: str):
        # WHO várható élettartam
        life_exp_df = self.fetch_indicator("WHOSIS_000001", country_code)
        
        if life_exp_df.empty:
            logger.warning(f"Nincs adat ehhez az országhoz: {country_code}") # Logolás print helyett
            return None 

        #Legutolsó elérhető adatot
        last_record = life_exp_df.iloc[-1]
        life_exp_val = round(last_record["value"], 1)

        # Öngyilkossági ráta
        suicide_df = self.fetch_indicator("MH_12", country_code)
        suicide_val = "-"
        if not suicide_df.empty:
            val = suicide_df.iloc[-1]["value"]
            suicide_val = f"{round(val, 1)}/100K"

        #WS Wikipédia munkanélkülséghez
        country_name = self.COUNTRY_MAP.get(country_code, "Hungary")
        unemployment_data = self.scrape_wikipedia_unemployment(country_name)
        
        # Wordbank API a GDP adatok miatt
        gdp_trend = self.fetch_worldbank_gdp(country_code)

        return {
            "country": country_code,
            "metrics": {
                "life_expectancy": life_exp_val,
                "suicide_rate": suicide_val,
                "unemployment": unemployment_data.get("unemployment", "N/A"),
                "gdp_trend": self.calculate_trend_direction(gdp_trend)
            },
            "charts": {
                "life_exp": life_exp_df.to_dict(orient="records"),
                "gdp": gdp_trend
            }
        }

    def scrape_wikipedia_unemployment(self, country_name):
        data = {"unemployment": "N/A"}
        try:
            url = "https://en.wikipedia.org/wiki/List_of_countries_by_unemployment_rate"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=3)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                for table in soup.find_all("table", class_="wikitable"):
                    for row in table.find_all("tr"):
                        text = row.get_text().strip()
                        if country_name in text:
                            numbers = re.findall(r'\d+\.\d+', text)
                            if numbers:
                                data["unemployment"] = f"{numbers[0]} %"
                                return data
        except Exception as e:
            logger.error(f"Hiba a scraping közben: {e}") 
        return data

    def fetch_worldbank_gdp(self, country_code):
        try:
            # ISO CODE (pl: HUN)
            url = f"{self.WORLDBANK_API_URL}/{country_code}/indicator/NY.GDP.PCAP.CD?format=json&date=2010:2023&per_page=20"
            response = requests.get(url, timeout=5)
            
            if response.status_code != 200:
                logger.error(f"Világbank API hiba: {response.status_code}") 
                return []

            data = response.json()
            
            if len(data) < 2:
                return []
            
            records = []
            for item in data[1]:
                if item["value"] is not None:
                    records.append({
                        "year": int(item["date"]),
                        "value": float(item["value"])
                    })
            
            #funkcionális
            return sorted(records, key=lambda x: x["year"])
            
        except Exception as e:
            logger.error(f"World Bank API hiba: {e}") 
            return []

    def calculate_trend_direction(self, trend_data):
        if len(trend_data) < 2:
            return "N/A"
        last = trend_data[-1]["value"]
        prev = trend_data[-2]["value"]
        return "Növekvő" if last > prev else "Csökkenő"

    def fetch_indicator(self, indicator, country):
        try:
            url = f"{self.WHO_API_URL}/{indicator}?$filter=SpatialDim eq '{country}'"
            resp = requests.get(url, timeout=5)
            data_raw = resp.json().get("value", [])
            
            if not data_raw: return pd.DataFrame()
            
            df = pd.DataFrame(data_raw)
            # Csak az év és az érték oszlopokat tartjuk meg
            df = df[["TimeDim", "Value", "Dim1"]] if "Dim1" in df.columns else df[["TimeDim", "Value"]]
            # Adattisztítás: levágjuk a felesleges karaktereket a számokról
            df["Value"] = df["Value"].apply(lambda x: self.clean_number_internal(x))
            # Nemek szerinti bontás
            if "Dim1" in df.columns:
                both_sexes = df[df["Dim1"].isin(["BTSX", "SEX_BTSX", "BOTH_SEXES"])]
                if not both_sexes.empty:
                    df = both_sexes

            df = df.rename(columns={"TimeDim": "year", "Value": "value"})
            df["year"] = pd.to_numeric(df["year"])
            
            grouped = df.groupby("year")
            df = grouped["value"].mean()
            df = df.reset_index()
            
            return df.sort_values("year")
            
        except Exception as e:
            logger.error(f"WHO API hiba ({indicator}): {e}")
            return pd.DataFrame()

    def clean_number_internal(self, value):
        try:
            clean_str = str(value).split(" ")[0]
            # számjegyek, pontok maradnak csak
            clean_str = re.sub(r'[^\d\.]', '', clean_str)
            return float(clean_str)
        except:
            return 0.0

    def clean_number(self, value):
        return self.clean_number_internal(value)
    
    def get_supported_countries(self):
        return self.COUNTRY_MAP
    
    