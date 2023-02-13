from flask_app import app, bcrypt
from flask import render_template, request, redirect, session, flash

from flask_app.models.user_model import User


@app.route("/")
def home():
    return render_template('index.html')


# *******- Check login credentials, creates user session - moves to next page -****************
@app.route("/login", methods=["POST"])
def login():

    logged_in_user = User.validate_login(request.form)
    
    if not logged_in_user:
        return redirect("/")

    session['uid'] = logged_in_user.id
    session['fname'] = logged_in_user.first_name

    return redirect('/dashboard')

# *******- Checks to see if user in session before welcoming to new page -****************
@app.route("/dashboard")
def welcome():
    if not 'uid' in session:
        flash("ACCESS DENIED. User not logged in.")
        return redirect("/")
    return render_template("dashboard.html")


# *******- Registers a new user -****************

@app.route('/new_user', methods=['POST'])
def new_user():


    register_check = User.validate(request.form)
    if not register_check:
        return redirect('/')

    hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": hash
    }

    User.register(data)
    return redirect("/")


# *******- Clears user from session (logout) -****************
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
