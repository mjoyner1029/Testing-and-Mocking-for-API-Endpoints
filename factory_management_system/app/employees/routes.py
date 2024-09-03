# app/employees/routes.py
from flask import Blueprint, request, jsonify
from app.models import Employee, db
from flask_limiter.util import get_remote_address

employees = Blueprint('employees', __name__)

@employees.route('/', methods=['POST'])
def create_employee():
    data = request.get_json()
    employee = Employee(name=data['name'], position=data['position'])
    db.session.add(employee)
    db.session.commit()
    return jsonify({'id': employee.id}), 201

@employees.route('/', methods=['GET'])
def list_employees():
    employees = Employee.query.all()
    return jsonify([{'id': emp.id, 'name': emp.name, 'position': emp.position} for emp in employees]), 200
