from fetch.fetch981Management import Fetch981Management


class Fetch18Park(Fetch981Management):
    def __init__(self, driver, browser):
        super().__init__(driver,  browser)
        self.room_type_map = [
            ("^1 bed 1 bath$", "1B1B"),
            ("^Townhouse$", "2B1.5B"),
            ("^2 bed 2 bath$", "2B2B"),
        ]
