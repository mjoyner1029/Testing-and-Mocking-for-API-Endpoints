# app/orders/__init__.py
from flask import Blueprint

orders = Blueprint('orders', __name__)

from app.orders import routes
