from flask import Flask

app = Flask(__name__)

#set FLASK_ENV = development
@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/about')
def about():
    return 'Hello, I am about !'

#Flask Variables & Rules
#To build dynamic URLs,  variable part can be added to rule parameters
#Labeled as  <variable-name>, passes an argument to associated function 
@app.route( '/hello/<name>')
def hello_name( name):
    string = "Hello " + name 
    return string

if __name__ == '__main__':
    app.run (host="127.0.0.1", port=5050, debug=True)

