from fetch.fetch981Management import Fetch981Management


class Fetch235GrandStreet(Fetch981Management):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_type_map = [
            ("^1 Bedroom - 1 Bathroom$", "1B1B"),
            ("^2 Bedroom - 2 Bathroom$", "2B2B"),
        ]
