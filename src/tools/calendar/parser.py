from datetime import datetime, timedelta
from dateutil import parser as dateutil_parser
import re
from src.tools.calendar.models import CalendarEvent

#convert natural language to datetime
def parse_date(text: str) -> datetime:
    text = text.lower().strip()
    now = datetime.now()

    #handling relative days
    if text.startswith("tomorrow"):
        base = now + timedelta(days = 1)
        #strip out the day word and extract time part
        time_part = text.replace("tomorrow", "").strip().lstrip("at").strip()
        if time_part:
            t = dateutil_parser.parse(time_part)
            return base.replace(hour = t.hour, minute = t.minute, second = 0, microsecond = 0)
        return base
    
    if text.startswith("today"):
        base = now
        time_part = text.replace("today", "").strip().lstrip("at").strip()
        if time_part:
            t = dateutil_parser.parse(time_part)
            return base.replace(hour = t.hour, minute = t.minute, second = 0, microsecond = 0)
        return base
    
    #fallback
    return dateutil_parser.parse(text, default = now)

#convert natural language into event details for api
def extract_event_details(command: str) -> dict:
    now = datetime.now()
    
    #extract duration (for 1 hour, for 30 minutes)
    duration_minutes = 60 #default
    duration_match = re.search(r'for (\d+)\s*(hour|hr|minute|min)s?', command, re.IGNORECASE)
    if duration_match:
        amount = int(duration_match.group(1))
        unit = duration_match.group(2).lower()
        duration_minutes = amount * 60 if "hour" in unit or "hr" in unit else amount
    
    #extract date/time 
    start_time = now
    for keyword in ["tomorrow", "today", "monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
        if keyword in command.lower():
            #extract time (2 pm, 10:30 am, 11 pm)
            time_match = re.search(r'(\d{1,2}(?::\d{2})?\s*[ap]m)', command, re.IGNORECASE)
            #extract date
            date_str = keyword
            if time_match:
                date_str += " at "  + time_match.group(1)
            start_time = parse_date(date_str)
            break
    
    end_time = start_time + timedelta(minutes = duration_minutes)

    #extract title
    title = command
    #deletes time + duration from title
    title = re.sub(r'for \d+\s*(hour|hr|minute|min)s?', '', title, flags=re.IGNORECASE)
    title = re.sub(r'\d{1,2}(?::\d{2})?\s*[ap]m', '', title, flags=re.IGNORECASE)
    #delete date from title
    for k in ["tomorrow", "today", "monday","tuesday","wednesday","thursday","friday","saturday","sunday"]:
        title = re.sub(k, '', title, flags = re.IGNORECASE)
    #clean up
    title = re.sub(r'\s+', ' ', title).strip().strip("at").strip()

    return {
        "title": title,
        "start": start_time,
        "end": end_time,
        "description": ""
    }