from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user


app = Flask(__name__)

@app.route("/")
def home():

    password = input("type your password")

    pass_hash = generate_password_hash(password=password, method="pbkdf2", salt_length= 3)
    print(pass_hash)

    validate = input("type to login")
    check = check_password_hash(pwhash=pass_hash, password=validate)
    print(check)



    return "Home"




if __name__ == "__main__":
    app.run(debug=True)