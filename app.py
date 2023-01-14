from flask import Flask, render_template, request, jsonify,  make_response,redirect, url_for
import sqlite3
from flask_mail import Mail,Message
from random import randint 
from flask_jwt_extended import JWTManager, jwt_required, create_access_token


app = Flask(__name__, template_folder='templates')
app.config['JWT_SECRET_KEY']  = 'dhbsckjsdnckjdsvlsmsdlkxjqsojx'
jwt = JWTManager(app)


#connect to database
con = sqlite3.connect('signupemail.db')
cur = con.cursor()

#Create tables
cur.execute('''CREATE TABLE IF NOT EXISTS User (id INTEGER, name TEXT, email TEXT, password TEXT)''')
cur.execute('''CREATE TABLE IF NOT EXISTS Internship (id INTEGER PRIMARY KEY AUTOINCREMENT, Internship_Position TEXT, Company TEXT, Application_details TEXT, Type TEXT, Starting_Date TEXT)''')
con.commit()

app.config["MAIL_SERVER"]='smtp.gmail.com'
app.config["MAIL_PORT"]=465
app.config["MAIL_USERNAME"]='ayaoueslati016@gmail.com'
app.config['MAIL_PASSWORD']='pfmgwmskdiaxvaij'              #give your password of gmail account
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
mail=Mail(app)


@app.route('/')
def sign():
  return render_template('signup.html')
  


@app.route('/login')
def log():
    return render_template('login.html')



@app.route('/verify')
def verify1():
        return render_template('verify.html')


@app.route('/jwtgeneration')
def generating():
  return render_template('Jwtgeneration.html')
  


from user import models
@app.route('/validate',methods=['POST'])
def validate():
    user_otp=request.form['otp']
    print (user_otp)
    if otp==int(user_otp):
        return "<h3>Email verification succesfull</h3>"
    else:
        return "<h3>Please Try Again</h3>"


@app.route('/Api_Dashboard', methods=['GET', 'POST'])
def API_dashboard():
        return render_template('APIdash.html')

#get all internships function
def fetch_db_all():
    con = sqlite3.connect('signupemail.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Internship''')
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({ "id" : row[0], "Internship_Position": row[1], "Company":row[2], "Application_details": row[3], "Type": row[4] , "Starting_Date" : row[5]})
        print (row[1])
    return data

#get all internships
@app.route('/Api_Dashboard/Internships', methods=['GET', 'POST'])
def internship():
    return make_response(jsonify(fetch_db_all()), 200)   



def fetch_db(position):  
    con = sqlite3.connect('signupemail.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Internship WHERE Internship_Position == ?''', (position, ))
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({ "id" : row[0], "Internship_Position": row[1], "Company":row[2], "Application_details": row[3], "Type": row[4] , "Starting_Date" : row[5]})
        print (row[1])
    return data


#get internship by position
@app.route('/Api_Dashboard/Internship', methods=['GET', 'POST'])
def get_internship_byname():
        data =request.form
        internship_obj = fetch_db(data["internship_position"])
        if internship_obj:
            return make_response(jsonify(internship_obj), 200)
        else:
            return make_response(jsonify(internship_obj), 404)



@app.route('/Api_Dashboard/internship/<InternshipPosition>', methods=['GET'])
def get_scholarship_name(InternshipPosition):
        internship_obj = fetch_db(InternshipPosition)
        if internship_obj:
            return make_response(jsonify(internship_obj), 200)
        else:
            return make_response(jsonify(internship_obj), 404)




def fetching_db(company):  
    con = sqlite3.connect('signupemail.db')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Internship WHERE Company == ?''', (company, ))
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({ "id" : row[0], "Internship_Position": row[1], "Company":row[2], "Application_details": row[3], "Type": row[4] , "Starting_Date" : row[5]})
        print (row[1])
    return data



@app.route('/internship/company/<company>', methods=['GET'])
def get_internship_bycompany(company):
        internship_obj = fetching_db(company)
        if internship_obj:
            return make_response(jsonify(internship_obj), 200)
        else:
            return make_response(jsonify(internship_obj), 404)



# adding an internship
@app.route('/internship/add', methods=['POST'])
def add_internship():
      # Parse the request body
      data = request.form

      # Connect to the database
      con = sqlite3.connect('signupemail.db')
      cur = con.cursor()

      # Insert the data into the database

      cur.execute("INSERT INTO Internship (Internship_Position, Company , Application_details, Type , Starting_Date ) VALUES (?, ?, ?, ?, ?)", (data['internship_position'], data['Company'], data['App_details'], data['type'], data['Starting_date']))
      con.commit()

      # Return a response to the client
      return jsonify({'status': 'success'})



@app.route('/internship/delete/<startingdate>', methods=['DELETE'])
@jwt_required()
def delete_scholarship(startingdate):
    try:
        con = sqlite3.connect('signupemail.db')
        cur = con.cursor()
        cur.execute("DELETE FROM Internship WHERE Starting_Date = ?", (startingdate,))
        con.commit()
        return jsonify({'status': 'success'})
    except sqlite3.Error as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        if con:
            con.close()



@app.route('/Internship/update', methods=['PUT', 'POST'])
def update_scholarship():
        data = request.form
        con = sqlite3.connect('signupemail.db')
        cur = con.cursor()
        cur.execute("UPDATE Internship SET Internship_Position = ?, Company = ?, Application_details = ?, Type = ?, Starting_Date = ? WHERE Internship_Position = ? AND Company = ? ", (data['internship_position'], data['Company'], data['App_details'], data['type'], data['Starting_date'], data['internship_position'], data['Company']))
        con.commit()
        return jsonify({'status': 'success'})



#import user routes
from user import routes
from user.models import otp
from user.models import User

if __name__ == '__main__':
   app.run(debug=True)




