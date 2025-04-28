# src/serc/extraterrestrial_radiation.py

import math

from .solar_geometry import declination_spencer
from .utils import equation_of_time, sunrise_sunset_hour_angle


def extraterrestrial_normal_irradiance(n: int) -> float:
    """
    Calculate extraterrestrial normal irradiance (Gon) in W/m².

    Parameters:
    - n: day of year (1 ~ 365)

    Returns:
    - Gon in W/m²
    """
    Gsc = 1367  # Solar constant in W/m²
    return Gsc * (1 + 0.033 * math.cos(math.radians(360 * n / 365)))


def extraterrestrial_horizontal_irradiance(
    latitude: float, n: int, hour_angle: float
) -> float:
    """
    Calculate instantaneous extraterrestrial irradiance on a horizontal plane (Go) in W/m².

    Parameters:
    - latitude: location latitude in degrees (north positive)
    - n: day of year
    - hour_angle: hour angle (ω) in degrees

    Returns:
    - Go in W/m²
    """
    declination = declination_spencer(n)
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    ha_rad = math.radians(hour_angle)

    cos_zenith = math.sin(lat_rad) * math.sin(dec_rad) + math.cos(lat_rad) * math.cos(
        dec_rad
    ) * math.cos(ha_rad)
    cos_zenith = max(cos_zenith, 0)  # 햇빛 없는 시간대에서는 0 처리

    Gon = extraterrestrial_normal_irradiance(n)
    Go = Gon * cos_zenith
    return Go


def hourly_extraterrestrial_radiation(
    latitude: float, n: int, omega1: float, omega2: float
) -> float:
    """
    Calculate extraterrestrial radiation (Io) over an hour period in J/m².

    Parameters:
    - latitude: location latitude in degrees
    - n: day of year
    - omega1: start hour angle in degrees
    - omega2: end hour angle in degrees

    Returns:
    - Io in J/m²
    """
    Gsc = 1367  # Solar constant in W/m²
    declination = declination_spencer(n)

    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    omega1_rad = math.radians(omega1)
    omega2_rad = math.radians(omega2)

    factor = math.sin(lat_rad) * math.sin(dec_rad)
    term = math.cos(lat_rad) * math.cos(dec_rad)

    Io = (
        (12 * 3600 / math.pi)
        * Gsc
        * (1 + 0.033 * math.cos(math.radians(360 * n / 365)))
        * (
            factor * (omega2_rad - omega1_rad)
            + term * (math.sin(omega2_rad) - math.sin(omega1_rad))
        )
    )
    return Io


def daily_extraterrestrial_radiation(latitude: float, n: int) -> float:
    """
    Calculate daily extraterrestrial radiation on a horizontal surface (Ho) in J/m²/day.

    Parameters:
    - latitude: location latitude in degrees
    - n: day of year

    Returns:
    - Ho in J/m²/day
    """
    Gsc = 1367  # Solar constant in W/m²
    declination = declination_spencer(n)
    ws = sunrise_sunset_hour_angle(
        latitude, declination
    )  # Sunset hour angle in degrees

    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    ws_rad = math.radians(ws)

    Ho = (
        (24 * 3600 / math.pi)
        * Gsc
        * (1 + 0.033 * math.cos(math.radians(360 * n / 365)))
        * (
            math.cos(lat_rad) * math.cos(dec_rad) * math.sin(ws_rad)
            + ws_rad * math.sin(lat_rad) * math.sin(dec_rad)
        )
    )
    return Ho
