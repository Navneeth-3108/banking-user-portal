from flask import Flask, render_template, request, session
from pymongo import MongoClient
import os

app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/")
app.secret_key = os.urandom(24)

db = client["Banking"]
usercollection = db["User_details"]
bankcollection = db["Account_details"]

@app.route('/')
def show_form():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def handle_form():
    email = request.form['email']
    password = request.form['password']
    user = usercollection.find_one({"Email": email, "Password": password})
    if user:
        session['phone'] = user["Phone"]
        session['name'] = user['Username']
        session['email'] = user['Email']
    if user and user["Link"]== False:
        return render_template('welcome.html', name=user['Username'])
    elif user and user["Link"] == True:
        return render_template('dashboard.html', name=user['Username'], show = True)
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
    user = usercollection.find_one({"Email": email, "Phone": phone})
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
            usercollection.update_one({"Username": name}, {"$set": {"Password": password1}})
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
    
    if usercollection.find_one({"Email": email}):
        return render_template('create.html', error="Email already exists")
    elif usercollection.find_one({"Phone": phone}):
        return render_template('create.html', error="Phone number already exists")
    elif usercollection.find_one({"Username": username}):
        return render_template('create.html', error="Username already exists")
    usercollection.insert_one({
        "Username": username,
        "Email": email,
        "Phone": int(phone),
        "Password": password,
        "Link": False
    })
    
    return render_template('index.html', message="User created successfully. Please login.")

@app.route('/login-page', methods=['POST'])
def home():
    return render_template('index.html')

@app.route('/link', methods=['POST'])
def link_account():
    phone = session.get('phone')
    user = usercollection.find_one({"Phone": phone})
    bank = bankcollection.find_one({"Phone": phone})
    if user and bank:
        usercollection.update_one({"Phone": phone}, {"$set": {"Link": True}})
        return render_template('dashboard.html', name=user["Username"],message="Account linked successfully", show = True)
    else:
        return render_template('welcome.html', error="No account linked with this phone number")

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return render_template('index.html', message="Logged out successfully")

@app.route('/balance', methods=['POST'])
def show_balance():
    phone = session.get('phone')
    if not phone:
        return render_template('index.html', error="Please login first")

    user = usercollection.find_one({"Phone": phone})
    bank = bankcollection.find_one({"Phone": phone})
    
    if user and bank:
        balance = f"Your current balance is: {bank['Balance']}"
        return render_template('dashboard.html', name=user['Username'], balance=balance, show=False)
    elif user:
        return render_template('dashboard.html', name=user['Username'], error="Bank Server Down", show=True)
    else:
        return render_template('index.html', error="User session expired. Please login again.")

@app.route('/hide', methods=['POST'])
def hide_balance():
    name = session.get('name')
    if not name:
        return render_template('index.html', error="Session expired. Please login again.")
    return render_template('dashboard.html',name = name , show=True)

@app.route('/transfer', methods=['POST'])
def transfer():
    phone = session.get('phone')
    if not phone:
        return render_template('index.html', error="Session expired. Please login again.")

    user = usercollection.find_one({"Phone": phone})
    bank = bankcollection.find_one({"Phone": phone})
    
    if user and bank:
        return render_template('transaction.html')
    else:
        return render_template('index.html', error="User session expired. Please login again.")

@app.route('/transaction', methods=['POST'])
def transaction():
    phone = session.get('phone')
    if not phone:
        return render_template('index.html', error="Session expired. Please login again.")

    user = usercollection.find_one({"Phone": phone})
    bank = bankcollection.find_one({"Phone": phone})
    
    if not user or not bank:
        return render_template('index.html', error="User session expired. Please login again.")
    
    upiid = request.form['UPIID']
    rupi = bankcollection.find_one({"UPIID": upiid})
    if not rupi:
        return render_template('transaction.html', error="Invalid UPI ID")
    
    if upiid == bank['UPIID']:
        return render_template('transaction.html', error="Cannot transfer to your own UPI ID")

    upipin = request.form['UPIPIN']
    if not upipin.isdigit() or len(upipin) != 4:
        return render_template('transaction.html', error="Please enter a valid 4-digit UPI PIN")
    if bank['UPIPIN'] != upipin:
        return render_template('transaction.html', error="Incorrect UPI PIN")

    amount = int(request.form['amount'])
    if amount <= 0:
        return render_template('transaction.html', error="Please enter a valid amount")

    if bank['Balance'] < amount:
        return render_template('transaction.html', error="Insufficient balance")

    bankcollection.update_one({"UPIID": upiid}, {"$inc": {"Balance": amount}})
    bankcollection.update_one({"Phone": phone}, {"$inc": {"Balance": -amount}})
    return render_template('dashboard.html', name=user['Username'], message=f"Transaction successful! Amount transferred: {amount}", show=True)

if __name__ == '__main__':
    app.run(debug=True)