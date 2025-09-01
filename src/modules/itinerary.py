from dataclasses import dataclass, field
from typing import List, Self

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
class Itinerary:
    list_name: str
    trip_title: str
    location: str
    start_date: str
    end_date: str
    trip_type: str
    activities: List[Activity] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "trip_title": self.trip_title,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "trip_type": self.trip_type,
            "activities": [a.to_dict() for a in self.activities]
        }

    @classmethod
    def from_dict(cls, list_name: str, data: dict) -> Self:
        activities = [Activity.from_dict(a) for a in data.get("activities", [])]
        return cls(
            list_name=list_name,
            trip_title=data["trip_title"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            trip_type=data["trip_type"],
            activities=activities
        )