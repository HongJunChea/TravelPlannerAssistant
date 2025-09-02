class Trip:
    def __init__(self, trip_name: str):
        self.trip_name = trip_name

    def get_trip_name(self) -> str:
        return self.trip_name

    def summary(self) -> str:
        return f"Component of trip: {self.trip_name}"
