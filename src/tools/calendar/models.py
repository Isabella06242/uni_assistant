#src/tools/calendar/models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class CalendarEvent:
    title: str
    start_time: datetime
    end_time: datetime
    description: str = ""

    #Convert to Google Calendar API format
    def to_google_formata(self) -> dict:
        return {
            "Summary": self.title,
            "Description": self.description,
            "Start": {
                "DateTime": self.start_time.isoformat(),
                "TimeZone": "America/New_York" #adjust timezone
            },
            "End": {
                "DateTime": self.end_time.isoformat(),
                "TimeZone": "America/New_York"
            }
        }
    
    #Validation Rules
    def validate(self):
        if not self.title:
            raise ValueError("Event must have a title")
        if self.endtime <= self.start_time:
            raise ValueError("End time must be after start time")
        return True