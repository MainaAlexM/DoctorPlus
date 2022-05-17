from flask import render_template,request,redirect,url_for,abort,flash
from . import main
# from ..requests import 
# from .forms import 
# from ..models import User
# from .. import db,photos

# from flask_login import login_required,current_user

@main.route('/')
def index():


    return render_template('main/index.html')
