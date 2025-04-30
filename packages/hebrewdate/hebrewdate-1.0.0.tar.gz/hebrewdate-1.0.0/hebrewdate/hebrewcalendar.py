"""
This module provides Hebrew calendar functionality with both text and HTML representations.
It extends the standard calendar module to support Hebrew dates and formatting.
"""
#  Copyright (c) 2025 Isaac Dovolsky

import sys
import calendar
from itertools import repeat
from calendar import HTMLCalendar
from .hebrewyear import HebrewYear
from .hebrewdate import HebrewDate, _validate_month, WEEKDAYS, HEBREW_DAYS


class HebrewCalendar(calendar.Calendar):
    """
    A calendar class for working with Hebrew dates.
    
    This class extends the standard Calendar class to provide Hebrew calendar functionality,
    including methods for iterating over month days and converting between Hebrew and 
    Gregorian dates.
    
    Attributes:
    -----------
    **firstweekday**: ``int``
        Specifies the first day of the week (1 = Sunday, default)
    """

    def __init__(self, firstweekday: int = 1):
        super().__init__(firstweekday)

    def itermonthdays(self, year, month):
        """
        Like itermonthdates(), but will yield day numbers. For days outside
        the specified month the day number is 0.
        """
        date = HebrewDate(month=month, year=year)
        day1, n_days = date.weekday_numeric, date.year.days[month - 1]
        days_before = (day1 - self.firstweekday) % 7
        yield from repeat(0, days_before)
        yield from range(1, n_days + 1)
        days_after = (self.firstweekday - day1 - n_days) % 7
        yield from repeat(0, days_after)

    def itermonthdays2gregorian(self, year, month):
        """
        Like itermonthdays(), but yields (day, weekday, gregorian_date) tuples.
        """
        for day, weekday in self.itermonthdays2(year, month):
            if day != 0:
                date = HebrewDate(day, month, year).to_gregorian().strftime("%d")
            else:
                date = ""
            yield day, weekday, date

    def monthdays2calendar(self, year, month, with_gregorian=False):
        """
        Return a matrix representing a month's calendar.
        Each row represents a week; week entries are
        (day number, weekday number) tuples. Day numbers outside this month
        are zero.
        """
        if with_gregorian:
            days = list(self.itermonthdays2gregorian(year, month))
        else:
            days = list(self.itermonthdays2(year, month))
        return [days[i:i + 7] for i in range(0, len(days), 7)]


class HTMLHebrewCalendar(HebrewCalendar, HTMLCalendar):
    """
    HTML representation of the Hebrew calendar.
    
    This class combines HebrewCalendar and HTMLCalendar to provide HTML formatting
    of Hebrew calendar data. It supports both Hebrew and Gregorian date display,
    custom CSS styling, and various formatting options for days, weeks, months,
    and complete years.
    
    The calendar is formatted right-to-left (RTL) to match the Hebrew calendar structure
    and includes both Hebrew and optional Gregorian date representations.

    Attributes:
    -----------
    **firstweekday**: ``int``
        Specifies the first day of the week (1 = Sunday, default)
    """

    def __init__(self, firstweekday=1):
        HebrewCalendar.__init__(self, firstweekday)
        HTMLCalendar.__init__(self, firstweekday)

    def formatday(self, day, weekday, gregorian_day=None):
        """
        Return a day as a table cell.
        """
        if day == 0:
            # day outside month
            return f'<td class="{self.cssclass_noday}">&nbsp;</td>'
        elif gregorian_day:
            return f'<td class="{self.cssclasses[weekday]}">{HEBREW_DAYS[day - 1]}\n{gregorian_day}</td>'
        else:
            return f'<td class="{self.cssclasses[weekday]}">{HEBREW_DAYS[day - 1]}</td>'

    def formatweek(self, week, with_gregorian=False):
        """
        Return a complete week as a table row.
        """
        if with_gregorian:
            s = ''.join(self.formatday(d, wd, g) for (d, wd, g) in week)
        else:
            s = ''.join(self.formatday(d, wd) for (d, wd) in week)
        return f'<tr>{s}</tr>'

    def formatweekday(self, day):
        """
        Return a weekday name as a table header.
        """
        return f'<th class="{self.cssclasses_weekday_head[day]}">{WEEKDAYS[day]}</th>'

    def formatmonthname(self, year, month, with_year=True, with_gregorian=False):
        """
        Return a month name as a table row.
        """
        _validate_month(month, year)
        h_year = HebrewYear(year)
        if with_gregorian:
            start = HebrewDate(month=month, year=year)
            end = (start + h_year.days[month - 1]).to_gregorian().strftime("%B")
            start = start.to_gregorian()
            g_year = start.year
            start = start.strftime('%B')
            gm = f'{start}-{end}' if start != end else start
            if with_year:
                s = f'{h_year.months[month - 1]} {year}\n{gm} {g_year}'
            else:
                s = f'{h_year.months[month - 1]}\n{gm}'
        else:
            if with_year:
                s = f'{h_year.months[month - 1]} {year}'
            else:
                s = h_year.months[month - 1]
        return f'<tr><th colspan="7" class="{self.cssclass_month_head}">{s}</th></tr>'

    def formatmonth(self, year, month, with_year=True, with_gregorian=False):
        """
        Return a formatted month as a table.
        """
        v = []
        a = v.append
        a(f'<table dir="rtl" border="0" cellpadding="0" cellspacing="0" class="{self.cssclass_month}">')
        a('\n')
        a(self.formatmonthname(year, month, with_year, with_gregorian))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(year, month, with_gregorian):
            a(self.formatweek(week, with_gregorian))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)

    def formatyear(self, year, width=3, with_gregorian=False):
        """
        Return a formatted year as a table of tables.
        """
        v = []
        a = v.append
        width = max(width, 1)
        a(f'<table dir="rtl" border="0" cellpadding="0" cellspacing="0" class="{self.cssclass_year}">')
        a('\n')
        a(f'<tr><th colspan="{width}" class="{self.cssclass_year_head}">{year}</th></tr>')
        for i in range(1, HebrewYear(year).month_count + 1, width):
            # months in this row
            months = range(i, min(i + width, 14))
            a('<tr>')
            for m in months:
                a('<td>')
                a(self.formatmonth(year, m, False, with_gregorian))
                a('</td>')
                a('</td>')
            a('</tr>')
        a('</table>')
        return ''.join(v)

    def formatyearpage(self, year, width=3, css="calendar.css", encoding=None, with_gregorian=False):
        """
        Return a formatted year as a complete HTML page.
        """
        if encoding is None:
            encoding = sys.getdefaultencoding()
        v = []
        a = v.append
        a(f'<?xml version="1.0" encoding="{encoding}"?>\n')
        a('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
        a('<html>\n')
        a('<head>\n')
        a(f'<meta http-equiv="Content-Type" content="text/html; charset={encoding}" />\n')
        if css is not None:
            a(f'<link rel="stylesheet" type="text/css" href="{css}" />\n')
        a(f'<title>Calendar for {year}</title>\n')
        a('</head>\n')
        a('<body>\n')
        a(self.formatyear(year, width, with_gregorian))
        a('</body>\n')
        a('</html>\n')
        return ''.join(v).encode(encoding, "xmlcharrefreplace")
