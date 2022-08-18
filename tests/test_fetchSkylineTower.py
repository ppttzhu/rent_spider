import unittest
from unittest.mock import MagicMock, patch

from fetch.fetchSkylineTower import FetchSkylineTower

from tests.test_utils import get_html_doc

mock_get_html_doc = MagicMock()


@patch("fetch.fetchSkylineTower.FetchSkylineTower.get_html_doc", mock_get_html_doc)
@patch("fetch.fetchStreetEasy.sleep", MagicMock())
class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.fetch = FetchSkylineTower(MagicMock(), MagicMock())

    def test_fetch_room_info(self):
        mock_get_html_doc.side_effect = [get_html_doc("SkylineTower")] + [
            get_html_doc("SkylineTower_room")
        ] * 10
        self.fetch.fetch_web()
        self.assertEqual(9, len(self.fetch.room_info))


if __name__ == "__main__":
    unittest.main()
