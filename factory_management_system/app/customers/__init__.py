# app/customers/__init__.py
from flask import Blueprint

customers = Blueprint('customers', __name__)

from app.customers import routes
