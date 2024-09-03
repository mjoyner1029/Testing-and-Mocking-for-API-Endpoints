# tests/test_employee_endpoints.py
import unittest
from unittest.mock import patch
from app import create_app, db
from app.models import Employee

class TestEmployeeEndpoints(unittest.TestCase):
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

    @patch('app.employees.routes.db.session')
    def test_create_employee(self, mock_db_session):
        response = self.client.post('/employees/', json={'name': 'John Doe', 'position': 'Engineer'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)

    @patch('app.employees.routes.Employee.query.all')
    def test_list_employees(self, mock_query):
        mock_query.return_value = [Employee(id=1, name='John Doe', position='Engineer')]
        response = self.client.get('/employees/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'John Doe')

    @patch('app.employees.routes.db.session')
    def test_create_employee_invalid(self, mock_db_session):
        response = self.client.post('/employees/', json={'name': '', 'position': 'Engineer'})
        self.assertEqual(response.status_code, 400)
