import os
import unittest
from unittest.mock import patch

from fetch.fetchSkylineTower import FetchSkylineTower


class TestDatabase(unittest.TestCase):
    @patch("fetch.fetchSkylineTower.FetchSkylineTower.get_html_doc")
    @patch("fetch.fetchSkylineTower.FetchSkylineTower.get_html_doc_room")
    def setUp(self, mock_room, mock_html):
        def get_html_doc():
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "fixtures/SkylineTower.html")
            with open(filename, mode="r", encoding="UTF-8") as file:
                return "\n".join(file.readlines())

        def get_html_doc_room():
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "fixtures/SkylineTower_room.html")
            with open(filename, mode="r", encoding="UTF-8") as file:
                return "\n".join(file.readlines())

        mock_html.return_value = get_html_doc()
        mock_room.return_value = get_html_doc_room()
        self.fetch = FetchSkylineTower("dummy-driver")

    def test_fetch_room_info(self):
        self.fetch.fetch_web()
        self.assertEqual(10, len(self.fetch.room_info))


if __name__ == "__main__":
    unittest.main()
