import unittest
from unittest.mock import MagicMock, patch

from fetch.fetchQLIC import FetchQLIC

from tests.test_utils import get_html_doc

mock_get_html_doc = MagicMock()


@patch("fetch.fetchQLIC.FetchQLIC.get_html_doc", mock_get_html_doc)
@patch("fetch.fetchStreetEasy.sleep", MagicMock())
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.fetch = FetchQLIC(MagicMock(), MagicMock())

    def test_fetch_room_info(self):
        mock_get_html_doc.side_effect = [get_html_doc("QLIC")] + [get_html_doc("QLIC_room")] * 10
        self.fetch.fetch_web()
        self.assertEqual(2, len(self.fetch.room_info))


if __name__ == "__main__":
    unittest.main()
