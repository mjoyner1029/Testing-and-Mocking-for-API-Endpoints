# tests/test_product_endpoints.py
import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Product

class TestProductEndpoints(unittest.TestCase):
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

    @patch('app.products.routes.db.session')
    def test_create_product(self, mock_db_session):
        response = self.client.post('/products/', json={'name': 'Widget', 'price': 19.99})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    @patch('app.products.routes.Product.query.all')
    def test_list_products(self, mock_query):
        mock_query.return_value = [Product(id=1, name='Widget', price=19.99)]
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Widget')

    @patch('app.products.routes.db.session')
    def test_create_product_invalid(self, mock_db_session):
        response = self.client.post('/products/', json={'name': 'Widget', 'price': -10})
        self.assertEqual(response.status_code, 400)
