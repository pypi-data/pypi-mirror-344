# src/serc/solar_geometry.py

import math


def declination_cooper(n: int) -> float:
    """
    Calculate solar declination (δ) using Cooper's approximate formula.

    δ = 23.45 * sin(360/365 * (284 + n))

    Parameters:
    - n: day of year (1 ~ 365)

    Returns:
    - Declination angle δ in degrees
    """
    return 23.45 * math.sin(math.radians((360 / 365) * (284 + n)))


def declination_spencer(n: int) -> float:
    """
    Calculate solar declination (δ) using Spencer's high-accuracy formula.
    (error < 0.035°)

    δ = (180/π) * (0.006918
                  - 0.399912 cos(B)
                  + 0.070257 sin(B)
                  - 0.006758 cos(2B)
                  + 0.000907 sin(2B)
                  - 0.002697 cos(3B)
                  + 0.00148 sin(3B))

    Parameters:
    - n: day of year (1 ~ 365)

    Returns:
    - Declination angle δ in degrees
    """
    B = math.radians((360 / 365) * (n - 1))

    delta = (
        0.006918
        - 0.399912 * math.cos(B)
        + 0.070257 * math.sin(B)
        - 0.006758 * math.cos(2 * B)
        + 0.000907 * math.sin(2 * B)
        - 0.002697 * math.cos(3 * B)
        + 0.00148 * math.sin(3 * B)
    )

    return math.degrees(delta)


# src/serc/solar_geometry.py


def incidence_angle(
    latitude: float,
    declination: float,
    slope: float,
    surface_azimuth: float,
    hour_angle: float,
) -> float:
    """
    Calculate the angle of incidence θ of beam radiation on a tilted surface.

    Parameters:
    - latitude: observer latitude (degrees)
    - declination: solar declination (degrees)
    - slope: tilt of the surface from horizontal (degrees)
    - surface_azimuth: surface azimuth angle from south (degrees, positive westward)
    - hour_angle: solar hour angle (degrees)

    Returns:
    - θ (degrees)
    """
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)
    slope_rad = math.radians(slope)
    surf_az_rad = math.radians(surface_azimuth)
    ha_rad = math.radians(hour_angle)

    cos_theta = (
        math.sin(dec_rad) * math.sin(lat_rad) * math.cos(slope_rad)
        - math.sin(dec_rad)
        * math.cos(lat_rad)
        * math.sin(slope_rad)
        * math.cos(surf_az_rad)
        + math.cos(dec_rad) * math.cos(lat_rad) * math.cos(slope_rad) * math.cos(ha_rad)
        + math.cos(dec_rad)
        * math.sin(lat_rad)
        * math.sin(slope_rad)
        * math.cos(surf_az_rad)
        * math.cos(ha_rad)
        + math.cos(dec_rad)
        * math.sin(slope_rad)
        * math.sin(surf_az_rad)
        * math.sin(ha_rad)
    )

    cos_theta = max(min(cos_theta, 1), -1)  # 안전하게 -1~1 범위 제한

    theta = math.degrees(math.acos(cos_theta))
    return theta
