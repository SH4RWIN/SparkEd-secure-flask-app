from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, EqualTo
from dotenv import load_dotenv
import os
from dbm import check_email_exists, create_user

# load environment variables
load_dotenv()

app = Flask(__name__)
# Ensure you have a .env file with SECRET_KEY defined
secret_key = os.getenv('SECRET_KEY')
app.secret_key = secret_key
# Set registration form validators

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm = StringField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
# When you use Flask-WTF and FlaskForm, form data is parsed automatically from request.form and stored in each field's 
# .data attribute

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('welcome.html')

# Registration page
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():

        # Check if the email already exists
        email = form.email.data
        if check_email_exists(email):
            return render_template('register.html', form=form, error="Email already exists.")

        # Create the user in the database
        create_user(
            email=email,
            full_name=form.full_name.data,
            phone=form.phone.data,
            password=form.password.data,
            is_admin=0,
            is_active=1,
            email_verified=0
        )
        return render_template('verification.html', email=email)
        # After verifications and user creation you can redirect to the email OTP verification page
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

