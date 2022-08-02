from fetch.fetch981Management import Fetch981Management


class Fetch235GrandStreet(Fetch981Management):
    def __init__(self, driver, browser):
        super().__init__(driver,  browser)
        self.room_type_map = [
            ("^1 Bedroom - 1 Bathroom$", "1B1B"),
            ("^2 Bedroom - 2 Bathroom$", "2B2B"),
        ]
