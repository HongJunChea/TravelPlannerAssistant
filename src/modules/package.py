from dataclasses import dataclass, field
from typing import List, Dict, Self


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
class PackingList:
    """packing list"""
    list_name: str
    destination_type: str
    duration: int
    weather: str
    travelers: int
    items: List[PackingItem] = field(default_factory=list)

    @property
    def total_items(self) -> int:
        """total number of items in packing list"""
        return sum(item.quantity for item in self.items)

    @property
    def packed_items(self) -> int:
        """item be packed"""
        return sum(item.quantity for item in self.items if item.is_packed)

    @property
    def packing_progress(self) -> float:
        """packing progress"""
        if self.total_items == 0:
            return 0.0
        return (self.packed_items / self.total_items) * 100

    def add_item(self, name: str, category: str, quantity: int = 1) -> None:
        """add item"""
        # check is that same item
        for item in self.items:
            if item.name == name and item.category == category:
                item.quantity += quantity
                return

        # add new item
        self.items.append(PackingItem(name, category, False, quantity))

    def remove_item(self, name: str) -> bool:
        """remove item"""
        for i, item in enumerate(self.items):
            if item.name == name:
                del self.items[i]
                return True
        return False

    def toggle_packed(self, name: str) -> bool:
        """change packing status to packed"""
        for item in self.items:
            if item.name == name:
                item.is_packed = not item.is_packed
                return True
        return False

    def get_items_by_category(self) -> Dict[str, List[PackingItem]]:
        """separate items by category"""
        categories = {}
        for item in self.items:
            if item.category not in categories:
                categories[item.category] = []
            categories[item.category].append(item)
        return categories

    def to_dict(self) -> dict:
        """Convert PackingList to dict for JSON serialization."""
        return {
            "destination_type": self.destination_type,
            "duration": self.duration,
            "weather": self.weather,
            "travelers": self.travelers,
            "items": [item.to_dict() for item in self.items]
        }

    @classmethod
    def from_dict(cls, list_name: str, data: dict) -> Self:
        """Create PackingList from dict."""
        items = [PackingItem.from_dict(item_data) for item_data in data.get("items", [])]
        return cls(
            list_name=list_name,
            destination_type=data["destination_type"],
            duration=int(data["duration"]),
            weather=data["weather"],
            travelers=int(data["travelers"]),
            items=items
        )