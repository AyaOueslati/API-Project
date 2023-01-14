from flask import Flask, jsonify, request
from user.models import User
from app import app
from flask_mail import Mail,Message



@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/login', methods=['POST'])
def login():
    return User().login()