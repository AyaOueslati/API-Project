from flask import Flask, jsonify, request, current_app,Response
import uuid
from passlib.hash import pbkdf2_sha256
import sqlite3
from flask_mail import Mail,Message
from random import randint
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import json
from app import app
import datetime

app.config['JWT_SECRET_KEY']  = 'dhbsckjsdnckjdsvlsmsdlkxjqsojx'
jwt = JWTManager(app)
app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='ayaoueslati016@gmail.com'
app.config['MAIL_PASSWORD']='pfmgwmskdiaxvaij'                    #you have to give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)
otp=randint(000000,999999)

class User:
    def signup(self):
        email=request.form['email']
        msg=Message(subject='Confirmation Code',sender='ayaoueslati016@gmail.com',recipients=[email])
        msg.body=str(otp)
        mail.send(msg)
        print(request.form)

        user = {
         "_id": uuid.uuid4().hex,
         "name": request.form.get('name'),
         "email": request.form.get('email'),
         "password": request.form.get('password')

            }
        #user['password'] = pbkdf2_sha256.encrypt(user["password"])

        con = sqlite3.connect('signupemail.db')
        cur = con.cursor()

        #check if user already exists
        result = cur.execute("SELECT * FROM User WHERE email = ?", [user['email']]).fetchone()
        if result:
                return jsonify({'error': 'User email  already Exist'}), 400
        else:
                cur.execute('''INSERT INTO User (id, name, email, password) VALUES (?,?,?,?)''', (user['_id'], user['name'], user['email'], user['password']))
                con.commit()
                return jsonify(user), 200

    def login(self):
           
        user = {

         "email": request.form.get('email'),
         "password": request.form.get('password')

            }
        
        con = sqlite3.connect('signupemail.db')
        cur = con.cursor()   
        result1 = cur.execute("SELECT * FROM User WHERE email= ?", [user['email']]).fetchone()
        result2 = cur.execute("SELECT * FROM User WHERE password= ?", [user['password']]).fetchone()
        if (result1) and (result2):
            print("You logged in successfully")
            access_token = create_access_token(identity = user['email'])
            print (access_token)
            return jsonify({'success': 'You logged in successfully'}), 200
        else:
            return jsonify({'error': 'You logged in with wrong credentials'}), 400


