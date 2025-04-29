# solar-radiation

---

## Installation

```bash
❯ pip install solar-radiation

## if you have Poetry
❯ poetry add solar-radiation
```
---

## Quick Start

```python
from solar_radiation.solar_radiation import calculate_extraterrestrial_radiation
import datetime

df = calculate_extraterrestrial_radiation(
    latitude=70.5,
    longitude=127.0,
    start_date=datetime.date(2024, 4, 28),
    end_date=datetime.date(2024, 4, 28),
    time_interval="1h",
    timezone="Asia/Seoul",  
    surface_tilt=0.0,       
    surface_azimuth=0.0,    
    only_daytime=True,      
    return_Gon=True,        
    return_solar_angles=True,  
)

print(df)

```

## Main Functions

calculate_extraterrestrial_radiation
Calculates extraterrestrial solar radiation over user-specified date ranges and intervals.

Parameters:

latitude (float): Latitude of location (degrees)

longitude (float): Longitude of location (degrees)

start_date (datetime.date): Start date

end_date (datetime.date): End date

time_interval (str): Time interval ('1m', '5m', '15m', '30m', '1h', '4h', '12h', '1d')

timezone (str): Timezone in IANA format (e.g., "Asia/Seoul", "UTC")

surface_tilt (float): Surface tilt from horizontal (degrees)

surface_azimuth (float): Surface azimuth (degrees from south)

only_daytime (bool): If True, only returns daytime values

return_Gon (bool): If True, include extraterrestrial normal irradiance (G_on)

return_solar_angles (bool): If True, include solar elevation and azimuth

Returns:

A Pandas DataFrame with:

datetime

G_o (W/m²)

(Optional) G_on (W/m²)

(Optional) solar_elevation (degrees)

(Optional) solar_azimuth (degrees)
