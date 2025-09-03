from dataclasses import dataclass, field
from typing import List, Dict, Self
from src.modules.trip import Trip


@dataclass
class PackingItem:
    """pack item"""
    name: str
    category: str
    is_packed: bool = False
    quantity: int = 1

    def to_dict(self) -> dict:
        """Convert PackingItem to dict for JSON serialization."""
        return {
            "name": self.name,
            "category": self.category,
            "is_packed": self.is_packed,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """Create PackingItem from dict."""
        return cls(
            name=data["name"],
            category=data["category"],
            is_packed=data.get("is_packed", False),
            quantity=data.get("quantity", 1)
        )


@dataclass
class PackingList(Trip):
    """packing list"""
    destination_type: str = ""
    duration: int = 0
    weather: str = ""
    travelers: int = 1
    items: List[PackingItem] = field(default_factory=list)

    def __init__(self, trip_name: str, destination_type: str, duration: int, weather: str, travelers: int, items: List[PackingItem] = None):
        super().__init__(trip_name)
        self.destination_type = destination_type
        self.duration = duration
        self.weather = weather
        self.travelers = travelers
        self.items = items if items else []

    # ---------- Properties ----------
    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

    @property
    def packed_items(self) -> int:
        return sum(item.quantity for item in self.items if item.is_packed)

    @property
    def packing_progress(self) -> float:
        if self.total_items == 0:
            return 0.0
        return (self.packed_items / self.total_items) * 100

    # ---------- Methods ----------
    def add_item(self, name: str, category: str, quantity: int = 1) -> None:
        for item in self.items:
            if item.name == name and item.category == category:
                item.quantity += quantity
                return
        self.items.append(PackingItem(name, category, False, quantity))

    def remove_item(self, name: str) -> bool:
        for i, item in enumerate(self.items):
            if item.name == name:
                del self.items[i]
                return True
        return False

    def toggle_packed(self, name: str) -> bool:
        for item in self.items:
            if item.name == name:
                item.is_packed = not item.is_packed
                return True
        return False

    def get_items_by_category(self) -> Dict[str, List[PackingItem]]:
        categories = {}
        for item in self.items:
            categories.setdefault(item.category, []).append(item)
        return categories

    # ---------- Serialization ----------
    def to_dict(self) -> dict:
        return {
            "trip_name": self.trip_name,   # ✅ from Trip
            "destination_type": self.destination_type,
            "duration": self.duration,
            "weather": self.weather,
            "travelers": self.travelers,
            "items": [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        items = [PackingItem.from_dict(item_data) for item_data in data.get("items", [])]
        return cls(
            trip_name=data["trip_name"],   # ✅ load trip_name
            destination_type=data["destination_type"],
            duration=int(data["duration"]),
            weather=data["weather"],
            travelers=int(data["travelers"]),
            items=items
        )
