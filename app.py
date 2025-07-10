from flask import Flask, render_template, request, session
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
app.secret_key = os.urandom(24)

db = client["Banking"]
collection = db["User_details"]

@app.route('/')
def show_form():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def handle_form():
    email = request.form['email']
    password = request.form['password']
    user = collection.find_one({"Email": email, "Password": password})
    if user:
        return render_template('welcome.html', name=user['Username'])
    else:
        return render_template('index.html', error="Invalid email or password")

@app.route('/forget', methods=['GET','POST'])
def forget_password():
    return render_template('forget.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    return render_template('create.html')

@app.route('/check', methods=['POST'])
def check_user():
    email = request.form['email']
    phone = request.form['phone']
    user = collection.find_one({"Email": email, "Phone": phone})
    if user:
        session['username'] = user['Username']
        return render_template('reset.html')
    else:
        return render_template('forget.html', error="Please check your email and phone number.")

@app.route('/reset', methods=['POST'])
def reset_password():
    password1 = request.form['password1']
    password2 = request.form['password2']
    if password1 == password2:
        name = session.get('username')
        if name:
            collection.update_one({"Username": name}, {"$set": {"Password": password1}})
            session.pop('username', None)
            return render_template('index.html', message="Password updated successfully")
        else:
            return render_template('forget.html', error="Session expired. Please try again.")
    else:
        return render_template('reset.html', error="Passwords do not match")

@app.route('/create', methods=['GET','POST'])
def create_user():
    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    
    if collection.find_one({"Email": email}):
        return render_template('create.html', error="Email already exists")
    elif collection.find_one({"Phone": phone}):
        return render_template('create.html', error="Phone number already exists")
    elif collection.find_one({"Username": username}):
        return render_template('create.html', error="Username already exists")
    collection.insert_one({
        "Username": username,
        "Email": email,
        "Phone": phone,
        "Password": password
    })
    
    return render_template('index.html', message="User created successfully. Please login.")

if __name__ == '__main__':
    app.run(debug=True)