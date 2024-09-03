# app/orders/routes.py
from flask import Blueprint, request, jsonify
from app.models import Order, db
from flask_limiter.util import get_remote_address

orders = Blueprint('orders', __name__)

@orders.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    order = Order(
        customer_id=data['customer_id'],
        product_id=data['product_id'],
        quantity=data['quantity'],
        total_price=data['total_price']
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({'id': order.id}), 201

@orders.route('/', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': ord.id,
        'customer_id': ord.customer_id,
        'product_id': ord.product_id,
        'quantity': ord.quantity,
        'total_price': ord.total_price
    } for ord in orders]), 200
