#!/usr/bin/env python3
"""Download public iCalendar feeds into static snapshots for the GitHub Pages calendar."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote
import sys

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DATA.mkdir(parents=True, exist_ok=True)

CALENDARS = [
    ("all-church.ics", "https://calendar.google.com/calendar/ical/" + quote("5feb8669918e0c65e45c6debb6dc344a824f7d4bbe53887150df9bf8ed5596e2@group.calendar.google.com", safe="") + "/public/basic.ics"),
    ("district.ics", "https://calendar.google.com/calendar/ical/" + quote("9d0718947251b0ecb937d26521e006c9e458155a8b0542442996ae64112a513e@group.calendar.google.com", safe="") + "/public/basic.ics"),
    ("student-workers.ics", "https://calendar.google.com/calendar/ical/" + quote("144b428f9fda4934be111d528e42fd6e831abf7880aca0b94576a6f449b5fb60@group.calendar.google.com", safe="") + "/public/basic.ics"),
    ("weekday-student-meeting.ics", "https://calendar.google.com/calendar/ical/" + quote("6d5e78d1ae879ea7dd573f6193354eae02b085523b874cb0fb30b3736cd6e322@group.calendar.google.com", safe="") + "/public/basic.ics"),
    ("student-birthdays.ics", "https://calendar.google.com/calendar/ical/" + quote("640bce4eda2a30e86dfe565dee12ac630bdc9454004d219e3ab359682f722bfe@group.calendar.google.com", safe="") + "/public/basic.ics"),
    ("student-gatherings.ics", "https://calendar.google.com/calendar/ical/" + quote("0e5684c7eea55390ead078357f529444010f25599c092a48717bdb6bcbbb217d@group.calendar.google.com", safe="") + "/public/basic.ics"),
    ("hk-holidays.ics", "https://www.1823.gov.hk/common/ical/gc/tc.ics"),
]

success = 0
failed = []
for filename, url in CALENDARS:
    target = DATA / filename
    try:
        req = Request(url, headers={"User-Agent": "ChurchCalendarStaticSnapshot/1.0"})
        with urlopen(req, timeout=25) as response:
            body = response.read()
        if b"BEGIN:VCALENDAR" not in body:
            raise ValueError("response is not an iCalendar feed")
        # Only replace an existing snapshot after validating the new download.
        target.write_bytes(body)
        print(f"UPDATED {filename}: {len(body)} bytes")
        success += 1
    except Exception as exc:
        print(f"WARNING {filename}: {exc}")
        failed.append(filename)

print(f"Summary: {success}/{len(CALENDARS)} feeds downloaded successfully.")
if failed:
    print("Feeds that could not be refreshed: " + ", ".join(failed))
if success == 0:
    # Keep the action from committing an empty/invalid update.
    sys.exit("No public calendar feeds could be downloaded. Check that the calendars are public.")
