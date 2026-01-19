import os
import httpx
from typing import Optional, List, Dict, Any, Union

# API Base URLs
XEMA_BASE_URL = "https://api.meteo.cat/xema/v1"
PRONOSTIC_BASE_URL = "https://api.meteo.cat/pronostic/v1"
REFERENCIA_BASE_URL = "https://api.meteo.cat/referencia/v1"

class MeteocatClient:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("METEOCAT_API_KEY is required")
        self.api_key = api_key
        self.headers = {
            "x-api-key": self.api_key,
            "Accept": "application/json",
        }

    async def _request(self, url: str) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            
            if response.status_code != 200:
                # detailed error handling could be added here
                raise Exception(f"Meteocat API error ({response.status_code}): {response.text}")
            
            return response.json()

    # ===== Reference Data =====

    async def get_municipalities(self) -> List[Dict[str, Any]]:
        return await self._request(f"{REFERENCIA_BASE_URL}/municipis")

    async def get_regions(self) -> List[Dict[str, Any]]:
        return await self._request(f"{REFERENCIA_BASE_URL}/comarques")

    async def get_weather_symbols(self) -> Any:
        return await self._request(f"{REFERENCIA_BASE_URL}/simbols")

    # ===== Station Data (XEMA) =====

    async def get_all_stations(self, state: Optional[str] = None, date: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{XEMA_BASE_URL}/estacions/metadades"
        params = []
        if state:
            params.append(f"estat={state}")
        if date:
            params.append(f"data={date}")
        
        if params:
            url += "?" + "&".join(params)
            
        return await self._request(url)

    async def get_station(self, station_code: str) -> Dict[str, Any]:
        # The API returns an object or a list? TS type says Station[], implying list.
        # But usually specific station endpoint returns one object or a list of one.
        # We will return whatever the API returns.
        return await self._request(f"{XEMA_BASE_URL}/estacions/{station_code}/metadades")

    async def get_station_variables(self, station_code: str, state: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{XEMA_BASE_URL}/estacions/{station_code}/variables/metadades"
        if state:
            url += f"?estat={state}"
        return await self._request(url)

    async def get_all_variables(self) -> List[Dict[str, Any]]:
        return await self._request(f"{XEMA_BASE_URL}/variables/metadades")

    async def get_latest_readings(self, variable_code: int, station_code: Optional[str] = None) -> List[Dict[str, Any]]:
        url = f"{XEMA_BASE_URL}/variables/mesurades/{variable_code}/ultimes"
        if station_code:
            url += f"?codiEstacio={station_code}"
        return await self._request(url)

    async def get_readings(
        self,
        variable_code: int,
        year: int,
        month: int,
        day: int,
        station_code: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        month_str = f"{month:02d}"
        day_str = f"{day:02d}"
        url = f"{XEMA_BASE_URL}/variables/mesurades/{variable_code}/{year}/{month_str}/{day_str}"
        if station_code:
            url += f"?codiEstacio={station_code}"
        return await self._request(url)

    # ===== Forecasts (Predicció) =====

    async def get_municipal_forecast_72h(self, municipality_code: str) -> Any:
        return await self._request(f"{PRONOSTIC_BASE_URL}/municipalHoraria/{municipality_code}")

    async def get_municipal_forecast_8days(self, municipality_code: str) -> Any:
        return await self._request(f"{PRONOSTIC_BASE_URL}/municipal/{municipality_code}")

    async def get_general_forecast(self, year: int, month: int, day: int) -> Any:
        month_str = f"{month:02d}"
        day_str = f"{day:02d}"
        return await self._request(f"{PRONOSTIC_BASE_URL}/catalunya/{year}/{month_str}/{day_str}")

    async def get_regional_forecast(self, year: int, month: int, day: int) -> Any:
        month_str = f"{month:02d}"
        day_str = f"{day:02d}"
        return await self._request(f"{PRONOSTIC_BASE_URL}/comarcal/{year}/{month_str}/{day_str}")

    async def get_uvi_forecast(self, municipality_code: str) -> Any:
        return await self._request(f"{PRONOSTIC_BASE_URL}/uvi/{municipality_code}")
