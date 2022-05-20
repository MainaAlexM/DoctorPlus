from flask import Flask,render_template ,request,url_for,flash,redirect,g,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login  import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import *




app = Flask(__name__)

mail = Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'apptestermind@gmail.com'
app.config['MAIL_PASSWORD'] = 'Apptester20#'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

app.secret_key = 'secrete key'
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///employer.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hosp.db'
app.config['SECRET_KEY'] = '0527'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['TESTING'] = False

db = SQLAlchemy(app)
#ap = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app )
login_manager.login_view = 'login'


   


   

 
   
        

if __name__ == '__main__':
    app.run(debug= True,host ="localhost")
