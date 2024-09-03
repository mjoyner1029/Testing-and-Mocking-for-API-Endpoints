# tests/test_production_endpoints.py
import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Production

class TestProductionEndpoints(unittest.TestCase):
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

    @patch('app.production.routes.db.session')
    def test_create_production(self, mock_db_session):
        response = self.client.post('/production/', json={
            'product_id': 1,
            'quantity_produced': 100,
            'date_produced': '2024-09-03'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    @patch('app.production.routes.Production.query.all')
    def test_list_production(self, mock_query):
        mock_query.return_value = [Production(id=1, product_id=1, quantity_produced=100, date_produced='2024-09-03')]
        response = self.client.get('/production/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['quantity_produced'], 100)

    @patch('app.production.routes.db.session')
    def test_create_production_invalid(self, mock_db_session):
        response = self.client.post('/production/', json={
            'product_id': 1,
            'quantity_produced': -10,
            'date_produced': '2024-09-03'
        })
        self.assertEqual(response.status_code, 400)
