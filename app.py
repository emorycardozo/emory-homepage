from flask import Flask, flash,  render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from dotenv import load_dotenv
import os

# Config dotenv
load_dotenv()

# Configure Application
app = Flask(__name__)

# Initialize Bootstrap
Bootstrap(app)

# App DataBase
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
    "SQLALCHEMY_TRACK_MODIFICATIONS")

# Secret Key Database
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# Initialize DB
db = SQLAlchemy(app)

# Initialize Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.after_request
def after_request(response):
    """Ensure response aren't cached"""
    response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    response.headers['Expires'] = 0
    response.headers['Pragma'] = 'no-cache'
    return response


# Create model

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False, unique=True)


with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Create a string

def __repr__(self):
    return '<Users%r>' % self.username


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    submit = SubmitField('Enviar')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    email = StringField(
        'E-mail', validators=[InputRequired(), Email('E-mail inválido'), Length(max=50)])
    password = StringField('Password', validators=[InputRequired(), EqualTo(
        'confirmation', message="Password don't Match"), Length(min=8, max=80)])
    confirmation = PasswordField(
        'Confirm Password', validators=[InputRequired()])
    submit = SubmitField('Enviar')


with app.app_context():
    db.create_all()

# Configure Routes


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/unama")
def unama():
    return render_template("unama.html")


@app.route("/diogosenior")
def diogosenior():
    return render_template("diogosenior.html")


@app.route("/priscilasenior")
def priscilasenior():
    return render_template("priscilasenior.html")


@app.route("/eldorado")
def eldorado():
    return render_template("eldorado.html")


@app.route("/hellenmonarcha")
def hellenmonarcha():
    return render_template("hellenmonarcha.html")


@app.route("/eu")
def emory():
    return render_template("emorycardozo.html")


@app.route("/linktree")
def linktree():
    return render_template("linktree.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    """Login user in"""
    if request.method == "POST":
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user:
                if check_password_hash(user.password_hash, form.password.data):
                    login_user(user)
                    flash("Login successfully!")
                    return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    """Register user in"""
    if request.method == "POST":
        if form.validate_on_submit():
            hash = generate_password_hash(form.password.data)
            new_user = Users(username=form.username.data,
                             email=form.email.data, password_hash=hash)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", name=current_user.username.capitalize())


@app.route("/logout")
@login_required
def logout():
    """Log user out"""
    logout_user()
    return redirect(url_for("login"))
