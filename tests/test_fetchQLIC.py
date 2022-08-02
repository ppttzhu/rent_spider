import os
import unittest
from unittest.mock import patch

from fetch.fetchQLIC import FetchQLIC


class TestDatabase(unittest.TestCase):
    @patch("fetch.fetchQLIC.FetchQLIC.get_html_doc")
    @patch("fetch.fetchQLIC.FetchQLIC.get_html_doc_room")
    def setUp(self, mock_room, mock_html):
        def get_html_doc():
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "fixtures/QLIC.html")
            with open(filename, mode="r", encoding="UTF-8") as file:
                return "\n".join(file.readlines())

        def get_html_doc_room():
            dirname = os.path.dirname(__file__)
            filename = os.path.join(dirname, "fixtures/QLIC_room.html")
            with open(filename, mode="r", encoding="UTF-8") as file:
                return "\n".join(file.readlines())

        mock_html.return_value = get_html_doc()
        mock_room.return_value = get_html_doc_room()
        self.fetch = FetchQLIC("dummy-driver")

    def test_fetch_room_info(self):
        self.fetch.fetch_web()
        self.assertEqual(2, len(self.fetch.room_info))
