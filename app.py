from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('welcome.html')

# Registration page
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        data = request.get_json()
        return f"<h1>{data}</h1>"
        pass    # add the registration handling logic
    else:
        return render_template('register.html')

# Login Page
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        pass    # add the login handling logic
    else:
        return render_template('login.html')


if __name__=="__main__":
    app.run(debug=True)