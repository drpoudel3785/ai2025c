from flask import Flask, render_template, request, redirect, url_for, session, make_response
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

#https://myaccount.google.com/apppasswords
# Mail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'dharmarajpoudel@gmail.com'
app.config['MAIL_PASSWORD'] = 'ihgpjqdlthauqpfe'
app.config['MAIL_DEFAULT_SENDER'] = 'dharmarajpoudel@gmail.com'
mail = Mail(app)

# Secret Key
app.secret_key = 'secret123'
# Token generator
serializer = URLSafeTimedSerializer(app.secret_key)

import mysql.connector
db = mysql.connector.connect(host="localhost",user="root", password="P@ssw0rd", database="ai2025c",port=3307)


@app.after_request
def disable_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route( '/')
def index():
   return render_template("index.html")

@app.route( '/about')
def about():
    return render_template("about.html")

@app.route( '/contact')
def contact():
   return render_template("contact.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND status=%s", 
            (username, 1)
        )
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # SESSION
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            # ROLE BASED REDIRECT
            if user['role'] == 'admin':
                redirect_url = url_for('admin_dashboard')
            else:
                redirect_url = url_for('user_dashboard')

            # COOKIE
            response = make_response(redirect(redirect_url))
            response.set_cookie('username', user['username'], max_age=60*60*24*15)

            return response
        else:
            msg = 'Invalid username or password'

    return render_template("login.html", msg=msg)

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, username, email, role, status FROM users")
        users = cursor.fetchall()
        total_users = len(users)   # COUNT USERS
        return render_template('admin/admin_dashboard.html', users=users,  total_users=total_users)
    

    return redirect(url_for('login'))


@app.route('/user/dashboard')
def user_dashboard():
    if 'loggedin' in session and session['role'] == 'user':
        return render_template('user/user_dashboard.html')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('login')))
    #response.delete_cookie('username')
    return response

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = db.cursor()

        # Check existing user
        cursor.execute("SELECT * FROM users WHERE email=%s OR username=%s", (email, username))
        account = cursor.fetchone()

        if account:
            return 'Account already exists!'
        else:
            hashed_password = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                (username, hashed_password, email)
            )
            db.commit()

            # Generate activation token
            token = serializer.dumps(email, salt='email-confirm')
            link = f"http://localhost:5000/activate/{token}"

            email_msg = Message(
                'Activate Your Account',
                recipients=[email]
            )
            email_msg.body = f'Click the link to activate your account:\n{link}'
            mail.send(email_msg)

            return 'Registration successful! Check your email.'

    return render_template("register.html")


@app.route('/activate/<token>')
def activate(token):
   try:
      email = serializer.loads(token, salt='email-confirm', max_age=3600)
   except:
      return "Activation link expired"
   cursor = db.cursor()
   cursor.execute("UPDATE users SET status=1, role='user' WHERE email=%s", (email,))
   db.commit()
   cursor.close()
   return "Account activated successfully!"

# @app.route( '/register', methods=['GET','POST'])
# def register():
#    if request.method=='GET':
#       return render_template("register.html")
#    else:
#       #capturing the data from the form
#       usr = request.form['username']
#       pwd = request.form['password']
#       eml = request.form['email']
#       cursor = db.cursor()
#       cursor.execute("INSERT INTO users(usernames, password, email) VALUES (%s, %s, %s)", (usr, pwd, eml))
#       db.commit()
#       db.close()
#       #return "Data Successfully Insterted"
#       return redirect(url_for('login'))

if __name__ == '__main__':
    app.run (host="127.0.0.1", port=5000, debug=True)