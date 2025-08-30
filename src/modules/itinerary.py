from dataclasses import dataclass
from typing import Self


@dataclass
class Itinerary:
    """
    Represents a full travel itinerary with trip details.
    """
    list_name: str
    trip_title: str
    location: str
    start_date: str
    end_date: str
    trip_type: str

    def to_dict(self) -> dict:
        """Convert Itinerary to dictionary (for JSON)."""
        return {
            "trip_title": self.trip_title,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "trip_type": self.trip_type,
        }

    @classmethod
    def from_dict(cls, list_name: str, data: dict) -> Self:
        """Recreate an Itinerary from dictionary."""
        return cls(
            list_name=list_name,
            trip_title=data["trip_title"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            trip_type=data["trip_type"],
        )