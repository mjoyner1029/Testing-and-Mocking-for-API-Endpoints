# tests/test_customer_endpoints.py
import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Customer

class TestCustomerEndpoints(unittest.TestCase):
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

    @patch('app.customers.routes.db.session')
    def test_create_customer(self, mock_db_session):
        response = self.client.post('/customers/', json={
            'name': 'Jane Doe',
            'email': 'jane.doe@example.com',
            'phone': '123-456-7890'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    @patch('app.customers.routes.Customer.query.all')
    def test_list_customers(self, mock_query):
        mock_query.return_value = [Customer(id=1, name='Jane Doe', email='jane.doe@example.com', phone='123-456-7890')]
        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['email'], 'jane.doe@example.com')

    @patch('app.customers.routes.db.session')
    def test_create_customer_invalid(self, mock_db_session):
        response = self.client.post('/customers/', json={
            'name': '',
            'email': 'jane.doe@example.com',
            'phone': '123-456-7890'
        })
        self.assertEqual(response.status_code, 400)
