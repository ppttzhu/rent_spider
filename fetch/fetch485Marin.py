from fetch.fetch981Management import Fetch981Management


class Fetch485Marin(Fetch981Management):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_type_map = [
            ("^0 Bed-1 Bath$", "Studio"),
            ("^1 Bed-1Bath$", "1B1B"),
            ("2 Bedroom-2 Bath$", "2B2B"),
            ("3 Bedroom-2 Bath$", "3B3B"),
        ]
