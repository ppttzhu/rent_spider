import unittest
from unittest.mock import MagicMock, patch

import constants as c
from database import Database

from tests.test_constants import ROOM1, ROOM2, ROOM2_UPDATED


class TestDatabase(unittest.TestCase):
    @patch("database.Database.__init__")
    def setUp(self, mock_init):
        mock_init.return_value = None
        self.database = Database()
        self.database.cursor = MagicMock()
        self.database.cursor.execute = MagicMock()
        self.database.conn = MagicMock()

    def test_compare_rooms_diff(self):
        # Test remove
        prev_rooms = [ROOM1, ROOM2]
        cur_rooms = [ROOM2]
        new_rooms, removed_rooms, updated_rooms = self.database.compare_rooms_diff(
            prev_rooms, cur_rooms
        )
        self.assertEqual(new_rooms, [])
        self.assertEqual(removed_rooms, [ROOM1])
        self.assertEqual(updated_rooms, [])
        # Test add
        prev_rooms = [ROOM2]
        cur_rooms = [ROOM1, ROOM2]
        new_rooms, removed_rooms, updated_rooms = self.database.compare_rooms_diff(
            prev_rooms, cur_rooms
        )
        self.assertEqual(new_rooms, [ROOM1])
        self.assertEqual(removed_rooms, [])
        self.assertEqual(updated_rooms, [])
        # Test update
        prev_rooms = [ROOM2]
        cur_rooms = [ROOM2_UPDATED]
        new_rooms, removed_rooms, updated_rooms = self.database.compare_rooms_diff(
            prev_rooms, cur_rooms
        )
        self.assertEqual(new_rooms, [])
        self.assertEqual(removed_rooms, [])
        self.assertEqual(updated_rooms, [(ROOM2, ROOM2_UPDATED)])

    def test_update_room(self):
        self.database.update_room(ROOM2, ROOM2_UPDATED)
        expected_updated_sql = "UPDATE room SET room_type = '1B1B',move_in_date = '9/7/2022',room_price = '4000' WHERE website_name = 'Jsq' AND room_number = '2301'"
        self.database.cursor.execute.assert_called_once_with(expected_updated_sql)

    def test_update_website(self):
        self.database.cursor.fetchall = MagicMock()
        self.database.cursor.fetchall.return_value = [
            [c.WEBSITES[0][c.WEBSITE_NAME_COLUMN]],
            ["Dummy Name"],
        ]
        self.database.update_website()
        expected_delete_sql = "DELETE FROM website WHERE website_name IN ('Dummy Name')"
        self.database.cursor.execute.assert_any_call(expected_delete_sql)
        expected_updated_sql = f"""INSERT INTO website (website_name, url, priority) VALUES('{c.WEBSITES[0][c.WEBSITE_NAME_COLUMN]}', '{c.WEBSITES[0][c.WEBSITE_URL_COLUMN]}', 0) ON DUPLICATE KEY UPDATE url='{c.WEBSITES[0][c.WEBSITE_URL_COLUMN]}', priority=0"""
        self.database.cursor.execute.assert_any_call(expected_updated_sql)


if __name__ == "__main__":
    unittest.main()
