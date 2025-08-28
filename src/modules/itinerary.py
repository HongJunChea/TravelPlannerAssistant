from dataclasses import dataclass, field
from typing import List, Dict, Self


@dataclass
class Activity:
    """
    Represents a single activity within an itinerary.
    """
    description: str
    date: str
    time: str = ""
    notes: str = ""
    is_completed: bool = False

    def to_dict(self) -> dict:
        """Convert Activity to a dictionary for JSON serialization."""
        return {
            "description": self.description,
            "date": self.date,
            "time": self.time,
            "notes": self.notes,
            "is_completed": self.is_completed
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create an Activity object from a dictionary."""
        return cls(
            description=data["description"],
            date=data["date"],
            time=data.get("time", ""),
            notes=data.get("notes", ""),
            is_completed=data.get("is_completed", False)
        )


@dataclass
class Itinerary:
    """
    Represents a full travel itinerary with trip details and activities.
    """
    list_name: str
    trip_title: str
    location: str
    start_date: str
    end_date: str
    trip_type: str
    activities: List[Activity] = field(default_factory=list)

    @property
    def total_activities(self) -> int:
        """Total number of activities in the itinerary."""
        return len(self.activities)

    @property
    def completed_activities(self) -> int:
        """Number of activities marked as completed."""
        return sum(1 for activity in self.activities if activity.is_completed)

    @property
    def completion_progress(self) -> float:
        """Completion progress of the itinerary as a percentage."""
        if self.total_activities == 0:
            return 0.0
        return (self.completed_activities / self.total_activities) * 100

    def add_activity(self, description: str, date: str, time: str = "", notes: str = "") -> None:
        """Add a new activity to the itinerary."""
        self.activities.append(Activity(description, date, time, notes))

    def remove_activity(self, description: str) -> bool:
        """Remove an activity from the itinerary by description."""
        for i, activity in enumerate(self.activities):
            if activity.description == description:
                del self.activities[i]
                return True
        return False

    def toggle_completed(self, description: str) -> bool:
        """Toggle the completion status of an activity by description."""
        for activity in self.activities:
            if activity.description == description:
                activity.is_completed = not activity.is_completed
                return True
        return False

    def get_activities_by_day(self) -> Dict[str, List[Activity]]:
        """Separate activities by date (day)."""
        days = {}
        for activity in self.activities:
            if activity.date not in days:
                days[activity.date] = []
            days[activity.date].append(activity)

        # Sort the activities by date
        sorted_days = {date: sorted(activities, key=lambda a: a.time) for date, activities in days.items()}

        return sorted_days

    def to_dict(self) -> dict:
        """Convert Itinerary to a dictionary for JSON serialization."""
        return {
            "trip_title": self.trip_title,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "trip_type": self.trip_type,
            "activities": [activity.to_dict() for activity in self.activities]
        }

    @classmethod
    def from_dict(cls, list_name: str, data: dict) -> Self:
        """Create an Itinerary object from a dictionary."""
        activities = [Activity.from_dict(item_data) for item_data in data.get("activities", [])]
        return cls(
            list_name=list_name,
            trip_title=data["trip_title"],
            location=data["location"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            trip_type=data["trip_type"],
            activities=activities
        )