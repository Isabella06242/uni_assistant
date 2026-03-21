from src.tools.calendar.parser import parse_date, extract_event_details
from src.tools.calendar.models import CalendarEvent

#test parse_date
print(parse_date("tomorrow at 3 pm"))
print(parse_date("today at 10:30am"))

#test extract_event_details
details = extract_event_details("Meeting with John tomorrow 2pm for 1 hour")
print(details)

#test CalendarEvent
event = CalendarEvent(
    title=details["title"],
    start_time=details["start"],
    end_time=details["end"],
    description=details["description"]
)

event.validate()
print(event.to_google_format())