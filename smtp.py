from flask import Flask
from flask_mail import Mail, Message
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)   

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
mail = Mail(app)

verification_email_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verify Your Email - SparkEd</title>
</head>
<body style="background: linear-gradient(135deg, #FCFCFC 0%, #FFFAE3 100%); font-family: 'Poppins', Arial, sans-serif; color: #333; margin:0; padding:0;">
  <div style="max-width: 420px; margin: 40px auto; background: #fff; border: 2px solid #F7567C; border-radius: 1.5rem; box-shadow: 0 8px 32px 0 rgba(247, 86, 124, 0.12); padding: 2.5rem 1.5rem;">
    <h2 style="color: #F7567C; text-align: center; font-weight: 600; margin-bottom: 1.5rem;">SparkEd Email Verification</h2>
    <p style="font-size: 1.1rem; text-align: center; margin-bottom: 2rem;">Thank you for registering with <b>SparkEd</b>!<br>Please click the button below to verify your email address:</p>
    <div style="text-align: center; margin-bottom: 2rem;">
      <a href="{verification_link}" style="background: linear-gradient(135deg, #F7567C 0%, #d6456a 100%); color: white; padding: 1rem 2rem; border-radius: 0.5rem; font-weight: 600; font-size: 1.1rem; text-decoration: none; display: inline-block;">Verify Email</a>
    </div>
    <p style="text-align: center; color: #666; font-size: 0.98rem;">This link is valid for 5 minutes.<br>If you did not request this, you can safely ignore this email.</p>
    <div style="text-align: center; margin-top: 2rem;">
      <span style="color: #F7567C; font-size: 1.1rem; font-weight: 500;">SparkEd Team</span>
    </div>
  </div>
</body>
</html>
'''

def send_confirm_email(email, subject, verification_link):
    
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.html = verification_email_html.format(verification_link=verification_link)

    try:
        with app.app_context():
            # Ensure the mail instance is initialized
            if not mail:
                raise Exception("Mail instance is not initialized.")
            # Send the email
            mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

# send_confirm_email("bennetsharwin76@gmail.com", "SparkEd Email Verification", "123456")
