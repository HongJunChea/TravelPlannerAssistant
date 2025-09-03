from dataclasses import dataclass, field
from typing import List, Self
from src.modules.trip import Trip


@dataclass
class Activity:
    date: str
    start_time: str
    end_time: str
    location: str
    detail: str
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
            "detail": self.detail,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Activity":
        return cls(
            date=data["date"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            location=data.get("location", ""),
            detail=data["detail"],
            notes=data.get("notes", "")
        )


@dataclass
class Itinerary(Trip):
    location: str = ""
    start_date: str = ""
    end_date: str = ""
    trip_type: str = ""
    activities: List[Activity] = field(default_factory=list)

    def __init__(self, trip_name: str, location: str, start_date: str, end_date: str, trip_type: str, activities: List[Activity] = None):
        super().__init__(trip_name)
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.trip_type = trip_type
        self.activities = activities if activities else []

    # ---------- Serialization ----------
    def to_dict(self) -> dict:
        return {
            "trip_name": self.trip_name,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "trip_type": self.trip_type,
            "activities": [a.to_dict() for a in self.activities]
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        activities = [Activity.from_dict(a) for a in data.get("activities", [])]
        return cls(
            trip_name=data["trip_name"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            trip_type=data["trip_type"],
            activities=activities
        )
