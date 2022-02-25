

from http.client import NETWORK_AUTHENTICATION_REQUIRED




import flask
from flask import Flask, redirect, url_for, render_template, request, session, flash


from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import create_engine

from flask_wtf import FlaskForm, form

from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FieldList, FormField
from wtforms.fields.numeric import DecimalField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_bcrypt import Bcrypt
from flask_bootstrap import RESPONDJS_VERSION, Bootstrap
import sqlite3
import decimal
from decimal import Decimal
import pandas as pd

file_path = os.path.abspath(os.getcwd())+"\db.db"



app = Flask(__name__)

img_folder = os.path.join('static', 'img')
Bootstrap(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///'+file_path
app.config['SECRET_KEY'] = 'secretkey'
app.config['UPLOAD_FOLDER'] = img_folder

img_folder = os.path.join('static', 'img')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


network_list = []
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    network = db.Column(db.String(5))
    username = db.Column(db.String(20))
    password = db.Column(db.String(80))
    
    


class RegisterForm(FlaskForm):
    network = SelectField(u'Network', choices = [('Select', 'Select'),('2SM', '2SM'),( '6IX', '6IX'), ('ACE', 'ACE'), ('ARN', 'ARN'), ('NineRadio', 'NineRadio'), ('Nova', 'Nova'), ('RadioSport', 'RadioSport'), ('SCA', 'SCA'), ('SEN', 'SEN'), ('TAB', 'TAB')],  default='')
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
  


    def validate_username(self, username):
        existing_username = User.query.filter_by(username = username.data).first()
        if existing_username:
            raise ValidationError("That username already exists. Please choose a different one")
    
    def table_name(self, network):
         existing_network = User.query.filter_by(network = network.data).first()
         if existing_network:
             network_list.append(network.data)
             
   

class LoginForm(FlaskForm):
    network = SelectField(u'Network', choices = [('Select', 'Select'),('2SM', '2SM'),( '6IX', '6IX'), ('ACE', 'ACE'), ('ARN', 'ARN'), ('NineRadio', 'NineRadio'), ('Nova', 'Nova'), ('RadioSport', 'RadioSport'), ('SCA', 'SCA'), ('SEN', 'SEN'), ('TAB', 'TAB')],  default='')
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})




      

networks = []

class DropdownForm(FlaskForm):
    submitprofits = SubmitField('Submit')
    SydT1 =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    SydT2 =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    SydDirect =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    MelT1 =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    MelT2 =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    MelDirect =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    BriT1 =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    BriT2 =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    BriDirect =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    BriTotal =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    AdeTotal =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    PerTotal =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    PerT1 =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    PerT2 =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    PerDirect =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    AdeT1 =   DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    AdeT2 =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    AdeDirect =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
    MetroTotal =  DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
  

class DropdownForm_SEN(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2CH-Syd', '2CH-Syd'), ('SEN-Mel', 'SEN-Mel')],  default='')
    submit = SubmitField('Submit')
 
   

class DropdownForm_TAB(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2KY-Syd', '2KY-Syd'), ('4TAB-Bri', '4TAB-Bri')],  default='')
    submit = SubmitField('Submit')
 
    

class DropdownForm_SCA(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('MMM-Syd', 'MMM-Syd'), ('MMM-Mel', 'MMM-Mel'), ('MMM-Bri', 'MMM-Bri'), ('MMM-Ade', 'MMM-Ade'), ('92.9-Per', '92.9-Per'), ('2DayFM-Syd', '2DayFM-Syd'), ('FOXFM-Mel', 'FOXFM-Mel'), ('b105-Bri', 'b105-Bri'), ('Hit107-Ade', 'Hit107-Ade'), ('MIX94.5-Per', 'MIX94.5-Per')],  default='')
    submit = SubmitField('Submit')
 

   
class DropdownForm_RadioSport(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('927-Mel', '927-Mel')],  default='')
    submit = SubmitField('Submit')
 
    
class DropdownForm_Nova(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('Nova969-Syd', 'Nova969-Syd'), ('Nova100-Mel', 'Nova100-Mel'), ('Nova1069-Bri', 'Nova1069-Bri'), ('Nova919-Ade', 'Nova919-Ade')],  default='')
    submit = SubmitField('Submit')
 
class DropdownForm_NineRadio(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2GB-Syd', '2GB-Syd'), ('3AW-Mel', '3AW-Mel'), ('4BC-Bri', '4BC-Bri'), ('6PR-Per', '6PR-Per'), ('2UE-Syd', '2UE-Syd'), ('Magic1278-Mel', 'Magic1278-Mel'), ('NineDAB-Syd', 'NineDAB-Syd'), ('NineDAB-Mel', 'NineDAB-Mel'), ('NineDAB-Bri', 'NineDAB-Bri'), ('NineDAB-Per', 'NineDAB-Per'), ('NineStreaming-Metro', 'NineStreaming-Metro'), ('NinePodcast-Metro', 'NinePodcast-Metro')],  default='')
    submit = SubmitField('Submit')

class DropdownForm_ARN(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('KIIS1065-Syd', 'KIIS1065-Syd'), ('KIIS101.1-Mel', 'KIIS101.1-Mel'), ('New97.3-Bri', 'New97.3-Bri'), ('MIX102.3-Ade', 'MIX102.3-Ade'), ('96FM-Per', '96FM-Per'), ('WSFM-Syd', 'WSFM-Syd'), ('GOLD104.3-Mel', 'GOLD104.3-Mel'), ('4KQ-Bri', '4KQ-Bri'), ('Cruise-Ade', 'Cruise-Ade'), ('ARNDAB-Syd', 'ARNDAB-Syd'), ('ARNDAB-Mel', 'ARNDAB-Mel'), ('ARNDAB-Bri', 'ARNDAB-Bri'), ('ARNDAB-Ade', 'ARNDAB-Ade'), ('ARNDAB-Per', 'ARNDAB-Per'), ('ARNStreaming-Metro', 'ARNStreaming-Metro'), ('ARNPodcast-Metro', 'ARNPodcast-Metro')],  default='')
    submit = SubmitField('Submit')

class DropdownForm_ACE(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('3MP-Mel', '3MP-Mel'), ('2UE-Syd', '2UE-Syd'), ('Magic1278-Mel', 'Magic1278-Mel'), ('4BH-Bri', '4BH-Bri'), ('ACEDAB-Syd', 'ACEDAB-Syd'), ('ACEDAB-Mel', 'ACEDAB-Mel'), ('ACEDAB-Bri', 'ACEDAB-Bri'), ('ACEStreaming-Metro', 'ACEStreaming-Metro'), ('ACEPodcast-Metro', 'ACEPodcast-Metro')],  default='')
    submit = SubmitField('Submit')

class DropdownForm_6IX(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')],  default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('6IX-Per', '6IX-Per'), ('6IXDAB-Per', '6IXDAB-Per'), ('6IXStreaming-Metro', '6IXStreaming-Metro'), ('6IXPodcast-Metro', '6IXPodcast-Metro')],  default='')
    submit = SubmitField('Submit')

class DropdownForm_2SM(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2021M08', '2021M08'), ('2021M09', '2021M09')], default='')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')], default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2SM-Syd', '2SM-Syd'), ('2SMDAB-Syd', '2SMDAB-Syd'), ('2SMStreaming-Metro', '2SMStreaming-Metro'), ('2SMPodcast-Metro', '2SMPodcast-Metro')], default='')
    submit = SubmitField('Submit')

class ReportingForm(FlaskForm):
    month_select = SelectField(u'Month Code', choices = [(0,'Select'),('All', 'All'), ('2021M011', '2021M011'), ('2021M010', '2021M010')])
    station_select = SelectField(u'Station', choices = [(0, 'Select'),('All', 'All'), ('2CH-Syd', '2CH-Syd'),( 'SEN-Mel', 'SEN-Mel')])
    period_select = SelectField(u'Period', choices = [(0, 'Select'),('All', 'All'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit")




username_list = []
   
username_list = []
list_1 = []
list_2 = []
list_3 = []
list_4 = []
list_5 = []
list_6 = []
list_7 = []
list_8 = []
list_9 = []
list_10 = []
list_11 = []
list_12 = []
list_13 = []
list_14 = []
list_15 = []
list_16 = []
list_17 = []
list_18 = []

list_all = []

@app.route('/', methods=['GET', 'POST'])
def login():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CRA-logo-medium.jpg' )
    form = LoginForm()
 


    if form.validate_on_submit():
        user = User.query.filter_by(network=form.network.data, username=form.username.data).first()
        if user:
         
        

         
         username = '{}'.format(form.username.data)
        
         if bcrypt.check_password_hash(user.password, form.password.data):
               login_user(user) 
               if form.network.data != 'Select':
                return redirect(url_for('dashboard'))
               else:
                  message = "Please Enter a valid Network"
                  return render_template("login.html", form=form, user_image=pic1, message=message)

         else:
                message_1 = "Incorrect Password Entered. Please Check that you have Entered the correct Password"
                return render_template("login.html", form=form, user_image=pic1, message=message_1)
        else:
            message_2 = "Incorrect Username or Network entered"
            return render_template("login.html", form=form, user_image=pic1, message=message_2)

      
    else:
      return render_template("login.html", form=form, user_image=pic1)

    

var_list = []
list = []
contact_list = []
station_list = []
network_mkt = []
revenue_list = []

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = DropdownForm()
    if current_user.network == 'SEN':
     form_1 = DropdownForm_SEN()
    if current_user.network == 'TAB':
     form_1 = DropdownForm_TAB()
    if current_user.network == 'SCA':
     form_1 = DropdownForm_SCA()
    if current_user.network == 'NineRadio':
     form_1 = DropdownForm_NineRadio()
    if current_user.network == 'Nova':
     form_1 = DropdownForm_Nova()
    if current_user.network == 'ARN':
      form_1 = DropdownForm_ARN()
    if current_user.network == 'ACE':
       form_1 = DropdownForm_ACE()
    if current_user.network == '2SM':
        form_1 = DropdownForm_2SM()
     
    pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )
    if request.method == 'POST':
        

        
     station= '{}'.format(form_1.type4.data)
     month = '{}'.format(form_1.type2.data)
     contact = '{}'.format(form_1.type3.data)
         
     null = ""
     var_list.append(month)
     if null in var_list:
      var_list.remove(null)

     list.append(station)
        
     station_table_edit2.append(station)

     if station not in station_table:
      station_table.append(station)
         
     if null in station_table:
       station_table.remove(null)
       if null in station_table_edit2:
          station_table_edit2.remove(null)

     contact_list.append(contact)
        

    return render_template("dashboard.html", user_image=pic, network = current_user.network, form=form, form_1 = form_1)
    

@app.route('/register', methods=[ 'GET', 'POST'])
def register():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CRA-logo-medium.jpg' )
    form = RegisterForm()
    
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data)
      new_user = User(network = form.network.data, username=form.username.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
    
      return redirect(url_for('login'))

    return render_template("register.html", form=form, user_image=pic1)

station_table = []
station_table_edit2 = []
station_edit_Bri = []
station_edit_Bri.append('New97.3-Bri')
station_edit_Bri.append('4BH-Bri')
station_edit_Bri.append('4BC-Bri')
station_edit_Bri.append('Nova1069-Bri')
station_edit_Bri.append('MMM-Bri')
station_edit_Bri.append('b105-Bri')
station_edit_Bri.append('4TAB-Bri')
station_edit_Bri.append('4KQ-Bri')
station_edit_Bri.append('ACEDAB-Bri')
station_edit_Bri.append('ARNDAB-Bri')
station_edit_Bri.append('NineDAB-Bri')

station_edit_Ade = []
station_edit_Ade.append('MIX102.3-Ade')
station_edit_Ade.append('Cruise-Ade')
station_edit_Bri.append('Nova919-Ade')
station_edit_Bri.append('5aa-Ade')
station_edit_Bri.append('MMM-Ade')
station_edit_Bri.append('Hit107-Ade')
station_edit_Bri.append('ARNDAB-Ade')

station_edit_Per = []
station_edit_Per.append('6IX-Per')
station_edit_Per.append('96FM-Per')
station_edit_Per.append('6PR-Per')
station_edit_Per.append('6IXDAB-Per')
station_edit_Per.append('92.9-Per')
station_edit_Per.append('MIX94.5-Per')
station_edit_Per.append('ARNDAB-Per')
station_edit_Per.append('NineDAB-Per')


station_edit_Mel_Syd = []
station_edit_Mel_Syd.append('2SM-Syd')
station_edit_Mel_Syd.append('3MP-Mel')
station_edit_Mel_Syd.append('KIIS1065-Syd')
station_edit_Mel_Syd.append('KIIS101.1-Mel')
station_edit_Mel_Syd.append('WSFM-Syd')
station_edit_Mel_Syd.append('GOLD104.3-Mel')
station_edit_Mel_Syd.append('2GB-Syd')
station_edit_Mel_Syd.append('3AW-Mel')
station_edit_Mel_Syd.append('2UE-Syd')
station_edit_Mel_Syd.append('Magic1278-Mel')
station_edit_Mel_Syd.append('Nova969-Syd')
station_edit_Mel_Syd.append('Nova100-Mel')
station_edit_Mel_Syd.append('2SMDAB-Syd')
station_edit_Mel_Syd.append('2UE-Syd')
station_edit_Mel_Syd.append('Magic1278-Mel')
station_edit_Mel_Syd.append('927-Mel')
station_edit_Mel_Syd.append('MMM-Syd')
station_edit_Mel_Syd.append('SEN-Mel')
station_edit_Mel_Syd.append('2CH-Syd')
station_edit_Mel_Syd.append('ACEDAB-Syd')
station_edit_Mel_Syd.append('ACEDAB-Mel')
station_edit_Mel_Syd.append('ARNDAB-Syd')
station_edit_Mel_Syd.append('ARNDAB-Mel')
station_edit_Mel_Syd.append('NineDAB-Syd')
station_edit_Mel_Syd.append('NineDAB-Mel')



station_edit_Metro = []
station_edit_Metro.append('2SMStreaming-Metro')
station_edit_Metro.append('2SMPodcast-Metro')
station_edit_Metro.append('6IXStreaming-Metro')
station_edit_Metro.append('6IXPodcast-Metro')
station_edit_Metro.append('ACEStreaming-Metro')
station_edit_Metro.append('ACEPodcast-Metro')
station_edit_Metro.append('ARNStreaming-Metro')
station_edit_Metro.append('ARNPodcast-Metro')
station_edit_Metro.append('NineStreaming-Metro')
station_edit_Metro.append('NinePodcast-Metro')


@app.route('/edit', methods=['GET', 'POST'])
def edit():
 form = DropdownForm()
 if current_user.network == 'SEN':
  form_1 = DropdownForm_SEN()
 if current_user.network == 'TAB':
  form_1 = DropdownForm_TAB()
 if current_user.network == 'SCA':
  form_1 = DropdownForm_SCA()
 if current_user.network == 'NineRadio':
  form_1 = DropdownForm_NineRadio()
 if current_user.network == 'Nova':
  form_1 = DropdownForm_Nova()
 if current_user.network == 'ARN':
  form_1 = DropdownForm_ARN()
 if current_user.network == 'ACE':
  form_1 = DropdownForm_ACE()
 if current_user.network == '2SM':
  form_1 = DropdownForm_2SM()

 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )
 network = current_user.network

 if current_user.network == 'SEN':
        networks.append('2CH-Syd')
        networks.append('SEN-Mel')
        
 elif current_user.network == '2SM':
        networks.append("2SM-Syd")
 elif current_user.network == '6IX':
        networks.append("6IX-Per")
 elif current_user.network == 'ACE':
        networks.append("3MP-Mel")
 elif current_user.network == 'ARN':
        networks.append('KIIS1065-Syd')
        networks.append('KIIS101.1-Mel')
        networks.append('New97.3-Bri')
        networks.append('MIX102.3-Ade')
        networks.append('96FM-Per')
        networks.append("WSFM-Syd")
        networks.append("GOLD104.3-Mel")
        networks.append("4KQ-Bri")
        networks.append("Cruise-Ade")
 elif current_user.network == 'NineRadio':
        networks.append("2GB-Syd")
        networks.append("3AW-Mel")
        networks.append("4BC-Bri")
        networks.append("6PR-Per")
        networks.append("2UE-Syd")
        networks.append("Magic1278-Mel")
        networks.append("4BH-Bri")
 elif current_user.network == 'Nova':
        networks.append("Nova969-Syd")
        networks.append("Nova100-Mel")
        networks.append("Nova1069-Bri")  
        networks.append("Nova919-Ade")
        networks.append("Nova937-Per")
        networks.append("SmoothFM95.3-Syd")
        networks.append("SmoothFM91.5-Mel") 
        networks.append("5aa-Ade")
 elif current_user.network == 'RadioSport':
        networks.append("927-Mel")
 elif current_user.network == 'SCA':
        networks.append("MMM-Syd")
        networks.append("MMM-Mel")
        networks.append("MMM-Bri")  
        networks.append("MMM-Ade")
        networks.append("92.9-Per")
        networks.append("2DayFM-Syd")
        networks.append("FOXFM-Mel") 
        networks.append("b105-Bri")
        networks.append("Hit107-Ade")
        networks.append("MIX94.5-Per")
 elif current_user.network == 'TAB':
        networks.append('2KY-Syd')
        networks.append('4TAB-Bri')
      
 if var_list:
    month = var_list[-1]
    if month == "":
      month = var_list[-2]

 if list:
   station = list[-1]
   if station == "":
     station = list[-2]
    
 if contact_list:
   contact = contact_list[-1]
   if contact == "":
      contact = contact_list[-1]
   name = month + "-" + network + "-" + contact + "-" + station +  ".db"
    
          
  
         
       
       
       
        
       
        
        


 if request.method == 'POST':
   
         station= '{}'.format(form_1.type4.data)
         month = '{}'.format(form_1.type2.data)
         contact = '{}'.format(form_1.type3.data)
         
         null = ""
         var_list.append(month)
         if null in var_list:
          var_list.remove(null)

         list.append(station)
        
         station_table_edit2.append(station)

         if station not in station_table:
          station_table.append(station)
         
         if null in station_table:
          station_table.remove(null)
         if null in station_table_edit2:
          station_table_edit2.remove(null)
         
        
      
         contact_list.append(contact)
      
       
         if var_list:
          month = var_list[-1]
          if month == "":
           month = var_list[-2]
         if list:
          station = list[-1]
          if station == "":
           station = list[-2]
    
         if contact_list:
          contact = contact_list[-1]
          if contact == "":
           contact = contact_list[-2]
         form_1.type2.default = month
         form_1.type4.default = station
         form_1.type3.default = contact
         form_1.process()

       

         name = month + "-" + network + "-" + contact + "-" + station +  ".db"

         if name == ( "0" + "-" + network + "0" + "-" + "0" + ".db"):
          message_1 = ('Please make a selection from the credentials above')
          return render_template("edit_default.html", message_1 = message_1, form=form, form_1 = form_1, contact = contact, user_image=pic, network = current_user.network)

         if name == ( "0" + "-" + network + "-" + contact + "-" + station +  ".db"):
          message_1 = ('Please make a selection for Month')
          return render_template("edit_default.html", message_1 = message_1, form=form, form_1 = form_1, contact = contact, user_image=pic, network = current_user.network)

         if name == ( month + "-" + network + "-" + "0" + "-" + station +  ".db"):
          message_1 = ('Please make a selection for Contact')
          return render_template("edit_default.html", message_1 = message_1, form=form, form_1 = form_1, contact = contact, user_image=pic, network = current_user.network)
         if name == ( month + "-" + network + "-" + contact + "-" + "0" +  ".db"):
          message_1 = ('Please make a selection for Station')
          return render_template("edit_default.html", message_1 = message_1, form=form, form_1 = form_1, contact = contact, user_image=pic, network = current_user.network)


         conn = sqlite3.connect(name)
    
         with sqlite3.connect(name) as conn: 
          c = conn.cursor()
          listOfTables = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='Edit_table'; """).fetchall()
          
          if listOfTables != []:
           c.execute("SELECT SydT1 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
           user_SydT1 = form.SydT1.data
           SydT1 = c.fetchone()[0]
           form.SydT1.data = Decimal(SydT1)
      
           c.execute("SELECT SydT2 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
           user_SydT2 = form.SydT2.data
           SydT2 = c.fetchone()[0]
           form.SydT2.data = Decimal(SydT2)

           c.execute("SELECT SydDirect FROM Edit_table ORDER BY ID DESC LIMIT 1;")
         
           user_SydDirect = form.SydDirect.data
           SydDirect = c.fetchone()[0]
           form.SydDirect.data = Decimal(SydDirect)

           c.execute("SELECT MelT1 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
         
           user_MelT1 = form.MelT1.data
           MelT1 = c.fetchone()[0]
           form.MelT1.data = Decimal(MelT1)

           c.execute("SELECT MelT2 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
         
           user_MelT2 = form.MelT2.data
           MelT2 = c.fetchone()[0]
           form.MelT2.data = Decimal(MelT2)

           c.execute("SELECT MelDirect FROM Edit_table ORDER BY ID DESC LIMIT 1;")
         
           user_MelDirect = form.MelDirect.data
           MelDirect = c.fetchone()[0]
           form.MelDirect.data = Decimal(MelDirect)

           c.execute("SELECT BriTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
         
           user_BriTotal = form.BriTotal.data
           BriTotal = c.fetchone()[0]
           form.BriTotal.data = Decimal(BriTotal)

           c.execute("SELECT AdeTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
        
           user_AdeTotal = form.AdeTotal.data
           AdeTotal = c.fetchone()[0]
           form.AdeTotal.data = Decimal(AdeTotal)

           c.execute("SELECT PerTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
         
           user_PerTotal = form.PerTotal.data
           PerTotal = c.fetchone()[0]
           form.PerTotal.data = Decimal(PerTotal)
            
     
           revenue_list.append(user_SydT1)
           revenue_list.append(user_SydT2)
           revenue_list.append(user_SydDirect)
           revenue_list.append(user_MelT1)
           revenue_list.append(user_MelT2)
           revenue_list.append(user_MelDirect)
           revenue_list.append(user_BriTotal)
           revenue_list.append(user_AdeTotal)
           revenue_list.append(user_PerTotal)

         if form.submitprofits.data:
           if listOfTables != []:
            SydT1_data = user_SydT1
            SydT2_data = user_SydT2
            SydDirect_data = user_SydDirect
            MelT1_data = user_MelT1
            MelT2_data = user_MelT2
            MelDirect_data = user_MelDirect
            BriTotal_data = user_BriTotal
            AdeTotal_data = user_AdeTotal
            PerTotal_data = user_PerTotal
          
           form_1.type2.default = month
           form_1.type4.default = station
           form_1.type3.default = contact
           form_1.process()




           with sqlite3.connect(name) as conn: 
            d = conn.cursor()


          
            item = station_table_edit2[-1]
     
            if item in station_edit_Bri:
             d.execute("CREATE TABLE IF NOT EXISTS Edit_table (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriT1 NUMERIC(8), BriT2 NUMERIC(8), BriDirect NUMERIC(8), AdeTotal NUMERIC(8), PerTotal NUMERIC(8));")
             d.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriT1, BriT2, BriDirect, AdeTotal, PerTotal) values (?,?,?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriT1.data), str(form.BriT2.data),str(form.BriDirect.data), str(form.AdeTotal.data), str(form.PerTotal.data), ))
             message_2 = ("Successfully Updated")
             return  render_template("edit_Bri.html", form=form, message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)

            elif item in station_edit_Ade:
             e = conn.cursor()
             e.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriTotal NUMERIC(8), AdeT1 NUMERIC(8),  AdeT2 NUMERIC(8),  AdeDirect NUMERIC(8),  PerTotal NUMERIC(8));")
             e.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeT1, AdeT2, AdeDirect, PerTotal) values (?,?,?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriTotal.data), str(form.AdeT1.data), str(form.AdeT2.data), str(form.AdeDirect.data), str(form.PerTotal.data), ))
             message_2 = ("Successfully Updated")
             return  render_template("edit_Ade.html", form=form, message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
         
            

            elif item in station_edit_Per:
             f = conn.cursor()
             f.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriTotal NUMERIC(8), AdeTotal NUMERIC(8), PerT1 NUMERIC(8), PerT2 NUMERIC(8), PerDirect NUMERIC(8));")
             f.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeTotal, PerT1, PerT2, PerDirect) values (?,?,?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriTotal.data), str(form.AdeTotal.data), str(form.PerT1.data), str(form.PerT2.data),  str(form.PerDirect.data), ))
             message_2 = ("Successfully Updated")
             return  render_template("edit_Per.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
            
            
            elif item in station_edit_Metro:
             g = conn.cursor()
             g.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, MetroTotal NUMERIC(8));")
             g.execute("INSERT into Edit_table (MetroTotal) values (?)",(str(form.MetroTotal.data), ))
             message_2 = ("Successfully Updated")
             return  render_template("edit_Metro.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
            
            
            else:
             h = conn.cursor()
             h.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8),BriTotal NUMERIC(8), AdeTotal NUMERIC(8), PerTotal NUMERIC(8));")
             h.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeTotal, PerTotal) values (?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriTotal.data), str(form.AdeTotal.data), str(form.PerTotal.data), ))
             message_2 = ("Successfully Updated")
             return  render_template("edit.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
         
 if station_table_edit2:       
  item = station_table_edit2[-1]
     
  if item in station_edit_Bri:
           return  render_template("edit_Bri.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
  if item in station_edit_Ade:
           return  render_template("edit_Ade.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
  if item in station_edit_Per:
           return  render_template("edit_Per.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
  if item in station_edit_Metro:
           return  render_template("edit_Metro.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
  else:
           return  render_template("edit.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
         
 else:
  return render_template("edit_default.html", form=form, form_1 = form_1,  user_image=pic, network = current_user.network)


    

     


           
   
    
network_st = [] 

import numpy as np

@app.route('/review', methods=['GET', 'POST'])
def review():
 form = DropdownForm()
 if current_user.network == 'SEN':
  form_1 = DropdownForm_SEN()
 if current_user.network == 'TAB':
  form_1 = DropdownForm_TAB()
 if current_user.network == 'SCA':
  form_1 = DropdownForm_SCA()
 if current_user.network == 'NineRadio':
  form_1 = DropdownForm_NineRadio()
 if current_user.network == 'Nova':
  form_1 = DropdownForm_Nova()
 if current_user.network == 'ARN':
  form_1 = DropdownForm_ARN()
 if current_user.network == 'ACE':
  form_1 = DropdownForm_ACE()
 if current_user.network == '2SM':
  form_1 = DropdownForm_2SM()

 network = current_user.network
 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )
 

 
       
 if var_list:
     month = var_list[-1]
     if month == "":
         month = var_list[-2]
 if list:
     station = list[-1]
     if station == "":
         station = list[-2]
    
    
 if contact_list:
     contact = contact_list[-1]
     if contact == "":
         contact = contact_list[-2]

     for item in networks:
       if item != station:
        prev_station = item

     name = month + "-" + network + "-" + contact + "-" + station + ".db"
     conn = sqlite3.connect(name)
     cursor = conn.cursor() 
     
     incomplete_station_data = []
 
     for i in networks:  
      if i not in station_table:
       
       incomplete_station_data.append(i)

     if station_table != networks:
       message = ("The following stations have not been entered, please edit the following stations: ")
    
 

    
    

     if len(station_table) < 2:
      name = month + "-" + network + "-" + contact + "-" + station + ".db"
      conn = sqlite3.connect(name)
      cursor = conn.cursor() 
      cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
      data = cursor.fetchall()
    
      if station in station_edit_Bri:
        row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
      if station in station_edit_Ade:
        row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
      if station in station_edit_Per:
        row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
      if station in station_edit_Mel_Syd:
        row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
      if station in station_edit_Metro:
        row_df = pd.DataFrame(data = data, columns = ['', 'MetroTotal'])


      df = row_df.iloc[: , 1:]
      df.insert(loc=0, value=station, column = '')   
      df = df.pivot_table(index=[''])
      df.loc['Total Mkt',:]= df.sum(axis=0)
      df.loc[:,'Total Stn'] = df.sum(axis=1) 
      
      if current_user.network == 'ARN':
       return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station,  tables=[df.to_html(classes='data', header="true")], incomplete = incomplete_station_data[0], incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6], message = message ) 
      elif current_user.network == 'SEN':
       return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station,  tables=[df.to_html(classes='data', header="true")], incomplete = incomplete_station_data[0])

      
     if len(station_table) >= 2:
    
        station = list[-2]
        if station == "":
           station = list[-1]
        
        month = var_list[-1]
       
    
       

     if len(station_table) >= 2:
        
        for item in station_table:
         if item != station:
          prev_station = item 
         
        prev_month = var_list[-2]
        name_2 = prev_month + "-" + network + "-" + contact + "-" + prev_station + ".db"
        
        connection = sqlite3.connect(name_2)
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
        d = cursor.fetchall()  

     

     if len(station_table) == 2:
        with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()  
          if station in station_edit_Bri:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
          if station in station_edit_Ade:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
          if station in station_edit_Per:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
          if station in station_edit_Mel_Syd:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
          if station in station_edit_Metro:
           row_df = pd.DataFrame(data = data, columns = ['', 'MetroTotal'])

          if prev_station in station_edit_Bri:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
          if prev_station in station_edit_Ade:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
          if prev_station in station_edit_Per:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
          if prev_station in station_edit_Mel_Syd:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
          if prev_station in station_edit_Metro:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'MetroTotal'])
           
          df = pd.concat([row_df, row_df_2], ignore_index=True, sort=False).fillna(0)
          df = df.iloc[: , 1:]
          stations = []
          stations.append(station)
          stations.append(prev_station)

          df.insert(loc=0, value=stations, column = '')   
          df = df.pivot_table(index=[''])
          df.loc['Total Mkt',:]= df.sum(axis=0)
          df.loc[:,'Total Stn'] = df.sum(axis=1) 

          

          if current_user.network == 'ARN':
           return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station,  tables=[df.to_html(classes='data', header="true")], incomplete = incomplete_station_data[0], incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6], message = message ) 
          elif current_user.network == 'SEN':
           return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station,  tables=[df.to_html(classes='data', header="true")])
   
     if len(station_table) == 3:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[0]
         print(prev_prev_station)
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()  

         
          if station in station_edit_Bri:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
          if station in station_edit_Ade:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
          if station in station_edit_Per:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
          if station in station_edit_Mel_Syd:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
          if station in station_edit_Metro:
           row_df = pd.DataFrame(data = data, columns = ['', 'MetroTotal'])

          if prev_station in station_edit_Bri:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
          if prev_station in station_edit_Ade:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
          if prev_station in station_edit_Per:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
          if prev_station in station_edit_Mel_Syd:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
          if prev_station in station_edit_Metro:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'MetroTotal'])
        
          if prev_prev_station in station_edit_Bri:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
          if prev_prev_station in station_edit_Ade:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
          if prev_prev_station in station_edit_Per:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
          if prev_prev_station in station_edit_Mel_Syd:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
          if prev_prev_station in station_edit_Metro:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'MetroTotal'])
         
          df = pd.concat([row_df, row_df_2, row_df_3], ignore_index=True, sort=False).fillna(0)
          df = df.iloc[: , 1:]
          stations = []
          stations.append(station)
          stations.append(prev_station)
          stations.append(prev_prev_station)
          df.insert(loc=0, value=stations, column = '')   
          df = df.pivot_table(index=[''])
          df.loc['Total Mkt',:]= df.sum(axis=0)
          df.loc[:,'Total Stn'] = df.sum(axis=1) 

         
           
          return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")], message = message, incomplete = incomplete_station_data[0], incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6])
 
     

    

     if len(station_table) == 4:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[1]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
        
         prev_prev_prev_station = station_table[0]
   
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall() 
        
         if station in station_edit_Bri:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         if station in station_edit_Ade:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
         if station in station_edit_Per:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
         if station in station_edit_Mel_Syd:
           row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])

         if prev_station in station_edit_Bri:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         if prev_station in station_edit_Ade:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
         if prev_station in station_edit_Per:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
         if prev_station in station_edit_Mel_Syd:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
        
         if prev_prev_station in station_edit_Bri:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         if prev_prev_station in station_edit_Ade:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
         if prev_prev_station in station_edit_Per:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
         if prev_prev_station in station_edit_Mel_Syd:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])

         if prev_prev_prev_station in station_edit_Bri:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         if prev_prev_prev_station in station_edit_Ade:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
         if prev_prev_prev_station in station_edit_Per:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
         if prev_prev_prev_station in station_edit_Mel_Syd:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])




         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4], ignore_index=True, sort=False).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)

         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
      
         return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")], message = message, incomplete = incomplete_station_data[0], incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6])

    
     elif len(station_table) == 5:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[2]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
         prev_prev_prev_station = station_table[1]
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         prev_prev_prev_prev_month = var_list[-5]
         prev_prev_prev_prev_station = station_table[0]
         name_5 = prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_5)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         g = cursor.fetchall() 
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()
        
         if station in station_edit_Bri:
            row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
            row_df = pd.DataFrame(data = data, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_station in station_edit_Bri:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_2 = pd.DataFrame(data = d, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_station in station_edit_Bri:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_3 = pd.DataFrame(data = e, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_station in station_edit_Bri:
          row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_4 = pd.DataFrame(data = f, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station in station_edit_Bri:
          row_df_5 = pd.DataFrame(data = g, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_5 = pd.DataFrame(data = g, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4, row_df_5], ignore_index=True, sort=False).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_station)
         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
         df = df[['SydT1', 'SydT2', 'SydDirect', 'MelDirect', 'MelT1', 'MelT2', 'BriTotal', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal', 'PerT1', 'PerT2', 'PerDirect', 'Total Stn']]
         return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")], message=message, incomplete = incomplete_station_data[0], incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6])


     elif len(station_table) == 6:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[3]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
         prev_prev_prev_station = station_table[2]
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         prev_prev_prev_prev_month = var_list[-5]
         prev_prev_prev_prev_station = station_table[1]
         name_5 = prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_5)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         g = cursor.fetchall() 
         prev_prev_prev_prev_prev_month = var_list[-6]
         prev_prev_prev_prev_prev_station = station_table[0]
         name_6 = prev_prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_6)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         h = cursor.fetchall() 
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()
         if station == 'New97.3-Bri':
            row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
            row_df = pd.DataFrame(data = data, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_station == 'New97.3-Bri':
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_2 = pd.DataFrame(data = d, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_station == 'New97.3-Bri':
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_3 = pd.DataFrame(data = e, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_station == 'New97.3-Bri':
          row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_4 = pd.DataFrame(data = f, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_5 = pd.DataFrame(data = g, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_5 = pd.DataFrame(data = g, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_6 = pd.DataFrame(data = h, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_6= pd.DataFrame(data = h, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 

         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4, row_df_5, row_df_6], ignore_index=True, sort=False).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_prev_station)

         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
         df = df[['SydT1', 'SydT2', 'SydDirect', 'MelDirect', 'MelT1', 'MelT2', 'BriTotal', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal', 'PerT1', 'PerT2', 'PerDirect', 'Total Stn']]
         return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")], incomplete = incomplete_station_data[0], message=message, incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6])
   
     elif len(station_table) == 6:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[4]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
         prev_prev_prev_station = station_table[3]
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         prev_prev_prev_prev_month = var_list[-5]
         prev_prev_prev_prev_station = station_table[2]
         name_5 = prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_5)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         g = cursor.fetchall() 
         prev_prev_prev_prev_prev_month = var_list[-6]
         prev_prev_prev_prev_prev_station = station_table[1]
         name_6 = prev_prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_6)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         h = cursor.fetchall() 
         prev_prev_prev_prev_prev_prev_month = var_list[-7]
         prev_prev_prev_prev_prev_prev_station = station_table[0]
         name_7 = prev_prev_prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_7)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         i = cursor.fetchall() 
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()
        
         if station == 'New97.3-Bri':
            row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
            row_df = pd.DataFrame(data = data, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_station == 'New97.3-Bri':
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_2 = pd.DataFrame(data = d, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_station == 'New97.3-Bri':
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_3 = pd.DataFrame(data = e, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_station == 'New97.3-Bri':
          row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_4 = pd.DataFrame(data = f, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_5 = pd.DataFrame(data = g, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_5 = pd.DataFrame(data = g, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_6 = pd.DataFrame(data = h, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_6= pd.DataFrame(data = h, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_7 = pd.DataFrame(data = i, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_7 =  pd.DataFrame(data = i, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         
       
        
         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4, row_df_5, row_df_6, row_df_7], ignore_index=False, sort=False).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_prev_prev_station)

         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
         df = df[['SydT1', 'SydT2', 'SydDirect', 'MelDirect', 'MelT1', 'MelT2', 'BriTotal', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal', 'PerT1', 'PerT2', 'PerDirect', 'Total Stn']]
         return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")], incomplete = incomplete_station_data[0], incomplete_2 = incomplete_station_data[1], incomplete_3 = incomplete_station_data[2], incomplete_4 = incomplete_station_data[3], incomplete_5 = incomplete_station_data[4], incomplete_6 = incomplete_station_data[5], incomplete_7 = incomplete_station_data[6]) 
         
     
     
     return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, incomplete = incomplete_station_data)  

 

 return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network)


@app.route('/submit', methods=['GET', 'POST'])
def submit():
 network = current_user.network
 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )
 form = DropdownForm()
 if current_user.network == 'SEN':
    form_1 = DropdownForm_SEN()
 if current_user.network == 'TAB':
    form_1 = DropdownForm_TAB()
 if current_user.network == 'SCA':
    form_1 = DropdownForm_SCA()
 if current_user.network == 'NineRadio':
    form_1 = DropdownForm_NineRadio()
 if current_user.network == 'Nova':
    form_1 = DropdownForm_Nova()
 if current_user.network == 'ARN':
    form_1 = DropdownForm_ARN()
 if current_user.network == 'ACE':
    form_1 = DropdownForm_ACE()
 if current_user.network == '2SM':
    form_1 = DropdownForm_2SM()



 if var_list:
     month = var_list[-1]
     if month == "":
         month = var_list[-2]
 if list:
     station = list[-1]
     if station == "":
         station = list[-2]
    
 if contact_list:
     contact = contact_list[-1]
     if contact == "":
         contact = contact_list[-2]

     name = month + "-" + network + "-" + contact + "-" + station + ".db"
     conn = sqlite3.connect(name)
     cursor = conn.cursor() 

     def submit_table(station_function, month_function):
        columns_list = df.columns.values.tolist()
        df_new_1 = pd.DataFrame(columns_list)
        df_new_1['Month'] = 'July 2021' 
        df_new_1['Network'] = network
        df_new_1['UserName'] = contact
        df_new_1['Month Code'] = month_function
        df_new_1['Station'] = station_function
        df_post = df.transpose()
        df_post = df_post[:-1]
        column_1 = df_post.iloc[:, 1] 
        df_new_1.reset_index(drop=True, inplace=True)
        df_new_1["MktKey"] = df_new_1.iloc[:,5] + "_" + df_new_1.iloc[:,0]
        revenue = pd.concat([column_1])
        revenue.reset_index(drop=True, inplace=True)
        revenue = revenue.to_frame()
        df_new_1 = df_new_1.reindex()
        df_new_1 = df_new_1.merge(revenue, left_index=True, right_index=True)
        df_new_1['Station2'] = station_function
        
        # RENAMING COLUMNS IN DATAFRAME
      
        df_new_1.rename(columns={ df_new_1.columns[7]: "Revenue" }, inplace = True)
        df_new_1.rename(columns={ df_new_1.columns[0]: "Market_station" }, inplace = True)       
        df_new_1['Market'] = df_new_1['Station'].astype(str).str[-3:]
        df_new_1['Level'] = df_new_1['Market_station'].astype(str).str[3:] 
        return df_new_1



     if len(station_table) >= 1:
      name = month + "-" + network + "-" + contact + "-" + station + ".db"
      conn = sqlite3.connect(name)
      cursor = conn.cursor() 
      cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
      data = cursor.fetchall()
    
      if station in station_edit_Bri:
         row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
      if station in station_edit_Mel_Syd:
         row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
      if station in station_edit_Ade:
         row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
      if station in station_edit_Per:
         row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
      if station in station_edit_Metro:
          row_df = pd.DataFrame(data = data, columns = ['', 'MetroTotal'])

      df = row_df.iloc[: , 1:]
      stations = []
      stations.append(station)
      df.insert(loc=0, value=stations, column = '')   
      df = df.pivot_table(index=[''])
      df.loc['Total Mkt',:]= df.sum(axis=0)
      df.loc[:,'Total Stn'] = df.sum(axis=1) 
  
     
      table =  submit_table(station, month)
      print(table)

      print("")
      
       
        
        
     
        
        
      
       
       
    
     
     if len(station_table) >= 2:
    
        station = list[-2]
        if station == "":
           station = list[-1]
        
        month = var_list[-1]
        for item in station_table:
         if item != station:
          prev_station = item
        prev_month = var_list[-2]
         
        
        name_2 = prev_month + "-" + network + "-" + contact + "-" + prev_station + ".db"
        connection = sqlite3.connect(name_2)
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
        d = cursor.fetchall()  

        if prev_station in station_edit_Bri:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
        if prev_station in station_edit_Ade:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
        if prev_station in station_edit_Per:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
        if prev_station in station_edit_Mel_Syd:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
        if prev_station in station_edit_Metro:
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'MetroTotal'])
           
        df = pd.concat([row_df, row_df_2], ignore_index=True).fillna(0)
        df = df.iloc[: , 1:]
     
     
        stations.append(prev_station)

        df.insert(loc=0, value=stations, column = '')   
        df = df.pivot_table(index=[''])
        df.loc['Total Mkt',:]= df.sum(axis=0)
        df.loc[:,'Total Stn'] = df.sum(axis=1) 

         
         
   
         
        table1 = submit_table(prev_station, prev_month)
        final_table = pd.concat([table, table1])
        print(final_table)

          
        
        
      
     if len(station_table) >= 3:

        prev_month_2 = var_list[-3]
        prev_station_2 = station_table[0]
        name_3 = prev_month_2 + "-" + network + "-" + contact + "-" + prev_station_2 + ".db"
        connection = sqlite3.connect(name_3)
        cursor = connection.cursor() 
        cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
        e = cursor.fetchall()  
         
       
      
        
        if prev_station_2 in station_edit_Bri:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
        if prev_station_2 in station_edit_Ade:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
        if prev_station_2 in station_edit_Per:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
        if prev_station_2 in station_edit_Mel_Syd:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])
        if prev_station_2 in station_edit_Metro:
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'MetroTotal'])
         
        df = pd.concat([row_df, row_df_2, row_df_3], ignore_index=True).fillna(0)
        df = df.iloc[: , 1:]
        
        stations.append(prev_station_2)
        df.insert(loc=0, value=stations, column = '')   
        df = df.pivot_table(index=[''])
        df.loc['Total Mkt',:]= df.sum(axis=0)
        df.loc[:,'Total Stn'] = df.sum(axis=1) 
      
        table3 = submit_table(prev_station_2, prev_month_2)
          
       
    
    

     if len(station_table) >= 4:
          
         prev_month_3 = var_list[-4]
        
         prev_station_3 = station_table[0]
   
         name_4 = prev_month_3 + "-" + network + "-" + contact + "-" + prev_station_3 + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         

        


         if prev_station_3 in station_edit_Bri:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         if prev_station_3 in station_edit_Ade:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeT1', 'AdeT2', 'AdeDirect', 'PerTotal'])
         if prev_station_3 in station_edit_Per:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerT1', 'PerT2', 'PerDirect'])
         if prev_station_3 in station_edit_Mel_Syd:
           row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal', 'AdeTotal', 'PerTotal'])


         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4], ignore_index=True).fillna(0)
         df = df.iloc[: , 1:]
        
         stations.append(prev_station_3)

         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 

         df_new_3 = pd.DataFrame(columns_list)
         df_new_3['Month'] = 'July 2021' 
         df_new_3['Network'] = network
         df_new_3['UserName'] = contact
         df_new_3['Month Code'] = prev_month_3
         df_new_3['Station'] = prev_station_3
       
         df_post = df.transpose()
         df_post = df_post[:-1]
         
         column_1 = df_post.iloc[:, 3] 
        
          
         df_new_3.reset_index(drop=True, inplace=True)
         
         df_new_3["MktKey"] = df_new_3.iloc[:,5] + "_" + df_new_3.iloc[:,0]
         revenue = pd.concat([column_1])
         revenue.reset_index(drop=True, inplace=True)
         revenue = revenue.to_frame()
         df_new_3 = df_new_3.reindex()
         df_new_3 = df_new_3.merge(revenue, left_index=True, right_index=True)
         df_new_3['Station2'] = prev_station_3
        
        # RENAMING COLUMNS IN DATAFRAME
      
         df_new_3.rename(columns={ df_new_3.columns[7]: "Revenue" }, inplace = True)
         df_new_3.rename(columns={ df_new_3.columns[0]: "Market_station" }, inplace = True)

       
         df_new_3['Market'] = df_new_3['Station'].astype(str).str[-3:]
         df_new_3['Level'] = df_new_3['Market_station'].astype(str).str[3:] 
     


     
     if len(station_table) >= 5:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[2]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
         prev_prev_prev_station = station_table[1]
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         prev_prev_prev_prev_month = var_list[-5]
         prev_prev_prev_prev_station = station_table[0]
         name_5 = prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_5)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         g = cursor.fetchall() 
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()
        
         if station == 'New97.3-Bri':
            row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
            row_df = pd.DataFrame(data = data, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_station == 'New97.3-Bri':
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_2 = pd.DataFrame(data = d, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_station == 'New97.3-Bri':
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_3 = pd.DataFrame(data = e, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_station == 'New97.3-Bri':
          row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_4 = pd.DataFrame(data = f, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_5 = pd.DataFrame(data = g, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_5 = pd.DataFrame(data = g, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4, row_df_5], ignore_index=True).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_station)
         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
         df = df[['SydT1', 'SydT2', 'SydDirect', 'MelDirect', 'MelT1', 'MelT2', 'BriTotal', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal', 'Total Stn']]
         return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")])

     elif len(station_table) == 6:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[3]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
         prev_prev_prev_station = station_table[2]
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         prev_prev_prev_prev_month = var_list[-5]
         prev_prev_prev_prev_station = station_table[1]
         name_5 = prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_5)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         g = cursor.fetchall() 
         prev_prev_prev_prev_prev_month = var_list[-6]
         prev_prev_prev_prev_prev_station = station_table[0]
         name_6 = prev_prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_6)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         h = cursor.fetchall() 
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()
         if station == 'New97.3-Bri':
            row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
            row_df = pd.DataFrame(data = data, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_station == 'New97.3-Bri':
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_2 = pd.DataFrame(data = d, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_station == 'New97.3-Bri':
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_3 = pd.DataFrame(data = e, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_station == 'New97.3-Bri':
          row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_4 = pd.DataFrame(data = f, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_5 = pd.DataFrame(data = g, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_5 = pd.DataFrame(data = g, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_6 = pd.DataFrame(data = h, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_6= pd.DataFrame(data = h, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 

         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4, row_df_5, row_df_6], ignore_index=True).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_prev_station)

         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
         df = df[['SydT1', 'SydT2', 'SydDirect', 'MelDirect', 'MelT1', 'MelT2', 'BriTotal', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal', 'Total Stn']] 
         return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")])
     
     elif len(station_table) == 6:
         prev_prev_month = var_list[-3]
         prev_prev_station = station_table[4]
         name_3 = prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_station + ".db"
         connection = sqlite3.connect(name_3)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         e = cursor.fetchall()  
         prev_prev_prev_month = var_list[-4]
         prev_prev_prev_station = station_table[3]
         name_4 = prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_4)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         f = cursor.fetchall()  
         prev_prev_prev_prev_month = var_list[-5]
         prev_prev_prev_prev_station = station_table[2]
         name_5 = prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_5)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         g = cursor.fetchall() 
         prev_prev_prev_prev_prev_month = var_list[-6]
         prev_prev_prev_prev_prev_station = station_table[1]
         name_6 = prev_prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_6)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         h = cursor.fetchall() 
         prev_prev_prev_prev_prev_prev_month = var_list[-7]
         prev_prev_prev_prev_prev_prev_station = station_table[0]
         name_7 = prev_prev_prev_prev_prev_prev_month + "-" + network + "-" + contact + "-" + prev_prev_prev_prev_prev_prev_station + ".db"
         connection = sqlite3.connect(name_7)
         cursor = connection.cursor() 
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         i = cursor.fetchall() 
         with sqlite3.connect(name) as conn:
          cursor = conn.cursor() 
          cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
          data = cursor.fetchall()
        
         if station == 'New97.3-Bri':
            row_df = pd.DataFrame(data = data, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
            row_df = pd.DataFrame(data = data, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_station == 'New97.3-Bri':
           row_df_2 = pd.DataFrame(data = d, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_2 = pd.DataFrame(data = d, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_station == 'New97.3-Bri':
           row_df_3 = pd.DataFrame(data = e, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
           row_df_3 = pd.DataFrame(data = e, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_station == 'New97.3-Bri':
          row_df_4 = pd.DataFrame(data = f, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_4 = pd.DataFrame(data = f, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_5 = pd.DataFrame(data = g, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_5 = pd.DataFrame(data = g, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_6 = pd.DataFrame(data = h, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_6= pd.DataFrame(data = h, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         if prev_prev_prev_prev_station == 'New97.3-Bri':
          row_df_7 = pd.DataFrame(data = i, columns = ['', 'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal'])
         else:
          row_df_7 =  pd.DataFrame(data = i, columns = ['',  'SydT1', 'SydT2', 'SydDirect', 'MelT1', 'MelT2', 'MelDirect', 'BriTotal',  'AdeTotal', 'PerTotal']) 
         
       
        
         df = pd.concat([row_df, row_df_2, row_df_3, row_df_4, row_df_5, row_df_6, row_df_7], ignore_index=False).fillna(0)
         df = df.iloc[: , 1:]
         stations = []
         stations.append(station)
         stations.append(prev_station)
         stations.append(prev_prev_station)
         stations.append(prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_prev_station)
         stations.append(prev_prev_prev_prev_prev_prev_station)

         df.insert(loc=0, value=stations, column = '')   
         df = df.pivot_table(index=[''])
         df.loc['Total Mkt',:]= df.sum(axis=0)
         df.loc[:,'Total Stn'] = df.sum(axis=1) 
         df = df[['SydT1', 'SydT2', 'SydDirect', 'MelDirect', 'MelT1', 'MelT2', 'BriTotal', 'BriT1', 'BriT2', 'BriDirect', 'AdeTotal', 'PerTotal', 'Total Stn']]
         return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, station = station, prev_station=prev_station, tables=[df.to_html(classes='data', header="true")])
      
       
         
       
     
       
     
        
       
       
      
       
       
      
     else:
        return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network = current_user.network, station=station, contact = contact, month = month, tables=[df.to_html(classes='data', header="true")])
 else:
     return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network = current_user.network) 
   

  
   

 
   
  




 



@app.route("/reporting",  methods=['GET', 'POST'])
def reporting():
 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )
 form  = ReportingForm()

 
 if request.method == 'POST':
    dataset = pd.read_excel("CRA-2021M11DB-Revenue-000-final-anubhav-dummy-20210117-final.xlsx", sheet_name='Data')
    
    if current_user.network == 'SEN':
      dataset = dataset[dataset.Network == 'SEN']
    if current_user.network == 'ARN':
      dataset = dataset[dataset.Network == 'ARN']
    if current_user.network == 'TAB':
      dataset = dataset[dataset.Network == 'TAB']
    if current_user.network == 'SCA':
      dataset = dataset[dataset.Network == 'SCA']
    if current_user.network == 'NineRadio':
      dataset = dataset[dataset.Network == 'NineRadio']
    if current_user.network == 'Nova':
      dataset = dataset[dataset.Network == 'Nova']
    if current_user.network == 'ACE':
      dataset = dataset[dataset.Network == 'ACE']
    if current_user.network == '2SM':
      dataset = dataset[dataset.Network == '2SM']

   
    dataset = dataset.groupby(['Period', 'RevenueGroup', 'CalendarMonth', 'Station'], as_index=False).sum()
 

    def percentage_change(col1,col2):
     return ((col2 - col1) / col1) * 100
    
   
    def table_format(dataset):
     dataset = dataset.groupby(['Period', 'RevenueGroup'], as_index=False).sum()
     dataset = dataset.drop('MktGrowth%', axis=1)
     dataset = dataset.drop('StnGrowth%', axis=1)
     dataset = dataset.drop('RevenueOrder', axis=1)
     dataset['MktGrowth%'] = percentage_change(dataset['MktPrevious'],dataset['MktCurrent']) 
     dataset['StnGrowth%'] = percentage_change(dataset['StnPrevious'],dataset['StnCurrent']) 
     dataset = dataset[['Period', 'RevenueGroup', 'MktCurrent', 'MktPrevious', 'MktGrowth%', 'StnCurrent', 'StnPrevious', 'StnGrowth%', 'MktShrCurrent', 'MktShrPrevious', 'RankCurrent', '#StnsCurrent', 'RankPrevious', 'NumStnsPrevious']]
     dataset = dataset.reset_index(drop=True)
     dataset = dataset.round(2)
     return dataset

    def table_format_row_index(dataset):
     dataset = dataset.groupby(['Period', 'RevenueGroup'], as_index=False).sum()
     dataset = dataset.drop('MktGrowth%', axis=1)
     dataset = dataset.drop('StnGrowth%', axis=1)
     dataset = dataset.drop('RevenueOrder', axis=1)
     dataset['MktGrowth%'] = percentage_change(dataset['MktPrevious'],dataset['MktCurrent']) 
     dataset['StnGrowth%'] = percentage_change(dataset['StnPrevious'],dataset['StnCurrent']) 
     dataset = dataset[['Period', 'RevenueGroup', 'MktCurrent', 'MktPrevious', 'MktGrowth%', 'StnCurrent', 'StnPrevious', 'StnGrowth%', 'MktShrCurrent', 'MktShrPrevious', 'RankCurrent', '#StnsCurrent', 'RankPrevious', 'NumStnsPrevious']]
     dataset = dataset.reindex([11, 12, 14, 10, 13, 5, 6, 8, 4, 7, 1, 0, 9, 3, 2])
     dataset = dataset.reset_index(drop=True)
     dataset = dataset.round(2)
     return dataset

  
    
    
    
  
    
    if form.month_select.data == '2021M010':
      if form.station_select.data == 'All':
        if form.period_select.data == 'All':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_All_All.xlsx")

         link = "/static/reports/Report_2021M10_All_Month.xlsx"      
         return render_template("reporting.html", form=form, user_image=pic, link = link, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'Month':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Period == 'Month']
         dataset = table_format_row_index(dataset)
      
         dataset.to_excel("static/reports/Report_2021M10_All_Month.xlsx")
        
         link = "/static/reports/Report_2021M10_All_Month.xlsx"
         
         
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

        elif form.period_select.data == 'CYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Period == 'CYTD']
         dataset = table_format_row_index(dataset)
         dataset.to_excel("static/reports/Report_2021M10_All_CYTD.xlsx")
         link = "/static/reports/Report_2021M10_All_CYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")])  
        
        elif form.period_select.data == 'FYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Period == 'FYTD']
         dataset = table_format_row_index(dataset)
         dataset.to_excel("static/reports/Report_2021M10_All_FYTD.xlsx")
         link = "/static/reports/Report_2021M10_All_FYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

      elif form.station_select.data == '2CH-Syd':
        if form.period_select.data == 'All':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_2CH-Syd_All.xlsx")
         link = "/static/reports/Report_2021M10_2CH-Syd_All.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'Month':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = dataset[dataset.Period == 'Month']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_2CH-Syd_Month.xlsx")
         link = "static/reports/Report_2021M10_2CH-Syd_Month.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'CYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = dataset[dataset.Period == 'CYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_2CH-Syd_CYTD.xlsx")
         link = "/static/reports/Report_2021M10_2CH-Syd_CYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
      
        elif form.period_select.data == 'FYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = dataset[dataset.Period == 'FYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_2CH-Syd_FYTD.xlsx")
         link = "/static/reports/Report_2021M10_2CH-Syd_FYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

      elif form.station_select.data == 'SEN-Mel':

        if form.period_select.data == 'All':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_SEN-Mel_All.xlsx")
         link = "/static/reports/Report_2021M10_SEN-Mel_All.xlsx"

         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

        elif form.period_select.data == 'Month':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = dataset[dataset.Period == 'Month']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_SEN-Mel_Month.xlsx")
         link = "/static/reports/Report_2021M10_SEN-Mel_Month.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'CYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = dataset[dataset.Period == 'CYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_SEN-Mel_CYTD.xlsx")
         link = "/static/reports/Report_2021M10_SEN-Mel_CYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        

        elif form.period_select.data == 'FYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M10']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = dataset[dataset.Period == 'FYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M10_SEN-Mel_FYTD.xlsx")
         link = "/static/reports/Report_2021M10_SEN-Mel_FYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

    if form.month_select.data == '2021M011':
      if form.station_select.data == 'All':
        if form.period_select.data == 'All':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_All_All.xlsx")
         link = "/static/reports/Report_2021M11_All_All.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'Month':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Period == 'Month']
         dataset = table_format_row_index(dataset)
         dataset.to_excel("static/reports/Report_2021M11_All_Month.xlsx")
         link = "/static/reports/Report_2021M11_All_Month.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

        elif form.period_select.data == 'CYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Period == 'CYTD']
         dataset = table_format_row_index(dataset)
         dataset.to_excel("static/reports/Report_2021M11_All_CYTD.xlsx")
         link = "/static/reports/Report_2021M11_All_CYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'FYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Period == 'FYTD']
         dataset = table_format_row_index(dataset)
         dataset.to_excel("static/reports/Report_2021M11_All_FYTD.xlsx")
         link = "/static/reports/Report_2021M11_All_FYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

      elif form.station_select.data == '2CH-Syd':
        if form.period_select.data == 'All':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_2CH-Syd_All.xlsx")
         link = "/static/reports/Report_2021M11_2CH-Syd_All.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'Month':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = dataset[dataset.Period == 'Month']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_2CH-Syd_Month.xlsx")
         link = "/static/reports/Report_2021M11_2CH-Syd_Month.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'CYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = dataset[dataset.Period == 'CYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_2CH-Syd_CYTD.xlsx")
         
         link = "/static/reports/Report_2021M11_2CH-Syd_CYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
      
        elif form.period_select.data == 'FYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == '2CH-Syd (DUMMY)']
         dataset = dataset[dataset.Period == 'FYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_2CH-Syd_FYTD.xlsx")
         link = "/static/reports/Report_2021M11_2CH-Syd_FYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")])  

      elif form.station_select.data == 'SEN-Mel':
        if form.period_select.data == 'All':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
        
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_SEN-Mel_All.xlsx")
         link = "/static/reports/Report_2021M11_SEN-Mel_All.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

        elif form.period_select.data == 'Month':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = dataset[dataset.Period == 'Month']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_SEN-Mel_Month.xlsx")
         link = "/static/reports/Report_2021M11_SEN-Mel_Month.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        
        elif form.period_select.data == 'CYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = dataset[dataset.Period == 'CYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_SEN-Mel_CYTD.xlsx")
         link = "/static/reports/Report_2021M11_SEN-Mel_CYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 
        

        elif form.period_select.data == 'FYTD':
         dataset = dataset[dataset.CalendarMonth == '2021M11']
         dataset = dataset[dataset.Station == 'SEN-Mel (DUMMY)']
         dataset = dataset[dataset.Period == 'FYTD']
         dataset = table_format(dataset)
         dataset.to_excel("static/reports/Report_2021M11_SEN-Mel_FYTD.xlsx")
         link = "/static/reports/Report_2021M11_SEN-Mel_FYTD.xlsx"
         return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data, link = link, tables=[dataset.to_html(classes='data', header="true")]) 

  

        

          
         
         
        

       
 return render_template("reporting.html", user_image=pic, network = current_user.network, form=form, period = form.period_select.data, month = form.month_select.data, station = form.station_select.data) 


@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == 'main':
 app.run(debug=True, port=8080, host='0.0.0.0')