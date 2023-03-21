from fetch.fetch981Management import Fetch981Management


class FetchGp(Fetch981Management):
    def __init__(self, web_key, driver, browser):
        super().__init__(web_key, driver, browser)
        self.room_type_map = [
            ("^1 Bed - 1 Bath$", "1B1B"),
            ("^1 Bed - 1 Bath - Dining$", "1B1BD"),
            ("^2 Bed - 2 Bath$", "2B2B"),
            ("^2 Bed - 2 Bath - Dining$", "2B2BD"),
        ]
