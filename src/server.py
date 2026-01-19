#!/usr/bin/env python3
import os
import sys
from fastmcp import FastMCP
from dotenv import load_dotenv
from .meteocat_client import MeteocatClient

# Load environment variables
load_dotenv()

api_key = os.environ.get("METEOCAT_API_KEY")
if not api_key:
    # We might want to warn or fail, but for now let's just print to stderr
    print("Error: METEOCAT_API_KEY environment variable is required", file=sys.stderr)
    # Ideally we should probably exit, but fastmcp might handle errors gracefully
    # process.exit(1) equivalent

# Initialize client (lazy initialization might be safer if key is missing during build)
client = MeteocatClient(api_key) if api_key else None

mcp = FastMCP("Meteocat MCP Server")

@mcp.tool(description="Get all municipalities (municipis) in Catalonia with their codes, names, coordinates, and region info. Use this to find municipality codes for forecasts.")
async def get_municipalities() -> str:
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_municipalities()
    return str(result)

@mcp.tool(description="Get all regions (comarques) in Catalonia with their codes and names.")
async def get_regions() -> str:
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_regions()
    return str(result)

@mcp.tool(description="Get weather symbol reference data including sky conditions, precipitation types, and their icons.")
async def get_weather_symbols() -> str:
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_weather_symbols()
    return str(result)

@mcp.tool(description="Get metadata for all weather stations in the XEMA network. Optionally filter by operational state and date.")
async def get_all_stations(
    state: str = None, 
    date: str = None
) -> str:
    """
    Args:
        state: Filter by station state: 'ope' (operational), 'des' (decommissioned), 'rep' (under repair)
        date: Filter by date (format: YYYY-MM-DDZ). Returns stations active on this date.
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_all_stations(state, date)
    return str(result)

@mcp.tool(description="Get detailed metadata for a specific weather station by its code.")
async def get_station(station_code: str) -> str:
    """
    Args:
        station_code: The station code (e.g., 'UG' for Viladecans, 'CC' for Orís)
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_station(station_code)
    return str(result)

@mcp.tool(description="Get metadata for all measurable weather variables (temperature, humidity, wind, etc.) with their codes, units, and descriptions.")
async def get_all_variables() -> str:
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_all_variables()
    return str(result)

@mcp.tool(description="Get the list of weather variables measured by a specific station.")
async def get_station_variables(
    station_code: str,
    state: str = None
) -> str:
    """
    Args:
        station_code: The station code
        state: Filter by variable state: 'ope' (operational)
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_station_variables(station_code, state)
    return str(result)

@mcp.tool(description="Get the latest readings (last 4 hours) for a specific weather variable across all stations or a specific station.")
async def get_latest_readings(
    variable_code: int,
    station_code: str = None
) -> str:
    """
    Args:
        variable_code: The variable code (e.g., 32 for temperature, 33 for humidity). Use get_all_variables to find codes.
        station_code: Optional: filter by specific station code
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_latest_readings(variable_code, station_code)
    return str(result)

@mcp.tool(description="Get readings for a specific variable on a specific date.")
async def get_readings(
    variable_code: int,
    year: int,
    month: int,
    day: int,
    station_code: str = None
) -> str:
    """
    Args:
        variable_code: The variable code
        year: Year (e.g., 2024)
        month: Month (1-12)
        day: Day (1-31)
        station_code: Optional: filter by specific station code
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_readings(variable_code, year, month, day, station_code)
    return str(result)

@mcp.tool(description="Get hourly weather forecast for the next 72 hours for a specific municipality.")
async def get_municipal_forecast_72h(municipality_code: str) -> str:
    """
    Args:
        municipality_code: The municipality code (e.g., '080193' for Barcelona). Use get_municipalities to find codes.
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_municipal_forecast_72h(municipality_code)
    return str(result)

@mcp.tool(description="Get 8-day weather forecast for a specific municipality.")
async def get_municipal_forecast_8days(municipality_code: str) -> str:
    """
    Args:
        municipality_code: The municipality code
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_municipal_forecast_8days(municipality_code)
    return str(result)

@mcp.tool(description="Get the general weather forecast for all of Catalonia for a specific date.")
async def get_general_forecast(
    year: int,
    month: int,
    day: int
) -> str:
    """
    Args:
        year: Year (e.g., 2026)
        month: Month (1-12)
        day: Day (1-31)
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_general_forecast(year, month, day)
    return str(result)

@mcp.tool(description="Get weather forecast by region (comarca) for all of Catalonia for a specific date.")
async def get_regional_forecast(
    year: int,
    month: int,
    day: int
) -> str:
    """
    Args:
        year: Year (e.g., 2026)
        month: Month (1-12)
        day: Day (1-31)
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_regional_forecast(year, month, day)
    return str(result)

@mcp.tool(description="Get UV index forecast for the next 3 days for a specific municipality.")
async def get_uvi_forecast(municipality_code: str) -> str:
    """
    Args:
        municipality_code: The municipality code
    """
    if not client: return "Error: Server not configured (missing API key)"
    result = await client.get_uvi_forecast(municipality_code)
    return str(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"Starting Meteocat MCP server on {host}:{port}")
    
    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )