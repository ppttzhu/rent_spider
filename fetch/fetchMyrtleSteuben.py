from fetch.fetchStreetEasy import FetchStreetEasy


class FetchMyrtleSteuben(FetchStreetEasy):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.table_class = "nice_table listings building-pages active-rentals-table"
