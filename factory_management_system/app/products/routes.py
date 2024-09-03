# app/products/routes.py
from flask import Blueprint, request, jsonify
from app.models import Product, db
from flask_limiter.util import get_remote_address

products = Blueprint('products', __name__)

@products.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    product = Product(name=data['name'], price=data['price'])
    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id}), 201

@products.route('/', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{'id': prod.id, 'name': prod.name, 'price': prod.price} for prod in products]), 200
