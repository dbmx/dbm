import os
from datetime import datetime
from flask import Flask, render_template, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy


# Create Flask Instance
app = Flask(__name__)
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
#Secret Key
app.secret_key = os.urandom(32)
# Initialize the Database
db = SQLAlchemy(app)

# Create Model for Database
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    #Create String
    def __repr__(self):
        return '<Name %r>' % self.name

# Create Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create Database Tables Function
def create_db():
    with app.app_context():
        db.create_all()

# Routes Decorator
@app.route("/")
def index():
    first_name = "DBM"
    return render_template("index.html", first_name=first_name)


@app.route("/user/<name>")
def user(name):
    return render_template("user.html", user_name=name)


@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Name has Successfully submited.")
    return render_template("name.html", name=name, form=form)

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash(" Added Successfully.")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form, name=name, our_users=our_users)

# Invaild URL - Fixed.
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


# Invaild Server Error - Fixed.
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)
