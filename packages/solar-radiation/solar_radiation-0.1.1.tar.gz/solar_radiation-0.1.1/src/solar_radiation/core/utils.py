# src/serc/utils.py

import math
import datetime


def day_of_year(date: datetime.date) -> int:
    """
    Convert a date into day of year (n).
    """
    return date.timetuple().tm_yday


def is_leap_year(year: int) -> bool:
    """
    Check if a year is a leap year.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_of_year_from_month_day(month: int, day: int, year: int) -> int:
    """
    Convert month and day into day of year.
    """
    date = datetime.date(year, month, day)
    return day_of_year(date)


def equation_of_time(n: int) -> float:
    """
    Calculate the equation of time (EoT) in minutes.
    Based on Spencer's formula cited by Iqbal (1983).
    """
    B = math.radians((360 / 365) * (n - 1))
    EoT = 229.18 * (
        0.000075
        + 0.001868 * math.cos(B)
        - 0.032077 * math.sin(B)
        - 0.014615 * math.cos(2 * B)
        - 0.040849 * math.sin(2 * B)
    )
    return EoT


def hour_angle(
    standard_time: datetime.datetime, longitude: float, timezone: int
) -> float:
    """
    Calculate the hour angle (ω) in degrees.
    - standard_time: local standard time (datetime)
    - longitude: observer's longitude (degrees, east positive)
    - timezone: local time zone offset from GMT (integer)
    """
    standard_minutes = (
        standard_time.hour * 60 + standard_time.minute + standard_time.second / 60
    )
    local_standard_meridian = 15 * timezone  # degrees

    n = day_of_year(standard_time.date())
    EoT = equation_of_time(n)
    time_correction = 4 * (longitude - local_standard_meridian) + EoT  # in minutes

    solar_minutes = standard_minutes + time_correction
    solar_time = solar_minutes / 60  # hours

    omega = 15 * (solar_time - 12)  # degrees
    return omega


def solar_time(
    standard_time: datetime.datetime, longitude: float, timezone: int, n: int
) -> datetime.datetime:
    """
    Convert standard time to solar time (datetime).
    """
    standard_minutes = (
        standard_time.hour * 60 + standard_time.minute + standard_time.second / 60
    )
    local_standard_meridian = 15 * timezone  # degrees
    EoT = equation_of_time(n)
    time_correction = 4 * (longitude - local_standard_meridian) + EoT  # minutes

    solar_minutes = standard_minutes + time_correction
    solar_hours = solar_minutes / 60

    hours = int(solar_hours)
    minutes = int((solar_hours - hours) * 60)
    seconds = int((((solar_hours - hours) * 60) - minutes) * 60)

    return standard_time.replace(hour=hours, minute=minutes, second=seconds)


def sunrise_sunset_hour_angle(latitude: float, declination: float) -> float:
    """
    Calculate the sunset hour angle (ωs) in degrees.
    """
    lat_rad = math.radians(latitude)
    dec_rad = math.radians(declination)

    cos_omega_s = -math.tan(lat_rad) * math.tan(dec_rad)
    cos_omega_s = max(min(cos_omega_s, 1), -1)  # Clamp to [-1, 1]

    omega_s = math.degrees(math.acos(cos_omega_s))
    return omega_s


def minutes_to_time(minutes: float) -> datetime.time:
    """
    Convert total minutes into a time object.
    """
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    secs = int((minutes - (hours * 60 + mins)) * 60)
    return datetime.time(hour=hours, minute=mins, second=secs)


def time_to_minutes(time: datetime.time) -> float:
    """
    Convert a time object into total minutes.
    """
    return time.hour * 60 + time.minute + time.second / 60
