#  Copyright (c) 2025 Isaac Dovolsky

from unittest import TestCase
import datetime as dt
from hebrewdate import HebrewDate, HebrewYear, HebrewCalendar, HTMLHebrewCalendar


class TestHebrewYearAdditional(TestCase):

    def test_hebrew_year_creation_invalid_value(self):
        with self.assertRaises(ValueError):
            HebrewYear(0)

    def test_is_leap_year_static_method(self):
        leap_year = 5784
        non_leap_year = 5783
        self.assertTrue(HebrewYear.is_leap_year(leap_year))
        self.assertFalse(HebrewYear.is_leap_year(non_leap_year))

    def test_month_count_based_on_leap_year(self):
        leap_year = HebrewYear(5784)
        non_leap_year = HebrewYear(5783)
        self.assertEqual(leap_year.month_count, 13)
        self.assertEqual(non_leap_year.month_count, 12)

    def test_days_array_length(self):
        leap_year = HebrewYear(5784)
        non_leap_year = HebrewYear(5783)
        self.assertEqual(len(leap_year.days), 13)
        self.assertEqual(len(non_leap_year.days), 12)

    def test_total_days_in_year(self):
        leap_year = HebrewYear(5784)
        non_leap_year = HebrewYear(5783)
        self.assertTrue(isinstance(leap_year.total_days(), int))
        self.assertTrue(isinstance(non_leap_year.total_days(), int))

    def test_month_dict_keys_and_values(self):
        year = HebrewYear(5783)
        months = year.month_dict()
        self.assertEqual(len(months), len(year.months))
        for month, days in months.items():
            self.assertIn(month, year.months)
            self.assertIn(days, year.days)

    def test_new_moons_structure(self):
        year = HebrewYear(5783)
        new_moons = year.new_moons()
        self.assertEqual(len(new_moons), len(year.months))
        for month, time in new_moons.items():
            self.assertIn(month, year.months)
            self.assertTrue(isinstance(time, str))
            self.assertRegex(time, r'^\d:\d{1,2}:\d{1,4}$')

    def test_comparison_operations_between_two_years(self):
        year_1 = HebrewYear(5783)
        year_2 = HebrewYear(5784)
        self.assertTrue(year_1 < year_2)
        self.assertTrue(year_2 > year_1)
        self.assertTrue(year_1 != year_2)
        self.assertTrue(year_1 == HebrewYear(5783))

    def test_arithmetic_operations_year_addition(self):
        year = HebrewYear(5783)
        new_year = year + 1
        self.assertEqual(new_year.year, 5784)

    def test_arithmetic_operations_year_subtraction(self):
        year = HebrewYear(5783)
        previous_year = year - 1
        year_difference = year - HebrewYear(5781)
        self.assertEqual(previous_year.year, 5782)
        self.assertEqual(year_difference, 2)

    def test_len_method_on_hebrew_year(self):
        leap_year = HebrewYear(5784)
        non_leap_year = HebrewYear(5783)
        self.assertEqual(len(leap_year), 13)
        self.assertEqual(len(non_leap_year), 12)

    def test_first_new_moon_result(self):
        year = HebrewYear(5783)
        first_new_moon = year.first_new_moon()
        self.assertTrue(isinstance(first_new_moon, int))
        self.assertGreater(first_new_moon, 0)

    def test_str_and_repr_methods(self):
        year = HebrewYear(5783)
        self.assertEqual(str(year), "5783")
        self.assertEqual(repr(year), "Year(5783)")

    def test_first_weekday_calculation(self):
        year = HebrewYear(5783)
        self.assertTrue(isinstance(year.first_weekday, int))
        self.assertIn(year.first_weekday, range(0, 7))


class TestHebrewDate(TestCase):

    def test_hebrew_date_initialization(self):
        hebrew_date = HebrewDate(1, 1, 5785)
        self.assertEqual(hebrew_date.day_numeric, 1)
        self.assertEqual(hebrew_date.month_numeric, 1)
        self.assertEqual(hebrew_date.year_numeric, 5785)

    def test_hebrew_date_repr(self):
        hebrew_date = HebrewDate(1, 1, 5785)
        self.assertTrue(isinstance(repr(hebrew_date), str))

    def test_hebrew_date_str(self):
        hebrew_date = HebrewDate(1, "תשרי", 5785)
        self.assertTrue(isinstance(str(hebrew_date), str))

    def test_hebrew_date_to_int(self):
        hebrew_date = HebrewDate(1, 1, 5785)
        self.assertTrue(isinstance(int(hebrew_date), int))

    def test_comparison_operations(self):
        hebrew_date1 = HebrewDate(1, 1, 5785)
        hebrew_date2 = HebrewDate(2, 1, 5785)
        self.assertTrue(hebrew_date1 < hebrew_date2)
        self.assertTrue(hebrew_date1 <= hebrew_date2)
        self.assertTrue(hebrew_date2 > hebrew_date1)
        self.assertTrue(hebrew_date2 >= hebrew_date1)
        self.assertTrue(hebrew_date1 != hebrew_date2)
        hebrew_date3 = HebrewDate(1, 1, 5785)
        self.assertTrue(hebrew_date1 == hebrew_date3)

    def test_addition_operation(self):
        hebrew_date = HebrewDate(1, 1, 5785)
        result_date = hebrew_date + 1
        self.assertEqual(result_date.day_numeric, 2)

    def test_subtraction_operation_with_int(self):
        hebrew_date = HebrewDate(2, 1, 5785)
        result_date = hebrew_date - 1
        self.assertEqual(result_date.day_numeric, 1)

    def test_subtraction_operation_with_other_hebrew_date(self):
        hebrew_date1 = HebrewDate(2, 1, 5785)
        hebrew_date2 = HebrewDate(1, 1, 5785)
        difference = hebrew_date1 - hebrew_date2
        self.assertEqual(difference, 1)

    def test_get_month(self):
        hebrew_date = HebrewDate(1, "ניסן", 5785)
        month_numeric, month_name = hebrew_date.get_month()
        self.assertEqual(month_numeric, 7)
        self.assertEqual(month_name, "ניסן")

    def test_get_day(self):
        hebrew_date = HebrewDate(3, "ניסן", 5785)
        day_numeric, day_name = hebrew_date.get_day()
        self.assertEqual(day_numeric, 3)
        self.assertTrue(isinstance(day_name, str))

    def test_get_weekday(self):
        hebrew_date = HebrewDate(1, "ניסן", 5785)
        weekday_numeric, weekday_name = hebrew_date.get_weekday()
        self.assertTrue(0 <= weekday_numeric <= 6)
        self.assertTrue(isinstance(weekday_name, str))

    def test_days_before(self):
        hebrew_date = HebrewDate(15, "תשרי", 5785)
        days_before = hebrew_date.days_before()
        self.assertTrue(isinstance(days_before, int))

    def test_days_after(self):
        hebrew_date = HebrewDate(15, "תשרי", 5785)
        days_after = hebrew_date.days_after()
        self.assertTrue(isinstance(days_after, int))

    def test_delta_method(self):
        hebrew_date = HebrewDate(1, 1, 5785)
        result_date = hebrew_date.delta(days=1, months=1, years=1)
        self.assertTrue(isinstance(result_date, HebrewDate))
        self.assertNotEqual(result_date.year_numeric, hebrew_date.year_numeric)

    def test_from_gregorian(self):
        hebrew_date = HebrewDate.from_gregorian(day=1, month=1, year=2024)
        self.assertTrue(isinstance(hebrew_date, HebrewDate))
        with self.assertWarns(RuntimeWarning) as w:
            HebrewDate.from_gregorian(day=1, month=1, year=1)
        self.assertEqual(str(w.warning), "Hebrew dates may be inaccurate for years earlier than 1752.")

    def test_to_gregorian(self):
        hebrew_date_valid = HebrewDate(1, 1, 5785)
        hebrew_date_warn = HebrewDate(1, 1, 5000)
        hebrew_date_invalid = HebrewDate(1, 1, 2000)
        gregorian_date_valid = hebrew_date_valid.to_gregorian()
        self.assertTrue(isinstance(gregorian_date_valid, dt.date))
        with self.assertWarns(RuntimeWarning) as w:
            hebrew_date_warn.to_gregorian()
        self.assertEqual(str(w.warning), "Hebrew dates may be inaccurate for years earlier than 1752.")
        with self.assertWarns(RuntimeWarning) as w:
            hebrew_date_invalid.to_gregorian()
        self.assertEqual(str(w.warning), "The Hebrew date is too far in the past to convert to a Gregorian date.")

    def test_today_method(self):
        hebrew_date = HebrewDate.today()
        self.assertTrue(isinstance(hebrew_date, HebrewDate))

class TestHebrewCalendar(TestCase):

    def test_itermonthdays_produces_correct_day_numbers(self):
        calendar = HebrewCalendar(firstweekday=0)
        year = 5785
        month = 1  # Assuming the first Hebrew month
        days = list(calendar.itermonthdays(year, month))
        self.assertTrue(all(isinstance(day, int) for day in days))
        self.assertEqual(days.count(0), days[0:(7 - days[0] % 7)].count(0))

    def test_itermonthdays_include_zeros_correctly(self):
        calendar = HebrewCalendar()
        year = 5785
        month = 2
        days = list(calendar.itermonthdays(year, month))
        self.assertIn(0, days)  # Ensure zeros are included before and after the month's days

    def test_itermonthdays2gregorian_returns_correct_tuple_format(self):
        calendar = HebrewCalendar()
        year = 5785
        month = 1
        days = list(calendar.itermonthdays2gregorian(year, month))
        self.assertTrue(all(len(day_tuple) == 3 for day_tuple in days))
        self.assertTrue(all(isinstance(day_tuple[0], int) for day_tuple in days))
        self.assertTrue(all(isinstance(day_tuple[1], int) for day_tuple in days))
        self.assertTrue(all(isinstance(day_tuple[2], str) or day_tuple[2] == "" for day_tuple in days))

    def test_monthdays2calendar_returns_correct_matrix_size(self):
        calendar = HebrewCalendar()
        year = 5785
        month = 1
        matrix = calendar.monthdays2calendar(year, month)
        self.assertTrue(all(len(week) == 7 for week in matrix))
        self.assertEqual(len(matrix) * 7, len([day for week in matrix for day in week]))

    def test_monthdays2calendar_with_gregorian_flag(self):
        calendar = HebrewCalendar()
        year = 5785
        month = 1
        matrix_with_gregorian = calendar.monthdays2calendar(year, month, with_gregorian=True)
        self.assertTrue(all(len(week) == 7 for week in matrix_with_gregorian))
        self.assertTrue(all(len(day_tuple) == 3 for week in matrix_with_gregorian for day_tuple in week))

class TestHTMLHebrewCalendar(TestCase):

    def test_formatmonth_with_hebrew_year(self):
        calendar = HTMLHebrewCalendar(firstweekday=0)
        result = calendar.formatmonth(5785, 1)
        self.assertIn('<table dir="rtl', result)
        self.assertIn('תשרי 5785', result)

    def test_formatmonth_with_gregorian_dates(self):
        calendar = HTMLHebrewCalendar(firstweekday=0)
        result = calendar.formatmonth(5785, 1, with_gregorian=True)
        self.assertIn('October-November', result)

    def test_formatday_outside_month(self):
        calendar = HTMLHebrewCalendar(firstweekday=0)
        result = calendar.formatday(0, 0)
        self.assertEqual(result, '<td class="noday">&nbsp;</td>')
