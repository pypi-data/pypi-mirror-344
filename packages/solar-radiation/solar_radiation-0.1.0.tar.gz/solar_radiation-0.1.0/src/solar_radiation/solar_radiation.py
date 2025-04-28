import math
import pandas as pd
import datetime
from typing import List
from zoneinfo import ZoneInfo  # ✅ 표준 시간대 모듈

from solar_radiation.core.utils import (
    day_of_year,
    hour_angle,
)
from solar_radiation.core.solar_geometry import declination_spencer, incidence_angle
from solar_radiation.core.extraterrestrial_radiation import (
    extraterrestrial_normal_irradiance,
)


def calculate_extraterrestrial_radiation(
    latitude: float,
    longitude: float,
    start_date: datetime.date,
    end_date: datetime.date,
    time_interval: str = "1m",
    timezone: str = "UTC",  # ✅ 문자열 기반 표준시간대
    surface_tilt: float = 0.0,
    surface_azimuth: float = 0.0,
    only_daytime: bool = False,
    return_Gon: bool = False,
    return_solar_angles: bool = False,
) -> pd.DataFrame:
    """
    Returns:
      - datetime
      - G_o (always, clamped: G_o = max(G_o, 0))
      - G_on (optional)
      - solar_elevation, solar_azimuth (optional)
    """

    # === 방어 로직 ===
    if start_date > end_date:
        raise ValueError("start_date must be earlier than or equal to end_date.")

    if not (-90 <= latitude <= 90):
        raise ValueError("latitude must be between -90 and 90 degrees.")

    if not (-180 <= longitude <= 180):
        raise ValueError("longitude must be between -180 and 180 degrees.")

    if not (0 <= surface_tilt <= 180):
        raise ValueError("surface_tilt must be between 0 and 180 degrees.")

    if not (-180 <= surface_azimuth <= 180):
        raise ValueError("surface_azimuth must be between -180 and 180 degrees.")

    supported_intervals = ["1m", "5m", "15m", "30m", "1h", "4h", "12h", "1d"]
    if time_interval not in supported_intervals:
        raise ValueError(f"time_interval must be one of {supported_intervals}")

    interval_mapping = {
        "1m": datetime.timedelta(minutes=1),
        "5m": datetime.timedelta(minutes=5),
        "15m": datetime.timedelta(minutes=15),
        "30m": datetime.timedelta(minutes=30),
        "1h": datetime.timedelta(hours=1),
        "4h": datetime.timedelta(hours=4),
        "12h": datetime.timedelta(hours=12),
        "1d": datetime.timedelta(days=1),
    }
    delta = interval_mapping[time_interval]

    records = []

    current_date = start_date
    tz = ZoneInfo(timezone)  # ✅ zoneinfo 객체 생성

    while current_date <= end_date:
        n = day_of_year(current_date)
        declination = declination_spencer(n)
        Gon = extraterrestrial_normal_irradiance(n)  # 하루에 한 번만 계산

        current_time = datetime.datetime.combine(current_date, datetime.time(0, 0))
        current_time = current_time.replace(tzinfo=tz)  # ✅ local timezone 적용

        while current_time.date() == current_date:
            # 현재 시간을 UTC로 변환 후 표준 시간대 기준으로 다시 맞춘다
            standard_time = current_time.astimezone(ZoneInfo("UTC")).replace(
                tzinfo=None
            )

            omega = hour_angle(standard_time, longitude, 0)  # 표준 시간 기준으로 계산

            # Solar angles
            lat_rad = math.radians(latitude)
            dec_rad = math.radians(declination)
            ha_rad = math.radians(omega)

            cos_zenith = math.sin(lat_rad) * math.sin(dec_rad) + math.cos(
                lat_rad
            ) * math.cos(dec_rad) * math.cos(ha_rad)
            cos_zenith = max(min(cos_zenith, 1), -1)  # Clamp

            solar_elevation = math.degrees(math.asin(cos_zenith))

            if only_daytime and solar_elevation <= 0:
                current_time += delta
                continue

            if surface_tilt == 0:
                adjusted_cos_zenith = cos_zenith
            else:
                theta = incidence_angle(
                    latitude, declination, surface_tilt, surface_azimuth, omega
                )
                adjusted_cos_zenith = math.cos(math.radians(theta))
                adjusted_cos_zenith = max(adjusted_cos_zenith, 0)

            Go = Gon * adjusted_cos_zenith
            Go = max(0, Go)  # ✅ clamp

            record = {
                "datetime": current_time.replace(tzinfo=None),  # naive datetime 저장
                "G_o": Go,
            }
            if return_Gon:
                record["G_on"] = Gon
            if return_solar_angles:
                record["solar_elevation"] = solar_elevation
                record["solar_azimuth"] = None  # Future work

            records.append(record)

            current_time += delta

        current_date += datetime.timedelta(days=1)

    df = pd.DataFrame(records)
    return df
