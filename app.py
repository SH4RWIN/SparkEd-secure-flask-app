from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, EqualTo
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

app = Flask(__name__)
# Ensure you have a .env file with SECRET_KEY defined
secret_key = os.getenv('SECRET_KEY')
app.secret_key = secret_key 
# Set registration form validators

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm = StringField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])


@app.route('/', methods=['GET'])
def dashboard():
    return render_template('welcome.html')

# Registration page
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        # Add email verification logic here
        # After verification you can redirect to the email OTP verification page
    elif request.method == 'GET':
        return render_template('register.html', form=form)
    else:
        print(form.errors)
        return "Error Validating!" # render_template('register.html', form=form)

# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        pass    # add the login handling logic
    else:
        return render_template('login.html')

# frontend for email verification
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return render_template('verification.html')

if __name__=="__main__":
    app.run(debug=True)

