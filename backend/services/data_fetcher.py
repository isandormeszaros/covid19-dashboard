import requests
import pandas as pd

class AthenaAPI:
    BASE_URL = "https://ghoapi.azureedge.net/api"

    def __init__(self):
        pass

    def fetch_indicator_list(self):
        """Lekéri az összes elérhető indikátort (pl. halálozás, életkor stb.)"""
        url = f"{self.BASE_URL}/Indicator"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API hiba: {response.status_code}")
        data = response.json()["value"]
        indicators = [(item["IndicatorCode"], item["IndicatorName"]) for item in data]
        return indicators

    def fetch_country_data(self, indicator_code: str, country_code: str = "HUN"):
        """
        Lekéri egy adott ország adatait egy adott indikátorhoz.
        Példa: indicator_code='WHS9_86' (COVID-19 halálozás)
        """
        url = f"{self.BASE_URL}/{indicator_code}?$filter=SpatialDim eq '{country_code}'"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"API hiba: {response.status_code}")

        data = response.json().get("value", [])
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df = df[["SpatialDim", "TimeDim", "Value", "TimeDimType"]]
        df = df.rename(columns={
            "SpatialDim": "country",
            "TimeDim": "year",
            "Value": "value",
            "TimeDimType": "type"
        })
        return df