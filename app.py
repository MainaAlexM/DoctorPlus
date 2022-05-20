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


#login_manager.login_view  = 'get_signin_doctor'

# --------------------Model class------------------------
class User(UserMixin,db.Model):
     id = db.Column(db.Integer,primary_key =True)
     username = db.Column(db.String(100))
     email = db.Column(db.String(100),unique =True)
     password = db.Column(db.String(100))
     doctor = db.Column(db.Boolean)
     admin = db.Column(db.Boolean)
     work = db.Column(db.String(100))
     country = db.Column(db.String(100))
     image = db.Column(db.String(100))
     

     @property
     def unhashed_password(self):

          raise AttributeError('cannot view unhased password')

     @unhashed_password.setter
     def unhashed_password(self,unhashed_password):
          self.password = generate_password_hash(unhashed_password )



     appointment_by  = db.relationship('Appointments', 
     foreign_keys ='Appointments.asked_by_id',
     backref = 'asker',
     lazy=True
     
     )


     Receive_by  = db.relationship('Notiication', 
     foreign_keys ='Notiication.receive_by_id',
     backref = 'reciever',
     lazy=True
     
     )


     Sender_by  = db.relationship('Notiication', 
     foreign_keys ='Notiication.doctor_id',
     backref = 'sender',
     lazy=True
     
     )

     answers_requested  = db.relationship('Appointments', 
     foreign_keys ='Appointments.doctor_id',
     backref = 'expert',
     lazy=True
     
     )


# --------------------Model class------------------------

class Appointments(db.Model):

     id = db.Column(db.Integer,primary_key =True)
     name = db.Column(db.String(100))
     email = db.Column(db.String(100))
     date = db.Column(db.String(100))
     asked_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
     doctor_id = db.Column(db.Integer,db.ForeignKey('user.id'))



class Notiication(db.Model):

     id = db.Column(db.Integer,primary_key =True)
     name = db.Column(db.String(100))
     email = db.Column(db.String(100))
     date = db.Column(db.String(100))
     receive_by_id = db.Column(db.Integer,db.ForeignKey('user.id'))
     doctor_id = db.Column(db.Integer,db.ForeignKey('user.id'))





#==========================================#





@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))



@login_manager.unauthorized_handler
def unauthorized_callback():
     flash('register to access')
     return redirect(url_for('home'))



@app.route('/')
#@login_required


def home():
     return render_template('home.html')


@app.route('/add_appointment' , methods =['POST','GET ']) 

@login_required 

def add_appointment():

     name = request.form['name']
     email = request.form['email']
     date = request.form['date']
     doctor = request.form['doctor']
     
     add_appoint = Appointments(name =name,
     email =email,
     date =date,
     asked_by_id = current_user.id,
     doctor_id = doctor
)
     db.session.add(add_appoint)
     db.session.commit()
     
     flash("Successfull,Kindly check appointment at Manage ")
     
     return redirect(url_for('appointment'))


@app.route('/get_users')
@login_required
def get_users():
     usees = User.query.all()
     owner = User.query.filter_by(email=current_user.email,password=current_user.password,admin=True).first()
     if not owner:

          flash("The logins provided is not an admin!")
          return redirect(url_for('home'))
     
     else:

          return render_template('users.html', users = usees)

@app.route('/get_signin')
@login_required
def get_signin():
     owner = User.query.filter_by(email=current_user.email,password=current_user.password,admin=False,doctor =False).first()
     roww = db.session.query(Appointments.doctor_id == current_user.id).count()
     if not owner:

               flash("Kindly login as patient!")
               return redirect(url_for('home'))
          
     else:
               
          return render_template('dashboard.html',roww =roww)



@app.route('/get_signin_doctor' )
#@login_required
def get_signin_doctor(): 
     user_man = User.query.all()  
     doc_appoint = Appointments.query.filter_by(doctor_id =current_user.id).all()
     rows = db.session.query(Appointments.doctor_id == current_user.id).count()
     owner = User.query.filter_by(email=current_user.email,password=current_user.password,admin=False,doctor =True).first()
     if not owner:
          flash("Kindly login as Doctor !")
          return redirect(url_for('home'))

     else:
     
          return render_template('appointment_recieved.html' ,   appoints = doc_appoint,rows=rows)

     
     return render_template('doctor_dash.html',rows=rows)


@app.route('/get_signin_admin')
@login_required
def get_signin_admin():
     rows = db.session.query(User.doctor==0,User.admin==0).count()
     appoint_rows = db.session.query(Appointments).count()
     owner = User.query.filter_by(email=current_user.email,password=current_user.password,admin=True).first()
     if not owner:
          flash("The logins provided is not an admin!")
          return redirect(url_for('home'))
     
     else:

          return render_template('admin_dash.html' ,rows = rows )



@app.route('/get_appointment_recieved')
@login_required 
def get_appointment_recieved():
     rows = db.session.query(Appointments).count()

     doc_appoint = Appointments.query.filter_by(doctor_id =current_user.id).all()
     owner = User.query.filter_by(email=current_user.email,password=current_user.password,admin=False,doctor =True).first()
     if not owner:
          flash("Kindly login as patient !")
          return redirect(url_for('home'))

     else:
     
          return render_template('appointment_recieved.html' , appoints = doc_appoint,rows=rows)



@app.route('/dash')
@login_required
def dash():
     return render_template('dash.html')

@app.route('/doctor_dash')
@login_required
def doctor_dash():
     rows = db.session.query(Appointments).count()
     return render_template('doctor_dash.html',rows=rows)



@app.route('/get_signup')

def get_signup():
     return render_template('signup.html')


@app.route('/get_signup_doctor')

def get_signup_doctor():
     return render_template('signup_doctor.html')

@app.route('/logindoctor',methods = ['POST','GET'])
def logindoctor():
     #form = LoginForm()
     #if current_user.is_authenticated:
     #  return redirect(url_for('home'))
     #rows = db.session.query(User).count()
     
     email = request.form['email']
     password = request.form['password']
     owner = User.query.filter_by(email=email).first()

     if not owner or not check_password_hash(owner.password,password) :
          flash("Username or password is wrong")
          return   redirect(url_for('home'))
     else:

          login_user(owner)
          flash("Welcome")
          return   redirect(url_for('get_signin_doctor'))   


@app.route('/profile_doctor' ,methods = ['POST','GET'])
@login_required
def profile_doctor():
     rows = db.session.query(Appointments).count()
     owner = User.query.filter_by(email = current_user.email,password = current_user.password,doctor =True)
     get_usors = User.query.all()
     if not owner:
          flash('register or login to access page')
          return redirect(url_for('home'))

     else:
          return render_template('profile_doctor.html',users =get_usors,rows=rows)



@app.route('/register_patient',methods = ['POST','GET'])
def register_patient():

     username = request.form['username']
     email = request.form['email']
     #image = request.form['image']
     unhashed_password  = request.form['password']
     image = request.form['image']
     #image_filename = image.save(image)
     work = request.form['work']
     country = request.form['country']
     owner = User(username =username ,email =email,unhashed_password = unhashed_password,work=work,country=country,admin = False,image=image,doctor =False)
     db.session.add(owner)
     db.session.commit()
     #owner= user.query.filter_by(email=email).first()
     flash("successfull")
     
     return redirect(url_for('patients'))

@app.route('/register_doctor',methods = ['POST','GET'])
def register_doctor():

     username = request.form['username']
     email = request.form['email']
     image = request.form['image']
     # image_filename = image.save(image)
     unhashed_password  = request.form['password']
     work = request.form['work']
     country = request.form['country']

     owner = User(username =username ,email =email,work = work ,image=image,country = country,unhashed_password= unhashed_password,admin = False,doctor =True)
     db.session.add(owner)
     db.session.commit()
     #owner= user.query.filter_by(email=email).first()

     return redirect(url_for('get_signin_doctor'))


@app.route('/loginpatient',methods = ['POST','GET'])
def loginpatient ():
     email = request.form['email']
     password = request.form['password']
     owner = User.query.filter_by(email=email).first()

     if not owner or not check_password_hash(owner.password,password) :
          flash("Username or password is wrong")
          return   redirect(url_for('home'))
     else:

          login_user(owner)
          flash("Welcome")
          return   redirect(url_for('get_signin'))   



@app.route('/loginadmin',methods = ['POST','GET'])
def loginadmin():
     email = request.form['email']
     password = request.form['password']
     owner = User.query.filter_by(email=email,password=password,admin=True).first()
     if not owner:
          flash("Username or password is wrong")
          return   redirect(url_for('home'))
     else: 

          login_user(owner)
          flash("Welcome")
          return   redirect(url_for('get_signin_admin'))     



@app.route('/logout')
@login_required
def logout():
     logout_user()
     return redirect('/get_login') 





     

     
     
          

if __name__ == '__main__':
     app.run(debug= True,host ="localhost")
