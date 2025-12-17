from flask import Flask, render_template, request, redirect
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path="/")

import mysql.connector
db = mysql.connector.connect(host="localhost",user="root", password="P@ssw0rd", database="ai2025c",port=3307)

@app.route( '/')
def index():
   return render_template("index.html")

@app.route( '/about')
def about():
    return render_template("about.html")

@app.route( '/contact')
def contact():
   return render_template("contact.html")

@app.route( '/login')
def login():
   return render_template("login.html")

@app.route( '/register', methods=['GET','POST'])
def register():
   if request.method=='GET':
      return render_template("register.html")
   else:
      #capturing the data from the form
      usr = request.form['username']
      pwd = request.form['password']
      eml = request.form['email']
      cursor = db.cursor()
      cursor.execute("INSERT INTO users(usernames, password, email) VALUES (%s, %s, %s)", (usr, pwd, eml))
      db.commit()
      db.close()
      #return "Data Successfully Insterted"
      return redirect(url_for('login'))

if __name__ == '__main__':
    app.run (host="127.0.0.1", port=5000, debug=True)