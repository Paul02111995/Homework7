import unittest
from card import Card
from card_repository import app, card_repo
from flask_testing import TestCase


class CardTestCase(unittest.TestCase):
    def setUp(self):
        self.pan = "1234567890123456"
        self.expiry_date = "12/25"
        self.cvv = "123"
        self.issue_date = "01/20"
        self.owner_id = "123456789"
        self.status = "active"
        self.card = Card(self.pan, self.expiry_date, self.cvv, self.issue_date, self.owner_id, self.status)

    def test_card_attributes(self):
        self.assertEqual(self.card.pan, self.pan)
        self.assertEqual(self.card.expiry_date, self.expiry_date)
        self.assertEqual(self.card.cvv, self.cvv)
        self.assertEqual(self.card.issue_date, self.issue_date)
        self.assertEqual(self.card.owner_id, self.owner_id)
        self.assertEqual(self.card.status, self.status)


class CardAppTestCase(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        card_repo.create_table()

    def tearDown(self):
        card_repo.close()

    def test_create_card(self):
        response = self.client.get('/cards?pan=1234567890123456&expiry_date=12/25&cvv=123&issue_date=01/20&owner_id=123456789&status=active')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Card created with ID:", response.data)

    def test_get_card(self):
        response = self.client.get('/cards/12345678-1234-5678-1234-567812345678')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Card with ID 12345678-1234-5678-1234-567812345678 not found")

    def test_get_card_not_found(self):
        card_id = "12345678-1234-5678-1234-567812345678"
        response = self.client.get(f'/cards/{card_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"Card with ID 12345678-1234-5678-1234-567812345678 not found")


if __name__ == '__main__':
    unittest.main()
