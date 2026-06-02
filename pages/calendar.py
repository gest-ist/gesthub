from __future__ import annotations

import calendar
import logging
import threading
import time
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, time as datetime_time, timedelta

import recurring_ical_events
from django.conf import settings
from django.utils import timezone
from icalendar import Calendar

logger = logging.getLogger(__name__)

_calendar = None
_last_refresh_attempt = None
# It's fine to not use a lock here. We'll improve this if ever needed.
_started = False


@dataclass(frozen=True)
class CalendarEvent:
    title: str
    start: datetime
    end: datetime
    all_day: bool
    location: str

    @property
    def time_range(self) -> str:
        return "" if self.all_day else f"{_format_time(self.start)}—{_format_time(self.end)}"

    @property
    def details(self) -> str:
        return " · ".join(part for part in (self.time_range, self.location) if part)


@dataclass(frozen=True)
class CalendarState:
    calendar: Calendar
    loaded_at: datetime


def get_calendar():
    if _should_refresh():
        refresh_once()
    return _calendar


def start_calendar_refresh():
    global _started
    if _started:
        return

    _started = True
    thread = threading.Thread(target=_refresh_loop, daemon=True)
    thread.start()


def refresh_once():
    global _calendar, _last_refresh_attempt

    if not settings.CALENDAR_ICAL_URL:
        logger.warning("CALENDAR_ICAL_URL is not configured")
        return

    _last_refresh_attempt = timezone.now()
    try:
        request = urllib.request.Request(
            settings.CALENDAR_ICAL_URL, headers={"User-Agent": "GEST website"}
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            raw_calendar = response.read()

        _calendar = CalendarState(
            calendar=Calendar.from_ical(raw_calendar), loaded_at=timezone.now()
        )
    except Exception:
        logger.warning("Calendar refresh failed", exc_info=True)


def _refresh_loop():
    while True:
        refresh_once()
        time.sleep(settings.CALENDAR_REFRESH_SECONDS)


def _should_refresh():
    if not settings.CALENDAR_ICAL_URL:
        return False

    if _calendar is None:
        return True

    now = timezone.now()
    refresh_interval = timedelta(seconds=settings.CALENDAR_REFRESH_SECONDS)
    if _last_refresh_attempt is not None and now - _last_refresh_attempt < refresh_interval:
        return False
    return now - _calendar.loaded_at >= refresh_interval


def month_context(year: int, month: int, state: CalendarState | None = None):
    state = state or get_calendar()
    if state is None:
        return {"calendar_available": False}

    previous_month = month - 1 or 12
    previous_year = year - 1 if month == 1 else year
    next_month = month + 1 if month < 12 else 1
    next_year = year + 1 if month == 12 else year

    return {
        "calendar_available": True,
        "month_name_key": f"month-{month}",
        "year": year,
        "weeks": _month_days(year, month, _month_events(state, year, month)),
        "previous_month": previous_month,
        "previous_year": previous_year,
        "next_month": next_month,
        "next_year": next_year,
    }


def _value_datetime(value) -> datetime | None:
    if value is not None:
        match value.dt:
            case datetime() as raw:
                return (
                    timezone.make_aware(raw)
                    if timezone.is_naive(raw)
                    else raw.astimezone(timezone.get_current_timezone())
                )
            case date() as raw:
                return timezone.make_aware(datetime.combine(raw, datetime_time.min))


def _month_days(year: int, month: int, events):
    weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
    return [
        [
            {
                "date": day,
                "current_month": day.month == month,
                "events": _events_for_day(day, events),
            }
            for day in week
        ]
        for week in weeks
    ]


def _month_events(state: CalendarState, year: int, month: int):
    start = timezone.make_aware(datetime.combine(date(year, month, 1), datetime_time.min))
    next_month = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    end = timezone.make_aware(datetime.combine(next_month, datetime_time.min))
    events = []

    for component in recurring_ical_events.of(state.calendar).between(start, end):
        summary = str(component.get("summary", "")).strip()
        location = str(component.get("location", "")).strip()
        event_start = _value_datetime(component.get("dtstart"))
        event_end = _value_datetime(component.get("dtend"))
        if event_start is None:
            continue

        all_day = not isinstance(component.get("dtstart").dt, datetime)
        if event_end is None:
            event_end = event_start + (timedelta(days=1) if all_day else timedelta(hours=1))

        events.append(
            CalendarEvent(
                title=summary or "Evento",
                start=event_start,
                end=event_end,
                all_day=all_day,
                location=location,
            )
        )

    return events


def _format_time(value: datetime) -> str:
    return f"{value.hour}h{value.minute:02d}"


def _events_for_day(day: date, events):
    day_start = timezone.make_aware(datetime.combine(day, datetime_time.min))
    day_end = day_start + timedelta(days=1)
    return [event for event in events if event.start < day_end and event.end > day_start]
