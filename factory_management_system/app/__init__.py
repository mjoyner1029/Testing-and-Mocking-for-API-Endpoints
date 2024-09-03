# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from config import Config

db = SQLAlchemy()
limiter = Limiter()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    limiter.init_app(app)

    from app.main.routes import main
    from app.employees.routes import employees
    from app.products.routes import products
    from app.orders.routes import orders
    from app.customers.routes import customers
    from app.production.routes import production

    app.register_blueprint(main)
    app.register_blueprint(employees, url_prefix='/employees')
    app.register_blueprint(products, url_prefix='/products')
    app.register_blueprint(orders, url_prefix='/orders')
    app.register_blueprint(customers, url_prefix='/customers')
    app.register_blueprint(production, url_prefix='/production')

    return app
