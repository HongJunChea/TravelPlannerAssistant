from src.modules.package import PackingList, PackingItem
from src.utils.file import load_packing_lists, save_packing_lists
from typing import Dict

class PackingController:
    """packing list controller"""

    def __init__(self):
        # item database
        self.PACKING_DATABASE = {
            "base_items": {
                "Clothing": ["Underwear", "Socks", "Pajamas", "Change of clothes"],
                "Toiletries": ["Toothbrush", "Toothpaste", "Shampoo", "Body Wash", "Towel", "Skincare Products"],
                "Electronics": ["Phone Charger", "Power Bank", "Camera", "Earphones"],
                "Documents": ["ID Card", "Passport", "Flight Ticket", "Hotel Confirmation", "Insurance Policy"],
                "Medicines": ["Regular Medicine", "Band-aids", "Painkillers"],
                "Others": ["Wallet", "Cash", "Credit Card", "Keys"]
            },

            "destination_items": {
                "beach": {
                    "Clothing": ["Swimsuit", "Beach Shorts", "Sandals", "Sun Hat", "Sunglasses"],
                    "Supplies": ["Sunscreen", "Beach Towel", "Picnic Mat", "Snorkeling Gear", "Waterproof Bag", "Beach Umbrella"]
                },
                "mountain": {
                    "Clothing": ["Hiking Boots", "Windbreaker", "Long Pants", "Warm Clothes", "Hat"],
                    "Supplies": ["Trekking Poles", "Headlamp", "Thermos", "First Aid Kit", "Hiking Backpack", "Map"]
                },
                "city": {
                    "Clothing": ["Formal Wear", "Casual Shoes", "Jacket", "Scarf"],
                    "Supplies": ["Umbrella", "Shopping Bag", "City Map", "Metro Card"]
                },
                "countryside": {
                    "Clothing": ["Comfortable Shoes", "Long-Sleeve Clothes", "Insect-Proof Clothing", "Hat"],
                    "Supplies": ["Insect Repellent", "Flashlight", "Picnic Utensils", "Camera Tripod"]
                }
            },

            "weather_items": {
                "sunny": {
                    "Sun Protection": ["Sunscreen", "Sunglasses", "Sun Hat", "Sun-Protective Clothing"],
                },
                "rainy": {
                    "Rain Gear": ["Raincoat", "Umbrella", "Waterproof Bag", "Waterproof Shoe Covers"],
                },
                "cold": {
                    "Warm Gear": ["Thick Jacket", "Thermal Underwear", "Gloves", "Scarf", "Beanie", "Hand Warmers"],
                },
                "mild": {
                    "Moderate Weather Gear": ["Light Jacket", "Long-Sleeve Clothes", "Lightweight Shoes"]
                }
            }
        }

    def generate_packing_list(self, destination: str, duration: int, weather: str, travelers: int,
                              trip_name: str = None) -> PackingList:
        """generate packing list"""

        if not trip_name:
            trip_name = f"{destination} Trip"

        # create empty list
        packing_list = PackingList(
            trip_name=trip_name,
            destination_type=destination,
            duration=duration,
            weather=weather,
            travelers=travelers
        )

        # add items
        self._add_base_items(packing_list, duration, travelers)
        self._add_destination_items(packing_list, destination)
        self._add_weather_items(packing_list, weather)
        self._adjust_quantities_by_duration(packing_list, duration, travelers)

        return packing_list

    def _add_base_items(self, packing_list: PackingList, duration: int, travelers: int):
        """add base items"""
        base_items = self.PACKING_DATABASE["base_items"]

        for category, items in base_items.items():
            for item_name in items:
                if item_name in ["Underwear", "Socks", "Pajamas", "Change of clothes"]:
                    quantity = min(duration, 7) * travelers
                elif item_name in ["Toothbrush", "Towel", "Phone Charger", "Power Bank", "Camera", "Earphones",
                                   "ID Card", "Passport", "Flight Ticket", "Hotel Confirmation", "Insurance Policy",
                                   "Wallet", "Credit Card", "Keys", "Cash"]:
                    quantity = travelers
                else:
                    quantity = 1

                packing_list.add_item(item_name, category, quantity)

    def _add_destination_items(self, packing_list: PackingList, destination: str):
        """add item based on destination"""
        if destination in self.PACKING_DATABASE["destination_items"]:
            dest_items = self.PACKING_DATABASE["destination_items"][destination]
            for category, items in dest_items.items():
                for item_name in items:
                    packing_list.add_item(item_name, category, 1)

    def _add_weather_items(self, packing_list: PackingList, weather: str):
        """add item based on weather"""
        if weather in self.PACKING_DATABASE["weather_items"]:
            weather_items = self.PACKING_DATABASE["weather_items"][weather]
            for category, items in weather_items.items():
                for item_name in items:
                    packing_list.add_item(item_name, category, 1)

    def _adjust_quantities_by_duration(self, packing_list: PackingList, duration: int, travelers: int):
        """add item based on duration"""
        if duration >= 7:
            packing_list.add_item("Laundry Detergent", "Skincare Products", 1)
            packing_list.add_item("Clothes Hangers", "Others", 3)
        if duration >= 14:
            packing_list.add_item("Cold Medicine", "Medicine", 1)
            packing_list.add_item("Stomach Medicine", "Medicine", 1)

    def save_packing_list(self, packing_list: PackingList) -> bool:
        """save list"""
        try:
            existing_lists = load_packing_lists()
            existing_lists[packing_list.trip_name] = packing_list
            save_packing_lists(existing_lists)
            return True
        except Exception as e:
            print(f"Error while saving the file: {e}")
            return False

    def load_all_lists(self) -> Dict[str, PackingList]:
        """load all lists"""
        return load_packing_lists()

    def delete_list(self, trip_name: str) -> bool:
        """delete list"""
        try:
            existing_lists = load_packing_lists()
            if trip_name in existing_lists:
                del existing_lists[trip_name]
                save_packing_lists(existing_lists)
                return True
            return False
        except Exception as e:
            print(f"Error while deleting the file: {e}")
            return False
