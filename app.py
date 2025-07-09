from flask import Flask, render_template, request, url_for, redirect, flash, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from dotenv import load_dotenv
import os
import logging
import requests
from dbm import check_email_exists, create_user, activate_user_email, check_user_credentials, get_user_by_email
from werkzeug.security import generate_password_hash
from smtp import send_confirm_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import threading

# Hashing and Verifying Passwords
# Currently uses Werkzeug's password hashing
# But Argon2 is the most recommended hashing algorithm for passwords.
# It is more secure and resistant to GPU-based attacks.
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

#TURNSTILE KEYS
CF_TURNSTILE_SITEKEY = os.getenv('CF_TURNSTILE_SITEKEY')
CF_TURNSTILE_SECRETKEY = os.getenv('CF_TURNSTILE_SECRETKEY')

# Set registration form validators
class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

# create link to sent as email confitmation
def create_verification_link(email):
    serializer = URLSafeTimedSerializer(secret_key)
    # create a verification link with this token
    protocol = "https" if os.getenv("FLASK_ENV") == "production" else "http"
    token = serializer.dumps(email, salt='email-verification')
    craft_url = f"http://{host}:5000/confirm?token={token}"
    return craft_url

@app.route('/', methods=['GET'])
def welcome():
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
        # Get Turnstile token from form
        turnstile_token = request.form.get('cf-turnstile-response')

        # Verify the Turnstile token
        verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        payload = {
            'secret': CF_TURNSTILE_SECRETKEY,
            'response': turnstile_token,
            'remoteip': request.remote_addr  # optional but recommended
        }
        try:
            response = requests.post(verify_url, data=payload)
            result = response.json()

            if result.get("success"):
                pass
        except:
            pass

        if form.validate_on_submit():   # checks if the request is POST and has
            email = form.email.data
            # Check if the email already exists
            if check_email_exists(email):
                return jsonify({'status': 'error', 'message': 'This email is already registered. Please log in or use a different email address.'})
            # Create the user in the database
            create_user(
                email=email,
                full_name=form.full_name.data,
                phone=form.phone.data,
                password=generate_password_hash(form.password.data),
                is_admin=0,
                is_active=1,
                email_verified=0
            )
            # Send confirmation email asynchronously, this improves perfomance at a massive scale
            email_thread = threading.Thread(
                target=send_email_async,
                args=(email, "SparkEd Email Verification", create_verification_link(email))
            )
            email_thread.start()

            session['pending_verification_email'] = email
            return jsonify({'status': 'success', 'redirect_url': url_for('confirm')})
        else:
            # Validation failed
            return jsonify({'status': 'error', 'message': 'Validation failed. Please check your input.'})
    else:
        # GET request, render the form
        return render_template('register.html', form=form, sitekey=CF_TURNSTILE_SITEKEY)

# Route for email confirmation
@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    token = request.args.get('token')

    if token:
        serializer = URLSafeTimedSerializer(secret_key)
        try:
            email = serializer.loads(token, salt='email-verification', max_age=300) # Token valid for 5 minutes
            activate_user_email(email)  # Activate the user's email in the database by assigning email_verified=1
            session.pop('pending_verification_email', None) # Clear session after verification
            flash('Email successfully verified! You can now log in.', 'success')    # Redirect to login page and say success
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

def send_email_async(email, subject, verification_link):
    with app.app_context():
        send_confirm_email(email, subject, verification_link)


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template('login.html', form=form, sitekey=CF_TURNSTILE_SITEKEY)
    
    if request.method == 'POST':
        # Get Turnstile token from form
        turnstile_token = request.form.get('cf-turnstile-response')

        # Verify the Turnstile token
        verify_url = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'
        payload = {
            'secret': CF_TURNSTILE_SECRETKEY,
            'response': turnstile_token,
            'remoteip': request.remote_addr  # optional but recommended
        }
        try:
            response = requests.post(verify_url, data=payload)
            result = response.json()

            if result.get("success"):
                # Token is valid, proceed with login logic
                email = request.form.get('email')
                password = request.form.get('password')

                if not email or not password:
                    return jsonify({'status': 'error', 'message': 'Email and Password are required.'}), 400

                user_match = check_user_credentials(email, password)
                if user_match:
                    session['user_email'] = user_match.email  # Store user email in session
                    return jsonify({'status': 'success', 'redirect_url': url_for('dashboard')})
                else:
                    return jsonify({'status': 'error', 'message': 'Invalid email or password.'}), 401
            else:
                # Token is invalid
                return jsonify({'status': 'error', 'message': 'human verification failed.'}), 400
        except Exception as e:
            # Handle potential errors during the API call
            logging.error(f"Turnstile verification failed: {e}")
            return jsonify({'status': 'error', 'message': 'unknown error occured!'}), 500


@app.route('/dashboard', methods=['GET'])
def dashboard():
    user_email = session.get('user_email')
    # Redirect non-logged in users to login
    if not user_email:
        return redirect(url_for('login'))

    user = get_user_by_email(user_email)
    if not user:
        # This case should ideally not happen if the user_email in session is valid
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    return render_template('dashboard.html', user=user)

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('welcome'))

# Even after logout, the browser might show cached pages when the user hits the back button. 
# To prevent this, add cache-control headers
@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__=="__main__":
    app.run(debug=True)

