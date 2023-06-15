import sqlite3

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))




# Line below only required once, when creating DB.
# db.create_all()


@app.route('/')
def home():
    return render_template("index.html", logged_in= current_user.is_authenticated)



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.form:

        if db.session.query(User).filter(User.email == request.form["email"])[0]:
            flash("Email ID already registered, Use login option to Login with this email")

        else:
            password_input = request.form["password"]
            new_user = User(
                email=request.form["email"],
                password=generate_password_hash(password=password_input, method="pbkdf2", salt_length=8),
                name=request.form["name"]
            )

            db.session.add(new_user)
            db.session.commit()

            # Log in and authenticate user after adding details to database.
            login_user(new_user)
            return redirect(url_for("secrets", name=request.form["name"], logged_in=current_user.is_authenticated))


    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form:
            typed_email = request.form["email"]
            typed_password = request.form["password"]
            try:
                user_data = db.session.query(User).filter(User.email == typed_email).all()[0]
                if check_password_hash(pwhash=user_data.password, password=typed_password):
                    login_user(user_data)
                    flash('Logged in successfully.')
                    return redirect(url_for("secrets", name=user_data.name, logged_in=current_user.is_authenticated))
                else:
                    flash("Password doesnt match")

            except IndexError:
                flash("User name doesnt exist")


    return render_template("login.html" , logged_in=current_user.is_authenticated)


@app.route('/secrets/<name>')
@login_required
def secrets(name):
    return render_template("secrets.html", name=name, logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home", logged_in=current_user.is_authenticated))


@app.route('/download')
@login_required
def download():
        return send_from_directory("static", path="files/cheat_sheet.pdf", logged_in=current_user.is_authenticated)


if __name__ == "__main__":
    app.run(debug=True)
