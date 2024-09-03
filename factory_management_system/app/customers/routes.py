# app/customers/routes.py
from flask import Blueprint, request, jsonify
from app.models import Customer, db
from flask_limiter.util import get_remote_address

customers = Blueprint('customers', __name__)

@customers.route('/', methods=['POST'])
def create_customer():
    data = request.get_json()
    customer = Customer(name=data['name'], email=data['email'], phone=data['phone'])
    db.session.add(customer)
    db.session.commit()
    return jsonify({'id': customer.id}), 201

@customers.route('/', methods=['GET'])
def list_customers():
    customers = Customer.query.all()
    return jsonify([{
        'id': cust.id,
        'name': cust.name,
        'email': cust.email,
        'phone': cust.phone
    } for cust in customers]), 200
