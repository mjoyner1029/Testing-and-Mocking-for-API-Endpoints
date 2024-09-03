# tests/test_order_endpoints.py
import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Order

class TestOrderEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.drop_all()
        cls.app_context.pop()

    @patch('app.orders.routes.db.session')
    def test_create_order(self, mock_db_session):
        response = self.client.post('/orders/', json={
            'customer_id': 1,
            'product_id': 1,
            'quantity': 5,
            'total_price': 99.95
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    @patch('app.orders.routes.Order.query.all')
    def test_list_orders(self, mock_query):
        mock_query.return_value = [Order(id=1, customer_id=1, product_id=1, quantity=5, total_price=99.95)]
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['total_price'], 99.95)

    @patch('app.orders.routes.db.session')
    def test_create_order_invalid(self, mock_db_session):
        response = self.client.post('/orders/', json={
            'customer_id': 1,
            'product_id': 1,
            'quantity': -5,
            'total_price': 99.95
        })
        self.assertEqual(response.status_code, 400)
