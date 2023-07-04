from fetch.fetch981Management import Fetch981Management


class Fetch225GrandStreet(Fetch981Management):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.room_type_map = [
            ("^1 br - 1ba$", "1B1B"),
            ("^2 br - 2ba$", "2B2B"),
        ]
