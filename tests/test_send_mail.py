import unittest

from utils.send_mail import send_notification_email

from tests.test_constants import ROOM1, ROOM2, ROOM2_UPDATED


class TestSendMail(unittest.TestCase):
    def test_generate_update_table(self):
        new_rooms = [ROOM1]
        removed_rooms = []
        updated_rooms = [(ROOM2, ROOM2_UPDATED)]
        send_notification_email(new_rooms, removed_rooms, updated_rooms)


if __name__ == "__main__":
    unittest.main()
