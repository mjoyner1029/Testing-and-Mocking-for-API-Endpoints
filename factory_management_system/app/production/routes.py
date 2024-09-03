# app/production/routes.py
from flask import Blueprint, request, jsonify
from app.models import Production, db
from flask_limiter.util import get_remote_address

production = Blueprint('production', __name__)

@production.route('/', methods=['POST'])
def create_production():
    data = request.get_json()
    production = Production(
        product_id=data['product_id'],
        quantity_produced=data['quantity_produced'],
        date_produced=data['date_produced']
    )
    db.session.add(production)
    db.session.commit()
    return jsonify({'id': production.id}), 201

@production.route('/', methods=['GET'])
def list_production():
    production = Production.query.all()
    return jsonify([{
        'id': prod.id,
        'product_id': prod.product_id,
        'quantity_produced': prod.quantity_produced,
        'date_produced': prod.date_produced.isoformat()
    } for prod in production]), 200
