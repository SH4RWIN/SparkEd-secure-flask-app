from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from dotenv import load_dotenv
import os
import logging
from dbm import check_email_exists, create_user, activate_user_email
from smtp import send_confirm_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature


# Configure logging
logging.basicConfig(
    filename='email_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
# load environment variables
load_dotenv()

app = Flask(__name__)
# Ensure you have a .env file with SECRET_KEY defined
secret_key = os.getenv('SECRET_KEY')
host = os.getenv('HOST', 'localhost')
app.secret_key = secret_key
# Set registration form validators

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

def create_verification_link(email):
    serializer = URLSafeTimedSerializer(secret_key)
    # create a verification link with this token
    protocol = "https" if os.getenv("FLASK_ENV") == "production" else "http"
    token = serializer.dumps(email, salt='email-verification')
    craft_url = f"http://{host}:5000/confirm?token={token}"
    return craft_url

@app.route('/test', methods=['GET'])
def test():
    return f"{create_verification_link("test@example.com")}"

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('welcome.html')

# AJAX endpoint to check if email exists
@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form.get('email')
    exists = check_email_exists(email)
    return jsonify({'exists': exists})

# Registration page
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        # AJAX submission expected
        if form.validate_on_submit():
            email = form.email.data
            if check_email_exists(email):
                return jsonify({'status': 'error', 'message': 'This email is already registered. Please log in or use a different email address.'})
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
            # Send confirmation email
            send_confirm_email(
                email=email,
                subject="SparkEd Email Verification",
                verification_link=create_verification_link(email)
            )
            session['pending_verification_email'] = email
            return jsonify({'status': 'success', 'redirect_url': url_for('confirm')})
        else:
            # Validation failed
            errors = []
            for field, msgs in form.errors.items():
                for msg in msgs:
                    errors.append(f"{field}: {msg}")
            return jsonify({'status': 'error', 'message': ' '.join(errors)})
    else:
        # GET request, render the form
        return render_template('register.html', form=form)

# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        pass    # add the login handling logic
    else:
        return render_template('login.html')


# Route for email confirmation
@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    token = request.args.get('token')

    if token:
        serializer = URLSafeTimedSerializer(secret_key)
        try:
            email = serializer.loads(token, salt='email-verification', max_age=300) # Token valid for 5 minutes
            # TODO: Implement activate_user_email(email) in dbm.py
            # activate_user_email(email)
            session.pop('pending_verification_email', None) # Clear session after verification
            flash('Email successfully verified! You can now log in.', 'success')
            return redirect(url_for('login'))
        except SignatureExpired:
            flash('The verification link has expired.', 'danger')
            return redirect(url_for('register'))
        except BadSignature:
            flash('Invalid verification link.', 'danger')
            return redirect(url_for('register'))
    else:
        # If no token, check session (for users who just registered and landed on the confirmation page)
        email = session.get('pending_verification_email')
        if not email:
            return redirect(url_for('register'))
        return render_template('confirmation.html', email=email)

if __name__=="__main__":
    app.run(debug=True)

