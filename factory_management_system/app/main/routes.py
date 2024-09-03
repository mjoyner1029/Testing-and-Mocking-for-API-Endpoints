# app/main/routes.py
from flask import jsonify
from app.main import main

@main.route('/')
def index():
    return jsonify({"message": "Welcome to the Factory Management System API!"}), 200
