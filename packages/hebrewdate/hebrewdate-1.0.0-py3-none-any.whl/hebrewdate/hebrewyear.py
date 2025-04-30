"""
This module provides the HebrewYear class, which represents the Hebrew calendar year.

The class includes methods for determining if a year is a leap year, calculating the total
number of days in a year, computing the individual months and their lengths, and determining
the first weekday of the year. Additionally, it calculates the schedule of new moons and supports
operations such as year arithmetic and comparisons.
"""
#  Copyright (c) 2025 Isaac Dovolsky

from __future__ import annotations

FIRST_NEW_MOON = 57444  # First new moon time in parts
NEW_MOON_INTERVAL = 765433  # Interval between new moons in parts
INVALID_FIRST_DAYS = {1, 4, 6}  # Invalid first days of the Hebrew year
LEAP_YEARS = {0, 3, 6, 8, 11, 14, 17}  # 0 instead of 19 due to modular calculation

# Standard and Leap Year Month Lengths
STANDARD_MONTHS = {
    "תשרי": 30, "חשוון": 29, "כסלו": 30, "טבת": 29, "שבט": 30, "אדר": 29,
    "ניסן": 30, "אייר": 29, "סיוון": 30, "תמוז": 29, "אב": 30, "אלול": 29
}
LEAP_MONTHS = {
    "תשרי": 30, "חשוון": 29, "כסלו": 30, "טבת": 29, "שבט": 30, "אדר א": 30,
    "אדר ב": 29, "ניסן": 30, "אייר": 29, "סיוון": 30, "תמוז": 29, "אב": 30,
    "אלול": 29
}

class HebrewYear:
    """
    Represents a Hebrew year, handling leap years and calendar calculations.

    Attributes:
    -----------
    **year**: ``int``
        Numeric value of the Hebrew year.
    **is_leap**: ``bool``
        Whether the year is a leap year.
    **months**: ``list[str]``
        A list of month names for the year, adjusted for leap years.
    **days**: ``list[int]``
        Number of days in each month in the year.
    **month_count**: ``int``
        Number of months in the year (12 or 13 for leap years).
    **first_weekday**: ``int``
        Numeric representation of the first weekday of the year (0-6, where 0 is שבת for calculation purposes).
    """

    def __init__(self, year: int):
        if year < 1:
            raise ValueError("Invalid year")
        self.year = year
        self.is_leap = self.is_leap_year(self.year)
        index = LEAP_MONTHS if self.is_leap else STANDARD_MONTHS
        self.months = list(index.keys())
        self.days = list(index.values())
        self.month_count = 13 if self.is_leap else 12
        self.first_weekday = self._first_weekday()
        self._calculate_days()

    def __repr__(self) -> str:
        return f"Year({self.year})"

    def __str__(self) -> str:
        return str(self.year)

    def __int__(self) -> int:
        return self.year

    def __eq__(self, other: int | HebrewYear) -> bool:
        return self.year == int(other)

    def __ne__(self, other: int | HebrewYear) -> bool:
        return self.year != int(other)

    def __gt__(self, other: int | HebrewYear) -> bool:
        return self.year > int(other)

    def __lt__(self, other: int | HebrewYear) -> bool:
        return self.year < int(other)

    def __ge__(self, other: int | HebrewYear) -> bool:
        return self.year >= int(other)

    def __le__(self, other: int | HebrewYear) -> bool:
        return self.year <= int(other)

    def __len__(self) -> int:
        return self.month_count

    def __add__(self, other: int) -> HebrewYear:
        if isinstance(other, int):
            return HebrewYear(self.year + other)
        raise ValueError(f"Unsupported operand type(s) for +: 'Year' and {type(other).__name__}")

    def __sub__(self, other: int | HebrewYear) -> int | HebrewYear:
        if isinstance(other, int):
            return HebrewYear(self.year - other)
        if isinstance(other, HebrewYear):
            return self.year - other.year
        raise ValueError(f"Unsupported operand type(s) for -: 'Year' and {type(other).__name__}")

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 19 in LEAP_YEARS

    def total_days(self) -> int:
        return sum(self.days)

    def month_dict(self) -> dict[str, int]:
        return dict(zip(self.months, self.days))

    def new_moons(self) -> dict[str, str]:
        """ Return a dictionary of new moons for each month. """
        first_new_moon = self.first_new_moon() % 181440  # 7 * 24 * 1080 = 181440
        return {
            self.months[month]: (
                f'{(month * NEW_MOON_INTERVAL + first_new_moon) // 1080 // 24 % 7}:'
                f'{(month * NEW_MOON_INTERVAL + first_new_moon) // 1080 % 24}:'
                f'{(month * NEW_MOON_INTERVAL + first_new_moon) % 1080}'
            )
            for month in range(self.month_count)
        }

    def first_new_moon(self, year: int = None) -> int:
        """ Returns the time of the first new moon of the year (in parts) """
        year = (self.year if year is None else year) - 1
        # Number of leap years up to current year
        leap_years = (year // 19) * 7 + sum(1 for j in LEAP_YEARS if j <= year % 19 and j != 0)
        # Total new moons up to first new moon of the current year
        return (year * 12 + leap_years) * NEW_MOON_INTERVAL + FIRST_NEW_MOON

    def _first_weekday(self, year: int = None) -> int:
        """ Calculates the first weekday of the year. """
        year = self.year if year is None else year
        first_nm = self.first_new_moon(year)
        first_nmh = (first_nm // 1080) % 24
        first_day = (first_nm // 1080 // 24) % 7
        if first_day == 2 and self.is_leap_year(year - 1):
            if first_nmh == 15 and first_nm % 1080 >= 589 or first_nmh >= 16:
                first_day = 3
        elif first_day == 3 and not self.is_leap_year(year):
            if first_nmh == 9 and first_nm % 1080 >= 204 or first_nmh >= 10:
                first_day = 5
        elif first_nmh >= 18:
            first_day = (first_day + 1) % 7
        if first_day in INVALID_FIRST_DAYS:
            first_day = (first_day + 1) % 7
        return first_day

    def _calculate_days(self):
        """ Calculates the number of days in Heshvan and Kislev """
        if self.first_weekday != 3:
            next_theoretical = (self.total_days() + self.first_weekday) % 7
            next_actual = self._first_weekday(self.year + 1)
            if next_theoretical < next_actual or next_theoretical == 6 and next_actual == 0:
                self.days[1] = 30
            elif next_theoretical > next_actual or next_theoretical == 0 and next_actual == 1:
                self.days[1] = self.days[2] = 29
