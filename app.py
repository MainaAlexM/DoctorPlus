from flask import Flask,render_template ,request,url_for,flash,redirect,g,Response
from flask_sqlalchemy import SQLAlchemy
from flask_login  import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_mail import *




app = Flask(__name__)


   


   

 
   
        

if __name__ == '__main__':
    app.run(debug= True,host ="localhost")
