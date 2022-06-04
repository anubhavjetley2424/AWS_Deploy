

from locale import currency
from flask import Flask, current_app, redirect, url_for, render_template, request, session, flash


from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
import os

from sqlalchemy import create_engine

from flask_wtf import FlaskForm, form

from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FieldList, FormField, BooleanField
from wtforms.fields.numeric import DecimalField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_bcrypt import Bcrypt
from flask_bootstrap import RESPONDJS_VERSION, Bootstrap
import sqlite3
import decimal
from decimal import Decimal
import pandas as pd
import datetime as dt
import boto3
from waitress import serve

file_path = os.path.abspath(os.getcwd())+ "\db.db"



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
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    
    
    


class RegisterForm(FlaskForm):
    network = SelectField(u'Network', choices = [('Select', 'Select'),('2SM', '2SM'),( '6IX', '6IX'), ('ACE', 'ACE'), ('ARN', 'ARN'), ('NineRadio', 'NineRadio'), ('Nova', 'Nova'), ('RadioSport', 'RadioSport'), ('SCA', 'SCA'), ('SEN', 'SEN'), ('TAB', 'TAB')],  default='')
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")
  


    def validate_email(self, email):
        existing_email = User.query.filter_by(email = email.data).first()
        if existing_email:
            raise ValidationError("That email already exists. Please choose a different one")
    
    def table_name(self, network):
         existing_network = User.query.filter_by(network = network.data).first()
         if existing_network:
             network_list.append(network.data)
             
   

class LoginForm(FlaskForm):
    network = SelectField(u'Network', choices = [('Select', 'Select'),('2SM', '2SM'),( '6IX', '6IX'), ('ACE', 'ACE'), ('ARN', 'ARN'), ('NineRadio', 'NineRadio'), ('Nova', 'Nova'), ('RadioSport', 'RadioSport'), ('SCA', 'SCA'), ('SEN', 'SEN'), ('TAB', 'TAB')],  default='')
    email = StringField(validators=[InputRequired(), Length(min=4, max=80)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})




      
radio_network = []
network_SEN  = []
network_ACE = []
network_TAB = []
network_ARN = []
network_2SM = []
network_NineRadio = []
network_SCA = []
network_RadioSport = []
network_Nova = []
network_6IX = []

network_current = []
network_final = []

class DropdownForm(FlaskForm):
   
    submitprofits = SubmitField('Update')
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
    fillzeroes = BooleanField('Fill Zeroes')
    tester = DecimalField(validators=[InputRequired(), Length(min=1, max=100)])
   

   


today = dt.date.today()
first = today.replace(day=1)
lastmonth = first - dt.timedelta(days=1)
lastmonth = lastmonth.strftime("%m")

month_dict = {
"01" : "2022M01",
"02" : "2022M02",
"03" : "2022M03", 
"04" : "2022M04", 
"05" : "2022M05", 
"06" : "2022M06",
"07" : "2022M07",
"08" : "2022M08", 
"09" : "2022M09",
"10" : "2022M10", 
"11" : "2022M11",
"12" : "2022M12"

}

month = month_dict[lastmonth]

network_dict = {
  "SEN" : ["2CH-Syd", "SEN-Mel", "SENDAB-Syd", "SENDAB-Mel", "SENStreaming-National", "SENPodcast-National"],
  "TAB" : ["2KY-Syd", "4TAB-Bri", "TABDAB-Syd", "TABDAB-Bri", "TABStreaming-National", "TABPodcast-National" ],
  "SCA" : ["MMM-Syd", "MMM-Mel", "MMM-Bri", "MMM-Ade", "92.9-Per", "2DayFM-Syd", "FOXFM-Mel", "b105-Bri", "Hit107-Ade", "MIX94.5-Per", "SCADAB-Syd", "SCADAB-Mel", "SCADAB-Bri", "SCADAB-Ade", "SCADAB-Per", "SCAStreaming-National", "SCAPodcast-National" ],
  "RadioSport" : ["927-Mel", "RadioSportDAB-Mel", "RadioSportStreaming-National", "RadioSportPodcast-National"],
  "Nova" : ["Nova969-Syd", "Nova100-Mel", "Nova1069-Bri", "Nova1069-Bri", "Nova919-Ade", "Nova937-Per", "SmoothFM95.3-Syd", "SmoothFM91.5-Mel", "5aa-Ade", "NovaDAB-Syd", "NovaDAB-Mel", "NovaDAB-Ade", "NovaDAB-Bri", "NovaDAB-Per", "NovaStreaming-National", "NovaPodcast-National"],
  "6IX" : ["6IX-Per", "6IXDAB-Per", "6IXStreaming-National", "6IXPodcast-National"],
  "ACE" : ["3MP-Mel", "2UE-Syd", "Magic1278-Mel", "4BH-Bri", "ACEDAB-Syd", "ACEDAB-Mel", "ACEDAB-Bri", "ACEStreaming-National", "ACEPodcast-National"],
  "ARN" : ["KIIS1065-Syd", "KIIS101.1-Mel" , "New97.3-Bri", "MIX102.3-Ade", "96FM-Per", "WSFM-Syd", "GOLD104.3-Mel", "4KQ-Bri", "Cruise-Ade", "ARNDAB-Syd", "ARNDAB-Mel", "ARNDAB-Bri", "ARNDAB-Ade", "ARNDAB-Per", "ARNStreaming-National", "ARNPodcast-National"],
  "NineRadio" : ["2GB-Syd", "3AW-Mel", "4BC-Bri", "6PR-Per", "NineDAB-Syd", "NineDAB-Mel", "NineDAB-Bri", "NineDAB-Per", "NineStreaming-Nat", "NinePodcast-Nat"],
  "2SM" : ["2SM-Syd", "2SMDAB-Syd", "2SMStreaming-National", "2SMPodcast-National"]
}


class DropdownForm_SEN(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit')]) # ('Reporting', 'Reporting') 
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
   
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2CH-Syd', '2CH-Syd'), ('SEN-Mel', 'SEN-Mel'), ('SENDAB-Syd', 'SENDAB-Syd'), ('SENDAB-Mel', 'SENDAB-Mel'), ('SENStreaming-National', 'SENStreaming-National'), ('SENPodcast-National', 'SENPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')
 
   

class DropdownForm_TAB(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
   
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2KY-Syd', '2KY-Syd'), ('4TAB-Bri', '4TAB-Bri'), ('TABDAB-Syd', 'TABDAB-Syd'), ('TABDAB-Bri', 'TABDAB-Bri'), ('TABStreaming-National', 'TABStreaming-National'), ('TABPodcast-National', 'TABPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')
    
 
    

class DropdownForm_SCA(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
   
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('MMM-Syd', 'MMM-Syd'), ('MMM-Mel', 'MMM-Mel'), ('MMM-Bri', 'MMM-Bri'), ('MMM-Ade', 'MMM-Ade'), ('92.9-Per', '92.9-Per'), ('2DayFM-Syd', '2DayFM-Syd'), ('FOXFM-Mel', 'FOXFM-Mel'), ('b105-Bri', 'b105-Bri'), ('Hit107-Ade', 'Hit107-Ade'), ('MIX94.5-Per', 'MIX94.5-Per'), ('SCADAB-Syd', 'SCADAB-Syd'), ('SCADAB-Mel', 'SCADAB-Mel'), ('SCADAB-Bri', 'SCADAB-Bri'), ('SCADAB-Ade', 'SCADAB-Ade'), ('SCADAB-Per', 'SCADAB-Per'), ('SCAStreaming-National', 'SCAStreaming-National'), ('SCAPodcast-National', 'SCAPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')
 

   
class DropdownForm_RadioSport(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
  
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('927-Mel', '927-Mel'), ('RadioSportDAB-Mel', 'RadioSportDAB-Mel'), ('RadioSportStreaming-National', 'RadioSportStreaming-National'), ('RadioSportPodcast-National', 'RadioSportPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')
 
    
class DropdownForm_Nova(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
  
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('Nova969-Syd', 'Nova969-Syd'), ('Nova100-Mel', 'Nova100-Mel'), ('Nova1069-Bri', 'Nova1069-Bri'), ('Nova919-Ade', 'Nova919-Ade'), ('Nova937-Per', 'Nova937-Per'), ('SmoothFM95.3-Syd', 'SmoothFM95.3-Syd'), ('SmoothFM91.5-Mel', 'SmoothFM91.5-Mel'), ('5aa-Ade', '5aa-Ade'),('NovaDAB-Syd', 'NovaDAB-Syd'), ('NovaDAB-Mel', 'NovaDAB-Mel'), ('NovaDAB-Bri', 'NovaDAB-Bri'), ('NovaDAB-Ade', 'NovaDAB-Ade'), ('NovaDAB-Per', 'NovaDAB-Per'), ('NovaStreaming-National', 'NovaStreaming-National'), ('NovaPodcast-National', 'NovaPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'),('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')
 
class DropdownForm_NineRadio(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
   
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2GB-Syd', '2GB-Syd'), ('3AW-Mel', '3AW-Mel'), ('4BC-Bri', '4BC-Bri'), ('6PR-Per', '6PR-Per'),  ('NineDAB-Syd', 'NineDAB-Syd'), ('NineDAB-Mel', 'NineDAB-Mel'), ('NineDAB-Bri', 'NineDAB-Bri'), ('NineDAB-Per', 'NineDAB-Per'), ('NineStreaming-Nat', 'NineStreaming-Nat'), ('NinePodcast-Nat', 'NinePodcast-Nat')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')

class DropdownForm_ARN(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
    
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('KIIS1065-Syd', 'KIIS1065-Syd'), ('KIIS101.1-Mel', 'KIIS101.1-Mel'), ('New97.3-Bri', 'New97.3-Bri'), ('MIX102.3-Ade', 'MIX102.3-Ade'), ('96FM-Per', '96FM-Per'), ('WSFM-Syd', 'WSFM-Syd'), ('GOLD104.3-Mel', 'GOLD104.3-Mel'), ('4KQ-Bri', '4KQ-Bri'), ('Cruise-Ade', 'Cruise-Ade'), ('ARNDAB-Syd', 'ARNDAB-Syd'), ('ARNDAB-Mel', 'ARNDAB-Mel'), ('ARNDAB-Bri', 'ARNDAB-Bri'), ('ARNDAB-Ade', 'ARNDAB-Ade'), ('ARNDAB-Per', 'ARNDAB-Per'), ('ARNStreaming-National', 'ARNStreaming-National'), ('ARNPodcast-National', 'ARNPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit")
   
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')

class DropdownForm_ACE(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
    type3 = SelectField(u'Network Contact', choices = [(0, 'Select'),('Ian Garland', 'Ian Garland'), ('Anubhav Jetley', 'Anubhav Jetley')],  default='')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('3MP-Mel', '3MP-Mel'), ('2UE-Syd', '2UE-Syd'), ('Magic1278-Mel', 'Magic1278-Mel'), ('4BH-Bri', '4BH-Bri'), ('ACEDAB-Syd', 'ACEDAB-Syd'), ('ACEDAB-Mel', 'ACEDAB-Mel'), ('ACEDAB-Bri', 'ACEDAB-Bri'), ('ACEStreaming-National', 'ACEStreaming-National'), ('ACEPodcast-National', 'ACEPodcast-National')],  default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')

class DropdownForm_6IX(FlaskForm):
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
   
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('6IX-Per', '6IX-Per'), ('6IXDAB-Per', '6IXDAB-Per'), ('6IXStreaming-National', '6IXStreaming-National'), ('6IXPodcast-National', '6IXPodcast-National')], default='') 
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'),('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')])
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')

class DropdownForm_2SM(FlaskForm):
  
    type = SelectField(u'Action Type', choices=  [(0, 'Select'),('Introduction', 'Introduction'), ('Edit', 'Edit'), ('Review', 'Review'), ('Submit', 'Submit'), ('Reporting', 'Reporting')])
    type2 = SelectField(u'Month Code', choices = [(0,'Select'),('2022M01', '2022M01'), ('2022M02', '2022M02'), ('2022M03','2022M03'), ('2022M04', '2022M04'), ('2022M05', '2022M05'), ('2022M06', '2022M06'), ('2022M07', '2022M07'), ('2022M08', '2022M08'), ('2022M09', '2022M09'), ('2022M10', '2022M10'), ('2022M11', '2022M11'), ('2022M12', '2022M12')],  default='2022M05')
    type4 = SelectField(u'Station', choices = [(0, 'Select'),('2SM-Syd', '2SM-Syd'), ('2SMDAB-Syd','2SMDAB-Syd'),('2SMStreaming-National', '2SMStreaming-National'), ('2SMPodcast-National', '2SMPodcast-National')], default='')
    submit = SubmitField('Submit')
    period_select = SelectField(u'Period', choices = [(0, 'Select'), ('Month', 'Month'), ('CYTD', 'CYTD'),('FYTD', 'FYTD')], default='')
    submitrevenue = SubmitField(label="Submit Data")
    calendar_month = SelectField(u'Calendar Month', choices = [(0,'Select'),('2021M10', '2021M10'), ('2021M11', '2021M11')],  default='')









username_list = []
   
email_list = []

station_table = []

@app.route('/', methods=['GET', 'POST'])
def login():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CRA-logo-medium.jpg' )
    form = LoginForm()
 
    if len(station_table) > 0:

      station_table.clear()
      dashboard_var_list.clear()

    if form.validate_on_submit():
        user = User.query.filter_by(network=form.network.data, email=form.email.data).first()
        if user:
         
        

         
         email = '{}'.format(form.email.data)
         email_list.append(email)
        
         if bcrypt.check_password_hash(user.password, form.password.data):
               login_user(user) 
               if form.network.data != 'Select':
                radio_network.append(form.network.data)
               
                return redirect(url_for('dashboard'))
               else:
                  message = "Please Enter a valid Network"
                  return render_template("login.html", form=form, user_image=pic1, message=message)

         else:
                message_1 = "Incorrect Password Entered. Please Check that you have Entered the correct Password"
                return render_template("login.html", form=form, user_image=pic1, message=message_1)
        else:
            message_2 = "Incorrect Email or Network entered"
            return render_template("login.html", form=form, user_image=pic1, message=message_2)

      
    else:
      return render_template("login.html", form=form, user_image=pic1)

    

var_list = []
list_st = []
dashboard_var_list = []

station_list = []
network_mkt = []
revenue_list = []


thisdict =	{
  "Adam.Bainbridge@sca.com.au" : "Adam Bainbridge", 
  "anubhav.jetley123@gmail.com" : "Anubhav Jetley",
  "radio97@superradionetwork.com.au" : "Robyn Maclean",
  "degroote@capitalradio.net.au" : "Angela De Groote",
  "elliott@blytongroup.com.au" : "Josh Elliott",
  "darylf@team.aceradio.com.au" : "Daryl Foster",
  "mraco@aceradio.com.au" : "Maria Raco",
  "Abbyzhang@arn.com.au" : "Abby Zhang",
  "sooshin@arn.com.au" : "Soo Shin",
  "caroline.anderson@macquariemedia.com.au" : "Caroline Anderson",
  "anderson@capitalradio.net.au" : "Amanda Anderson",
  "darylf@team.aceradio.com.au" : "Daryl Foster",
  "deanne.hassett@macquariemedia.com.au" : "Deanne Hassett",
  "abloor@novaentertainment.com.au" : "Anna Bloor",
  "mduncan@novaentertainment.com.au" : "Michael Duncan",
   
  "mchappell@novaentertainment.com.au" : "Mark Chappell",
  "sallywalker@novaentertainment.com.au" : "Sally Walker",
  "Accounts@rsn.net.au" : "RSN Accounts",
  "shaneC@rsn.net.au" : "Shane Caruana",
  "Sharon.whishwilson@sca.com.au" : "Sharon Whishwilson",
  "ian.vendargon@sen.com.au" : "Ian Vendargon",
  "ivendargon@sen.com.au": "Ian Vendargon",
  "teresa.leung@sen.com.au" : "Teresa Leung",
  "kevin.buckley@tabcorp.com.au" : "Kevin Buckley",
  "iang@gmail.com": "IanG",
  "anubhav" : "AJ", 
  "bmcgee@novaentertainment.com.au" : "Ben McGee"
  

}


contact_list = []
contacts = []

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    form_2 = LoginForm()
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
    if current_user.network == 'RadioSport':
       form_1 = DropdownForm_RadioSport()
    if current_user.network == '6IX':
       form_1 = DropdownForm_6IX()
    
   
    

    contact = thisdict.get(current_user.email)
   
    contact_list.append(contact)

    #if len(dashboard_var_list) == 0:
      #base_path = os.getcwd()
      #s3 = boto3.client('s3', aws_access_key_id = 'access', aws_secret_access_key = 'secret')
      #x = dt.datetime.now()
      #logged_in = "Logged In" + "-" + current_user.network + "-" + x.strftime('%Y') + "-" + x.strftime('%m')  + "-" +  x.strftime('%d') + "-" + x.strftime('%H') + "-" + x.strftime('%M') + "-" + current_user.email + ".txt"
      #logged_in_path = os.path.join(base_path + "\\" + 'this_folder' + '\\' + logged_in)
      #open(logged_in_path, 'a').close()
      #s3.upload_file(logged_in_path, 'miltondata-radio1', logged_in )
    
  
    for i in contact_list:
      if i not in contacts:
        contacts.append(i)
   
    if len(contacts) >= 2:
      list_st.clear()
      station_table.clear()
      dashboard_var_list.clear()
      

     
     
      
      
      
      
      

      
      
  
    
   
     
    pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )

    
    if request.method == 'POST':
        
     
        
     
     month = '{}'.format(form_1.type2.data)
     
         
     null = ""
     dashboard_var_list.append(month)
     if null in dashboard_var_list:
      dashboard_var_list.remove(null)
    
    

  
    
    if len(dashboard_var_list) >= 1:
      month = dashboard_var_list[-1]
      form_1.type2.default = month
      form_1.process()
    

    
   
     
    
   
        

    return render_template("dashboard.html", user_image=pic, network = current_user.network, contact= contact, form=form, form_1 = form_1, form_2 = form_2)
    

@app.route('/register', methods=[ 'GET', 'POST'])
def register():
    pic1 = os.path.join(app.config['UPLOAD_FOLDER'], 'CRA-logo-medium.jpg' )
    form = RegisterForm()
    
    if form.validate_on_submit():
      hashed_password = bcrypt.generate_password_hash(form.password.data)
      new_user = User(network = form.network.data, email=form.email.data, password=hashed_password)
      db.session.add(new_user)
      db.session.commit()
    
      return redirect(url_for('login'))

    return render_template("register.html", form=form, user_image=pic1)


station_table_edit2 = []
station_edit_Bri = []
station_edit_Bri.append('New97.3-Bri')
station_edit_Bri.append('4BH-Bri')
station_edit_Bri.append('4BC-Bri')
station_edit_Bri.append('Nova1069-Bri')
station_edit_Bri.append('MMM-Bri')
station_edit_Bri.append('b105-Bri')
station_edit_Bri.append('TABDAB-Bri')
station_edit_Bri.append('4KQ-Bri')
station_edit_Bri.append('ACEDAB-Bri')
station_edit_Bri.append('ARNDAB-Bri')
station_edit_Bri.append('NineDAB-Bri')
station_edit_Bri.append('SCADAB-Bri')
station_edit_Bri.append('ARNDAB-Bri')
station_edit_Bri.append('Nova1069-Bri')
station_edit_Bri.append('4TAB-Bri')
station_edit_Bri.append('NovaDAB-Bri')

station_edit_Ade = []
station_edit_Ade.append('MIX102.3-Ade')
station_edit_Ade.append('Cruise-Ade')
station_edit_Ade.append('Nova919-Ade')
station_edit_Ade.append('5aa-Ade')
station_edit_Ade.append('MMM-Ade')
station_edit_Ade.append('Hit107-Ade')
station_edit_Ade.append('ARNDAB-Ade')
station_edit_Ade.append('SCADAB-Ade')
station_edit_Ade.append('ACEDAB-Ade')
station_edit_Ade.append('Nova919-Ade')
station_edit_Ade.append('NovaDAB-Ade')


station_edit_Per = []
station_edit_Per.append('6IX-Per')
station_edit_Per.append('96FM-Per')
station_edit_Per.append('6PR-Per')
station_edit_Per.append('6IXDAB-Per')
station_edit_Per.append('92.9-Per')
station_edit_Per.append('MIX94.5-Per')
station_edit_Per.append('ARNDAB-Per')
station_edit_Per.append('NineDAB-Per')
station_edit_Per.append('SCADAB-Per')
station_edit_Per.append('ACEDAB-Per')
station_edit_Per.append('Nova937-Per')
station_edit_Per.append('NovaDAB-Per')


station_edit_Mel_Syd = []
#2SM
station_edit_Mel_Syd.append('2SM-Syd')
station_edit_Mel_Syd.append('2SMDAB-Syd')



#ACE

station_edit_Mel_Syd.append('3MP-Mel')
station_edit_Mel_Syd.append('2UE-Syd')
station_edit_Mel_Syd.append('ACEDAB-Syd')
station_edit_Mel_Syd.append('ACEDAB-Mel')
station_edit_Mel_Syd.append('Magic1278-Mel')




#ARN
station_edit_Mel_Syd.append('KIIS1065-Syd')
station_edit_Mel_Syd.append('KIIS101.1-Mel')
station_edit_Mel_Syd.append('WSFM-Syd')
station_edit_Mel_Syd.append('GOLD104.3-Mel')
station_edit_Mel_Syd.append('ARNDAB-Syd')
station_edit_Mel_Syd.append('ARNDAB-Mel')

#SEN
station_edit_Mel_Syd.append('SEN-Mel')
station_edit_Mel_Syd.append('2CH-Syd')
station_edit_Mel_Syd.append('SENDAB-Syd')
station_edit_Mel_Syd.append('SENDAB-Mel')


#NINE
station_edit_Mel_Syd.append('2GB-Syd')
station_edit_Mel_Syd.append('3AW-Mel')


station_edit_Mel_Syd.append('2KY-Syd')
station_edit_Mel_Syd.append('NineDAB-Syd')
station_edit_Mel_Syd.append('NineDAB-Mel')


# Nova
station_edit_Mel_Syd.append('Nova969-Syd')
station_edit_Mel_Syd.append('Nova100-Mel')
station_edit_Mel_Syd.append("SmoothFM95.3-Syd")
station_edit_Mel_Syd.append("SmoothFM91.5-Mel") 
station_edit_Mel_Syd.append("NovaDAB-Syd")
station_edit_Mel_Syd.append("NovaDAB-Mel")


#RadioSport

station_edit_Mel_Syd.append('927-Mel')
station_edit_Mel_Syd.append("RadioSportDAB-Mel")


#SCA
station_edit_Mel_Syd.append('MMM-Syd')
station_edit_Mel_Syd.append('MMM-Mel')
station_edit_Mel_Syd.append('2DayFM-Syd')
station_edit_Mel_Syd.append('FOXFM-Mel')
station_edit_Mel_Syd.append('SCADAB-Syd')
station_edit_Mel_Syd.append('SCADAB-Mel')

#TAB
station_edit_Mel_Syd.append('2KY-Syd')
station_edit_Mel_Syd.append('TABDAB-Syd')



station_edit_National = []
# 2SM
station_edit_National.append('2SMStreaming-National')
station_edit_National.append('2SMPodcast-National')
#6IX
station_edit_National.append('6IXStreaming-National')
station_edit_National.append('6IXPodcast-National')
#ACE
station_edit_National.append('ACEStreaming-National')
station_edit_National.append('ACEPodcast-National')
#ARN
station_edit_National.append('ARNStreaming-National')
station_edit_National.append('ARNPodcast-National')
#NineRadio
station_edit_National.append('NineStreaming-Nat')
station_edit_National.append('NinePodcast-Nat')
#SCA
station_edit_National.append('SCAStreaming-National')
station_edit_National.append('SCAPodcast-National')
#RadioSport
station_edit_National.append('RadioSportStreaming-National')
station_edit_National.append('RadioSportPodcast-National') 
#SEN
station_edit_National.append('SENStreaming-National')
station_edit_National.append('SENPodcast-National')
#TAB
station_edit_National.append('TABStreaming-National')
station_edit_National.append('TABPodcast-National')
#NOVA
station_edit_National.append('NovaStreaming-National')
station_edit_National.append('NovaPodcast-National')

list_st_2SM = []
list_st_6IX = []
list_st_TAB = []
list_st_ARN = []
list_st_ACE = []
list_st_Nova = []
list_st_SCA = []
list_st_NineRadio = []
list_st_RadioSport = []
list_st_SEN = []

@app.route('/edit', methods=['GET', 'POST'])
def edit():

 

 network_current.append(current_user.network)
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
 if current_user.network == 'RadioSport':
    form_1 = DropdownForm_RadioSport()
 if current_user.network == '6IX':
    form_1 = DropdownForm_6IX()
 
 contact = thisdict.get(current_user.email)
 if len(dashboard_var_list) == 0:
  dashboard_var_list.append('2022M05')


 def return_template(station):
     if station in station_edit_Bri:
           return  render_template("edit_Bri.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
     if station in station_edit_Ade:
           return  render_template("edit_Ade.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
     if station in station_edit_Per:
           return  render_template("edit_Per.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
     if station in station_edit_National:
           return  render_template("edit_Metro.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
     if station in station_edit_Mel_Syd:
           return  render_template("edit.html", form=form, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network) 

 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )
 network = current_user.network
 
 if len(contacts) >= 2:
  
  
   contacts.clear()
   
  
   
   


 if current_user.network == 'SEN':
        network_SEN.append('2CH-Syd')
        network_SEN.append('SEN-Mel')
        network_SEN.append('SENDAB-Syd')
        network_SEN.append('SENDAB-Mel')
        
        network_SEN.append('SENStreaming-National')
        network_SEN.append('SENPodcast-National')
        
        
 elif current_user.network == '2SM':
        network_2SM.append("2SM-Syd")
        network_2SM.append("2SMDAB-Syd")
        network_2SM.append("2SMStreaming-National")
        network_2SM.append("2SMPodcast-National")

 elif current_user.network == 'ACE':
        network_ACE.append("3MP-Mel")
        network_ACE.append("2UE-Syd")
        network_ACE.append("Magic1278-Mel")
        network_ACE.append("4BH-Bri")
        network_ACE.append("ACEDAB-Syd")
        network_ACE.append("ACEDAB-Mel")
        network_ACE.append("ACEDAB-Bri")
        network_ACE.append("ACEStreaming-National")
        network_ACE.append("ACEPodcast-National")

 elif current_user.network == 'ARN':
        network_ARN.append('KIIS1065-Syd')
        network_ARN.append('KIIS101.1-Mel')
        network_ARN.append('New97.3-Bri')
        network_ARN.append('MIX102.3-Ade')
        network_ARN.append('96FM-Per')
        network_ARN.append("WSFM-Syd")
        network_ARN.append("GOLD104.3-Mel")
        network_ARN.append("4KQ-Bri")
        network_ARN.append("Cruise-Ade")
        network_ARN.append("ARNDAB-Syd")
        network_ARN.append("ARNDAB-Mel")
        network_ARN.append("ARNDAB-Bri")
        network_ARN.append("ARNDAB-Ade")
        network_ARN.append("ARNDAB-Per")
        network_ARN.append("ARNStreaming-National")
        network_ARN.append("ARNPodcast-National")

 elif current_user.network == 'NineRadio':
        network_NineRadio.append("2GB-Syd")
        network_NineRadio.append("3AW-Mel")
        network_NineRadio.append("4BC-Bri")
        network_NineRadio.append("6PR-Per")
        #network_NineRadio.append("2UE-Syd")
        #network_NineRadio.append("Magic1278-Mel")
        #network_NineRadio.append("4BH-Bri")
        network_NineRadio.append("NineDAB-Syd")
        network_NineRadio.append("NineDAB-Mel")
        
        network_NineRadio.append("NineDAB-Bri")
        network_NineRadio.append("NineDAB-Per")
        network_NineRadio.append("NineStreaming-Nat")
        network_NineRadio.append("NinePodcast-Nat")

 elif current_user.network == 'Nova':
        network_Nova.append("Nova969-Syd")
        network_Nova.append("Nova100-Mel")
        network_Nova.append("Nova1069-Bri")  
        network_Nova.append("Nova919-Ade")
        network_Nova.append("Nova937-Per")
        network_Nova.append("SmoothFM95.3-Syd")
        network_Nova.append("SmoothFM91.5-Mel") 
        network_Nova.append("5aa-Ade")
        network_Nova.append("NovaDAB-Syd")
        network_Nova.append("NovaDAB-Mel")
        network_Nova.append("NovaDAB-Ade")
        network_Nova.append("NovaDAB-Bri")
        network_Nova.append("NovaDAB-Per")
        network_Nova.append("NovaStreaming-National")
        network_Nova.append("NovaPodcast-National")


 elif current_user.network == 'RadioSport':
        network_RadioSport.append("927-Mel")
        network_RadioSport.append("RadioSportDAB-Mel")
        
        network_RadioSport.append("RadioSportStreaming-National")
        network_RadioSport.append("RadioSportPodcast-National")

 elif current_user.network == 'SCA':
        network_SCA.append("MMM-Syd")
        network_SCA.append("MMM-Mel")
        network_SCA.append("MMM-Bri")  
        network_SCA.append("MMM-Ade")
        network_SCA.append("92.9-Per")
        network_SCA.append("2DayFM-Syd")
        network_SCA.append("FOXFM-Mel") 
        network_SCA.append("b105-Bri")
        network_SCA.append("Hit107-Ade")
        network_SCA.append("MIX94.5-Per")
        network_SCA.append("SCADAB-Syd")
        network_SCA.append("SCADAB-Mel")
        network_SCA.append("SCADAB-Bri")
        network_SCA.append("SCADAB-Ade")
        network_SCA.append("SCADAB-Per")
        network_SCA.append("SCAStreaming-National")
        network_SCA.append("SCAPodcast-National")
 elif current_user.network == 'TAB':
        network_TAB.append('2KY-Syd')
        network_TAB.append('4TAB-Bri')
        network_TAB.append('TABDAB-Syd')
        network_TAB.append('TABDAB-Bri')
        network_TAB.append('TABStreaming-National')
        network_TAB.append('TABPodcast-National')
 elif current_user.network == '6IX':
        network_6IX.append('6IX-Per')
        network_6IX.append('6IXDAB-Per')
        network_6IX.append('6IXStreaming-National')
        network_6IX.append('6IXPodcast-National')
 

   
 

 
    




 network_stations = network_dict.get(current_user.network)
 if request.method == 'POST':
         network_final.clear()
         station= '{}'.format(form_1.type4.data)
        
        
         list_st.append(station)

         if current_user.network=='2SM':
           list_st_2SM.append(station)
         elif current_user.network == '6IX':
           list_st_6IX.append(station)
         elif current_user.network == 'TAB':
           list_st_TAB.append(station)
         elif current_user.network == 'ACE':
           list_st_ACE.append(station)
         elif current_user.network == 'Nova':
           list_st_Nova.append(station)
         elif current_user.network == 'NineRadio':
           list_st_NineRadio.append(station)
         elif current_user.network == 'SEN':
           list_st_SEN.append(station)
         elif current_user.network == 'ARN':
           list_st_ARN.append(station)
         elif current_user.network == 'RadioSport':
           list_st_RadioSport.append(station)
         elif current_user.network == 'SCA':
           list_st_SCA.append(station)
         
       
         month = dashboard_var_list[-1]
         
         # Removing null values and 0 to avoid errors of invalid db name if user makes an error in credential selection
         null = ""
         invalid_db_name = ""
         
         
         
         
        
         
         
         
         if invalid_db_name in list_st:
          list_st.remove(invalid_db_name)
         
         var_list.append(month)
         if invalid_db_name in var_list:
          var_list.remove(invalid_db_name)
          
          
        


         station_table_edit2.append(station)
         if invalid_db_name in station_table_edit2:
          station_table_edit2.remove(invalid_db_name)

        
         
        
      
         
      
        
        
        
         
         
         if current_user.network == '2SM':
           station = list_st_2SM[-1]
           if station == "":
             station = list_st_2SM[-2]

         if current_user.network == '6IX':
           station = list_st_6IX[-1]
           if station == "":
             station = list_st_6IX[-2]

         if current_user.network == 'SEN':
           station = list_st_SEN[-1]
           if station == "":
             station = list_st_SEN[-2]

         if current_user.network == 'ACE':
           station = list_st_ACE[-1]
           if station == "": 
             station = list_st_ACE[-2]
        
         if current_user.network == 'ARN':
           station = list_st_ARN[-1]
           if station == "":
             station = list_st_ARN[-2]
          
         if current_user.network == 'NineRadio':
           station = list_st_NineRadio[-1]
           if station == "":
             station = list_st_NineRadio[-2]
          
         if current_user.network == 'Nova':
           station = list_st_Nova[-1]
           if station == "":
             station = list_st_Nova[-2]
        
         if current_user.network == 'SCA':
           station = list_st_SCA[-1]
           if station == "":
             station = list_st_SCA[-2]
         
         if current_user.network == 'RadioSport':
           station = list_st_RadioSport[-1]
           if station == "":
             station = list_st_RadioSport[-2]
        
         if current_user.network == 'TAB':
           station = list_st_TAB[-1]
           if station == "":
             station = list_st_TAB[-2]
 

         # Remove any '' (null) values from lists    
         if current_user.network == '2SM':
          for i in list_st_2SM:
           if i == '':
             list_st_2SM.remove(i)

         if current_user.network == '6IX':
          for i in list_st_6IX:
           if i == '':
             list_st_6IX.remove(i)

         if current_user.network == 'ACE':
          for i in list_st_ACE:
           if i == '':
             list_st_ACE.remove(i)

         if current_user.network == 'TAB':
          for i in list_st_TAB:
           if i == '':
             list_st_TAB.remove(i)

         if current_user.network == 'NineRadio':
          for i in list_st_NineRadio:
           if i == '':
             list_st_NineRadio.remove(i)
         
         if current_user.network == 'RadioSport':
          for i in list_st_RadioSport:
           if i == '':
             list_st_RadioSport.remove(i)

         if current_user.network == 'ARN':
          for i in list_st_ARN:
           if i == '':
             list_st_ARN.remove(i)

         if current_user.network == 'Nova':
          for i in list_st_Nova:
           if i == '':
             list_st_Nova.remove(i)


         if current_user.network == 'SCA':
          for i in list_st_SCA:
           if i == '':
             list_st_SCA.remove(i)









        

         if var_list:
           month = var_list[-1]
    
        # if list_st:
          # station = list_st[-1]
         
         form_1.type4.default = station
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

         else:
          conn = sqlite3.connect(name)
    
         
          c = conn.cursor()
          listOfTables = c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='Edit_table'; """).fetchall()



         if form.fillzeroes.data:
          
          
           if station in station_edit_National:
            form.MetroTotal.data = Decimal(0)
           else:
            form.SydT1.data = Decimal(0)
            form.SydT2.data = Decimal(0)
            form.SydDirect.data = Decimal(0)
            form.MelT1.data = Decimal(0)
            form.MelT2.data = Decimal(0)
            form.MelDirect.data = Decimal(0)

            user_SydT1 = form.SydT1.data
            user_SydT2 = form.SydT2.data
            user_SydDirect = form.SydDirect.data
            user_MelT1 = form.MelT1.data
            user_MelT2 = form.MelT2.data
            user_MelDirect = form.MelDirect.data
           if station in station_edit_Mel_Syd:
            form.BriTotal.data = Decimal(0)
            form.AdeTotal.data = Decimal(0)
            form.PerTotal.data = Decimal(0)

            user_BriTotal = form.BriTotal.data
            user_AdeTotal = form.AdeTotal.data
            user_PerTotal = form.PerTotal.data
           if station in station_edit_Ade:
            form.BriTotal.data = Decimal(0)
            form.AdeT1.data = Decimal(0)
            form.AdeT2.data = Decimal(0)
            form.AdeDirect.data = Decimal(0)
            form.PerTotal.data = Decimal(0)

            user_BriTotal = form.BriTotal.data
            user_AdeT1 = form.AdeT1.data
            user_AdeT2 = form.AdeT2.data
            user_AdeDirect = form.AdeDirect.data
            user_PerTotal = form.PerTotal.data


           if station in station_edit_Bri:
            form.BriT1.data = Decimal(0)
            form.BriT2.data = Decimal(0)
            form.BriDirect.data = Decimal(0)
            form.AdeTotal.data = Decimal(0)
            form.PerTotal.data = Decimal(0)

            user_BriT1 = form.BriT1.data
            user_BriT2 = form.BriT2.data
            user_BriDirect = form.BriDirect.data

           if station in station_edit_Per:
             form.BriTotal.data = Decimal(0)
             form.AdeTotal.data = Decimal(0)
             form.PerT1.data = Decimal(0)
             form.PerT2.data = Decimal(0)
             form.PerDirect.data = Decimal(0)

             user_BriTotal = form.BriTotal.data
             user_AdeTotal = form.AdeTotal.data
             user_PerT1 = form.PerT1.data
             user_PerT2 = form.PerT2.data
             user_PerDirect = form.PerDirect.data
         
           
          

           


           
           
         else:
           if listOfTables != []:
            if station not in station_edit_National:
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


           
            
            if station in station_edit_Ade:

             c.execute("SELECT BriTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_BriTotal = form.BriTotal.data
             BriTotal = c.fetchone()[0]
             form.BriTotal.data = Decimal(BriTotal)

             c.execute("SELECT AdeT1 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_AdeT1 = form.AdeT1.data
             AdeT1 = c.fetchone()[0]
             form.AdeT1.data = Decimal(AdeT1)

             c.execute("SELECT AdeT2 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_AdeT2 = form.AdeT2.data
             AdeT2 = c.fetchone()[0]
             form.AdeT2.data = Decimal(AdeT2)

             c.execute("SELECT AdeDirect FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_AdeDirect = form.AdeDirect.data
             AdeDirect = c.fetchone()[0]
             form.AdeDirect.data = Decimal(AdeDirect)

             c.execute("SELECT PerTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_PerTotal = form.PerTotal.data
             PerTotal = c.fetchone()[0]
             form.PerTotal.data = Decimal(PerTotal)

           
           
            if station in station_edit_Bri:

             c.execute("SELECT BriT1 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_BriT1 = form.BriT1.data
             BriT1 = c.fetchone()[0]
             form.BriT1.data = Decimal(BriT1)

             c.execute("SELECT BriT2 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_BriT2 = form.BriT2.data
             BriT2 = c.fetchone()[0]
             form.BriT2.data = Decimal(BriT2)

             c.execute("SELECT BriDirect FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_BriDirect = form.BriDirect.data
             BriDirect = c.fetchone()[0]
             form.BriDirect.data = Decimal(BriDirect)

             c.execute("SELECT AdeTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_AdeTotal = form.AdeTotal.data
             AdeTotal = c.fetchone()[0]
             form.AdeTotal.data = Decimal(AdeTotal)

             c.execute("SELECT PerTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_PerTotal = form.PerTotal.data
             PerTotal = c.fetchone()[0]
             form.PerTotal.data = Decimal(PerTotal)

          
           
          

            if station in station_edit_Per:
            
             c.execute("SELECT BriTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_BriTotal = form.BriTotal.data
             BriTotal = c.fetchone()[0]
             form.BriTotal.data = Decimal(BriTotal)
           
             c.execute("SELECT AdeTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_AdeTotal = form.AdeTotal.data
             AdeTotal = c.fetchone()[0]
             form.AdeTotal.data = Decimal(AdeTotal)

             c.execute("SELECT PerT1 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_PerT1 = form.PerT1.data
             PerT1 = c.fetchone()[0]
             form.PerT1.data = Decimal(PerT1)

             c.execute("SELECT PerT2 FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_PerT2 = form.PerT2.data
             PerT2 = c.fetchone()[0]
             form.PerT2.data = Decimal(PerT2)

             c.execute("SELECT PerDirect FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_PerDirect = form.PerDirect.data
             PerDirect = c.fetchone()[0]
             form.PerDirect.data = Decimal(PerDirect)

         
           
            if station in station_edit_National:

             c.execute("SELECT MetroTotal FROM Edit_table ORDER BY ID DESC LIMIT 1;")
             user_MetroTotal = form.MetroTotal.data
             MetroTotal = c.fetchone()[0]
             form.MetroTotal.data = Decimal(MetroTotal)

           

            if station in station_edit_Mel_Syd:
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
         
       
            
          
          

         

         


        
          
            
     
          
        
         if form.submitprofits.data:
         
           if listOfTables != []:
            if station not in station_edit_National:

             SydT1_data = user_SydT1
             SydT2_data = user_SydT2
             SydDirect_data = user_SydDirect
             MelT1_data = user_MelT1
             MelT2_data = user_MelT2
             MelDirect_data = user_MelDirect

            if station in station_edit_Mel_Syd:
             BriTotal_data = user_BriTotal
             AdeTotal_data = user_AdeTotal
             PerTotal_data = user_PerTotal

            if station in station_edit_Ade:
              BriTotal_data = user_BriTotal
              AdeT1_data = user_AdeT1
              AdeT2_data = user_AdeT2
              AdeDirect_data = user_AdeDirect
              PerTotal_data = user_PerTotal

            if station in station_edit_Bri:
              BriT1_data = user_BriT1
              BriT2_data = user_BriT2
              BriDirect_data = user_BriDirect
            
            if station in station_edit_Per:
              PerT1_data = user_PerT1
              PerT2_data = user_PerT2
              PerDirect_data = user_PerDirect
            

            if station in station_edit_National:
              MetroTotal_data = user_MetroTotal
            
           if station not in station_table:
             station_table.append(station)
           if invalid_db_name in station_table:
             station_table.remove(invalid_db_name)
         
           if null in station_table:
             station_table.remove(null)
           if null in station_table_edit2:
             station_table_edit2.remove(null)

           del var_list[-1]

           

        
           
           



           with sqlite3.connect(name) as conn: 
           
            item = station_table_edit2[-1]
            if listOfTables != []:
             if station in station_edit_Bri:
              d = conn.cursor()
              d.execute("CREATE TABLE IF NOT EXISTS Edit_table (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriT1 NUMERIC(8), BriT2 NUMERIC(8), BriDirect NUMERIC(8), AdeTotal NUMERIC(8), PerTotal NUMERIC(8));")
              d.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriT1, BriT2, BriDirect, AdeTotal, PerTotal) values (?,?,?,?,?,?,?,?,?,?,?)",(str(user_SydT1),str(user_SydT2),str(user_SydDirect), str(user_MelT1), str(user_MelT2), str(user_MelDirect), str(user_BriT1), str(user_BriT2),str(user_BriDirect), str(user_AdeTotal), str(user_PerTotal), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Bri.html", form=form, message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)

             elif station in station_edit_Ade:
              e = conn.cursor()
              e.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriTotal NUMERIC(8), AdeT1 NUMERIC(8),  AdeT2 NUMERIC(8),  AdeDirect NUMERIC(8),  PerTotal NUMERIC(8));")
              e.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeT1, AdeT2, AdeDirect, PerTotal) values (?,?,?,?,?,?,?,?,?,?,?)",(str(user_SydT1),str(user_SydT2),str(user_SydDirect), str(user_MelT1), str(user_MelT2), str(user_MelDirect), str(user_BriTotal), str(user_AdeT1), str(user_AdeT2), str(user_AdeDirect), str(user_PerTotal), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Ade.html", form=form, message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
         
            

             elif station in station_edit_Per:
              f = conn.cursor()
              f.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriTotal NUMERIC(8), AdeTotal NUMERIC(8), PerT1 NUMERIC(8), PerT2 NUMERIC(8), PerDirect NUMERIC(8));")
              f.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeTotal, PerT1, PerT2, PerDirect) values (?,?,?,?,?,?,?,?,?,?,?)",(str(user_SydT1),str(user_SydT2),str(user_SydDirect), str(user_MelT1), str(user_MelT2), str(user_MelDirect), str(user_BriTotal), str(user_AdeTotal), str(user_PerT1), str(user_PerT2),  str(user_PerDirect), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Per.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
            
            
             elif station in station_edit_National:
              g = conn.cursor()
              g.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, MetroTotal NUMERIC(8));")
              g.execute("INSERT into Edit_table (MetroTotal) values (?)",(str(user_MetroTotal), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Metro.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
            
            
             elif station in station_edit_Mel_Syd:
              h = conn.cursor()
              h.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8),BriTotal NUMERIC(8), AdeTotal NUMERIC(8), PerTotal NUMERIC(8));")
              h.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeTotal, PerTotal) values (?,?,?,?,?,?,?,?,?)",(str(user_SydT1),str(user_SydT2),str(user_SydDirect), str(user_MelT1), str(user_MelT2), str(user_MelDirect), str(user_BriTotal), str(user_AdeTotal), str(user_PerTotal), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)

            else:
             if station in station_edit_Bri:
              d = conn.cursor()
              d.execute("CREATE TABLE IF NOT EXISTS Edit_table (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriT1 NUMERIC(8), BriT2 NUMERIC(8), BriDirect NUMERIC(8), AdeTotal NUMERIC(8), PerTotal NUMERIC(8));")
              d.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriT1, BriT2, BriDirect, AdeTotal, PerTotal) values (?,?,?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriT1.data), str(form.BriT2.data), str(form.BriDirect.data),str(form.AdeTotal.data), str(form.PerTotal.data), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Bri.html", form=form, message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)

             elif station in station_edit_Ade:
              e = conn.cursor()
              e.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriTotal NUMERIC(8), AdeT1 NUMERIC(8),  AdeT2 NUMERIC(8),  AdeDirect NUMERIC(8),  PerTotal NUMERIC(8));")
              e.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeT1, AdeT2, AdeDirect, PerTotal) values (?,?,?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriTotal.data), str(form.AdeT1.data), str(form.AdeT2.data), str(form.AdeDirect.data), str(form.PerTotal.data), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Ade.html", form=form, message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
         
            

             elif station in station_edit_Per:
              f = conn.cursor()
              f.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8), BriTotal NUMERIC(8), AdeTotal NUMERIC(8), PerT1 NUMERIC(8), PerT2 NUMERIC(8), PerDirect NUMERIC(8));")
              f.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeTotal, PerT1, PerT2, PerDirect) values (?,?,?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriTotal.data), str(form.AdeTotal.data), str(form.PerT1.data), str(form.PerT2.data),  str(form.PerDirect.data), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Per.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
            
            
             elif station in station_edit_National:
              g = conn.cursor()
              g.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, MetroTotal NUMERIC(8));")
              g.execute("INSERT into Edit_table (MetroTotal) values (?)",(str(form.MetroTotal.data), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit_Metro.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
            
            
             elif station in station_edit_Mel_Syd:
              h = conn.cursor()
              h.execute("CREATE TABLE IF NOT EXISTS Edit_table  (id INT AUTO_INCREMENT PRIMARY KEY, SydT1 NUMERIC(8), SydT2 NUMERIC(8), SydDirect NUMERIC(8), MelT1 NUMERIC(8), MelT2 NUMERIC(8), MelDirect NUMERIC(8),BriTotal NUMERIC(8), AdeTotal NUMERIC(8), PerTotal NUMERIC(8));")
              h.execute("INSERT into Edit_table (SydT1, SydT2, SydDirect, MelT1, MelT2, MelDirect, BriTotal, AdeTotal, PerTotal) values (?,?,?,?,?,?,?,?,?)",(str(form.SydT1.data),str(form.SydT2.data),str(form.SydDirect.data), str(form.MelT1.data), str(form.MelT2.data), str(form.MelDirect.data), str(form.BriTotal.data), str(form.AdeTotal.data),  str(form.PerTotal.data), ))
              message_2 = ("Successfully Updated")
              return  render_template("edit.html", form=form,  message_2 = message_2, form_1 = form_1, month=month, contact = contact, station=station, user_image=pic, network = current_user.network)
        
 else:
   return render_template("edit_default.html", form=form, form_1 = form_1,  user_image=pic, contact=contact,  network = current_user.network)
 
 if station_table_edit2: 

  
  
  

  return return_template(station)
  
 
 else:
  return render_template("edit_default.html", form=form, form_1 = form_1,  user_image=pic, contact = contact,  network = current_user.network)



    

     
# function to output tables for review and submit html pages


           
   
    
network_st = [] 



import numpy as np

@app.route('/review', methods=['GET', 'POST'])
def review():
 contact = thisdict.get(current_user.email)
 df = None
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
 if current_user.network == 'RadioSport':
  form_1 = DropdownForm_RadioSport()
 if current_user.network == '6IX':
  form_1 = DropdownForm_6IX()

 

 network = current_user.network
 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )

 def filter_stations():
   network_stations = network_dict.get(current_user.network)
   
   concurrent_station_2SM = []
   concurrent_station_SEN = []
   concurrent_station_TAB = []
   concurrent_station_6IX = []
   concurrent_station_RadioSport = []
   concurrent_station_NineRadio = []
   concurrent_station_Nova = []
   concurrent_station_SCA = []
   concurrent_station_ACE = []
   concurrent_station_ARN = []

   for e in network_stations:
    if current_user.network=='2SM':
     if e in list_st_2SM:
      concurrent_station_2SM.append(e)
      
    elif current_user.network == '6IX':
     if e in list_st_6IX:
      concurrent_station_6IX.append(e)
      
    elif current_user.network == 'TAB':
     if e in list_st_TAB:
      concurrent_station_TAB.append(e)
     
    elif current_user.network == 'ACE':
     if e in list_st_ACE:
      concurrent_station_ACE.append(e)
      
    elif current_user.network == 'Nova':
     if e in list_st_Nova:
      concurrent_station_Nova.append(e)
    
    elif current_user.network == 'NineRadio':
     if e in list_st_NineRadio:
      concurrent_station_NineRadio.append(e)
      
    elif current_user.network == 'SEN':
     if e in list_st_SEN:
      concurrent_station_SEN.append(e)
      
    elif current_user.network == 'ARN':
     if e in list_st_ARN:
      concurrent_station_ARN.append(e)
     
    elif current_user.network == 'RadioSport':
     if e in list_st_RadioSport:
      concurrent_station_RadioSport.append(e)
      
    elif current_user.network == 'SCA':
     if e in list_st_SCA:
      concurrent_station_SCA.append(e)
      
   if current_user.network == '2SM':
     return concurrent_station_2SM
   if current_user.network == '6IX':
     return concurrent_station_6IX
   if current_user.network == 'TAB':
     return concurrent_station_TAB
   if current_user.network == 'ACE':
     return concurrent_station_ACE
   if current_user.network == 'SCA':
     return concurrent_station_SCA
   if current_user.network == 'Nova':
     return concurrent_station_Nova
   if current_user.network == 'NineRadio':
     return concurrent_station_NineRadio
   if current_user.network == 'RadioSport':
     return concurrent_station_RadioSport
   if current_user.network == 'ARN':
     return concurrent_station_ARN
   if current_user.network == 'SEN':
     return concurrent_station_SEN
 
    
   
   





 def incomplete_station_def():
    
    network_stations = network_dict.get(current_user.network)
   
    incomplete_station_data_list_2SM = []
    incomplete_station_data_list_6IX = []
    incomplete_station_data_list_TAB = []
    incomplete_station_data_list_SEN = []
    incomplete_station_data_list_ARN = []
    incomplete_station_data_list_Nova = []
    incomplete_station_data_list_SCA = []
    incomplete_station_data_list_NineRadio = []
    incomplete_station_data_list_RadioSport = []
    incomplete_station_data_list_ACE = []

    incomplete_2SM = []
    incomplete_TAB = []
    incomplete_SEN = []
    incomplete_NineRadio = []
    incomplete_Nova = []
    incomplete_RadioSport = []
    incomplete_6IX = []
    incomplete_ARN = []
    incomplete_ACE = []
    incomplete_SCA = []

    for e in network_stations:  
     if current_user.network=='2SM':
      if e not in list_st_2SM:
       incomplete_station_data_list_2SM.append(e)
      for element in incomplete_station_data_list_2SM:
       if element not in incomplete_2SM:
        if element in network_stations:
         incomplete_2SM.append(element)
       else:
        del element
      
     elif current_user.network == '6IX':
      if e not in list_st_6IX:
        incomplete_station_data_list_6IX.append(e)
      for element in incomplete_station_data_list_6IX:
       if element not in incomplete_6IX:
        if element in network_stations:
         incomplete_6IX.append(element)
       else:
        del element

      
     elif current_user.network == 'TAB':
      if e not in list_st_TAB:
       incomplete_station_data_list_TAB.append(e)
      for element in incomplete_station_data_list_TAB:
       if element not in incomplete_TAB:
        if element in network_stations:
         incomplete_TAB.append(element)
       else:
        del element
     
     elif current_user.network == 'ACE':
      if e not in list_st_ACE:
       incomplete_station_data_list_ACE.append(e)
      for element in incomplete_station_data_list_ACE:
       if element not in incomplete_ACE:
        if element in network_stations:
         incomplete_ACE.append(element)
       else:
        del element
      
     elif current_user.network == 'Nova':
      if e not in list_st_Nova:
       incomplete_station_data_list_Nova.append(e)
      for element in incomplete_station_data_list_Nova:
       if element not in incomplete_Nova:
        if element in network_stations:
         incomplete_Nova.append(element)
       else:
        del element
    
     elif current_user.network == 'NineRadio':
      if e not in list_st_NineRadio:
       incomplete_station_data_list_NineRadio.append(e)
      for element in incomplete_station_data_list_NineRadio:
       if element not in incomplete_NineRadio:
        if element in network_stations:
         incomplete_NineRadio.append(element)
       else:
        del element
      
     elif current_user.network == 'SEN':
      if e not in list_st_SEN:
       incomplete_station_data_list_SEN.append(e)
      for element in incomplete_station_data_list_SEN:
       if element not in incomplete_SEN:
        if element in network_stations:
         incomplete_SEN.append(element)
       else:
        del element
      
     elif current_user.network == 'ARN':
      if e not in list_st_ARN:
       incomplete_station_data_list_ARN.append(e)
      for element in incomplete_station_data_list_ARN:
       if element not in incomplete_ARN:
        if element in network_stations:
         incomplete_ARN.append(element)
       else:
        del element
     
     elif current_user.network == 'RadioSport':
      if e not in list_st_RadioSport:
      
       incomplete_station_data_list_RadioSport.append(e)
      for element in incomplete_station_data_list_RadioSport:
       if element not in incomplete_RadioSport:
        if element in network_stations:
         incomplete_RadioSport.append(element)
       else:
        del element
      
     elif current_user.network == 'SCA':
      if e not in list_st_SCA:
       incomplete_station_data_list_SCA.append(e)
      for element in incomplete_station_data_list_SCA:
       if element not in incomplete_SCA:
        if element in network_stations:
         incomplete_SCA.append(element)
       else:
        del element
    
   

   
    
      
    if current_user.network == '2SM':
     df_incomplete = pd.DataFrame(incomplete_2SM, columns=['Unedited Stations'])
     return df_incomplete, incomplete_2SM
    if current_user.network == '6IX':
     df_incomplete = pd.DataFrame(incomplete_6IX, columns=['Unedited Stations'])
     return df_incomplete, incomplete_6IX
    if current_user.network == 'TAB':
     df_incomplete = pd.DataFrame(incomplete_TAB, columns=['Unedited Stations'])
     return df_incomplete, incomplete_TAB
    if current_user.network == 'ACE':
     df_incomplete = pd.DataFrame(incomplete_ACE, columns=['Unedited Stations'])
     return df_incomplete, incomplete_ACE
    if current_user.network == 'SCA':
     df_incomplete = pd.DataFrame(incomplete_SCA, columns=['Unedited Stations'])
     return df_incomplete, incomplete_SCA
    if current_user.network == 'Nova':
     df_incomplete = pd.DataFrame(incomplete_Nova, columns=['Unedited Stations'])
     return df_incomplete, incomplete_Nova
    if current_user.network == 'NineRadio':
     df_incomplete = pd.DataFrame(incomplete_NineRadio, columns=['Unedited Stations'])
     return df_incomplete, incomplete_NineRadio
    if current_user.network == 'RadioSport':
     df_incomplete = pd.DataFrame(incomplete_RadioSport, columns=['Unedited Stations'])
     return df_incomplete, incomplete_RadioSport
    if current_user.network == 'ARN':
     df_incomplete = pd.DataFrame(incomplete_ARN, columns=['Unedited Stations'])
     return df_incomplete, incomplete_ARN
    if current_user.network == 'SEN':
     df_incomplete = pd.DataFrame(incomplete_SEN, columns=['Unedited Stations'])
     return df_incomplete, incomplete_SEN

    

 
 network_stations = network_dict.get(current_user.network)     
 if len(var_list) >= 1:
     month = var_list[-1]
     if month == "":
         month = var_list[-2]

       
    


 
    
    
     index = 0
     stations = []
     df = pd.DataFrame([])
     review_station_list = []
     concurrent_station = filter_stations()
    
     
     for x in range(len(concurrent_station)):
      
      if len(concurrent_station) >= index:
       
       station = concurrent_station[index]
       
       month = dashboard_var_list[-1]

       if station not in network_stations :
        del station 
        index = index + 1

       if station in review_station_list:
         del station
         index = index + 1



       else:
        review_station_list.append(station)
        
       
        name = month + "-" + network + "-" + contact + "-" + station + ".db"
    
        connection = sqlite3.connect(name)
        cursor = connection.cursor() 
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Edit_table' ''')
        if cursor.fetchone()[0]==1 :
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         l = cursor.fetchall() 
        
        
         if station in station_edit_Bri:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDT1', 'QLDT2', 'QLDDirect', 'SATotal', 'WATotal'])
         if station in station_edit_Ade:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDTotal', 'SAT1', 'SAT2', 'SADirect', 'WATotal'])
         if station in station_edit_Per:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDTotal', 'SATotal', 'WAT1', 'WAT2', 'WADirect'])
         if station in station_edit_Mel_Syd:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDTotal', 'SATotal', 'WATotal'])
         if station in station_edit_National:
          row_df = pd.DataFrame(data = l, columns = ['', 'National-Total'])

         pd.options.display.float_format = "{:,.2f}".format
 
         data = pd.DataFrame(row_df)
        
         data = row_df.iloc[: , 1:]
         
         df = df.append(data)
         
         
         
        
        
         stations.append(station)
              
      
         df = df.fillna(0)
         df.index = stations
      
    
         index = index + 1
       
        else:
         index = index + 1

     
     df['NSWTotal'] = df[['NSWT1', 'NSWT2', 'NSWDirect']].sum(axis=1)
     df['VICTotal'] = df[['VICT1', 'VICT2', 'VICDirect']].sum(axis=1)
    
     if 'QLDT1' in df.columns:
          df['QLD'] = df[['QLDT1', 'QLDT2', 'QLDDirect']].sum(axis=1)
          if 'QLDTotal' in df.columns:
           df['QLDTotal'] = df[['QLD', 'QLDTotal']].sum(axis=1)
          else:
           df['QLDTotal'] = df['QLD']
          df.drop('QLDT1', inplace=True, axis=1)
          df.drop('QLDT2', inplace=True, axis=1)
          df.drop('QLDDirect', inplace=True, axis=1)
          df.drop('QLD', inplace=True, axis=1)
         
          
     if 'SAT1' in df.columns:
       
          df['SA'] = df[['SAT1', 'SAT2', 'SADirect']].sum(axis=1)
          if 'SATotal' in df.columns:
           df['SATotal'] = df[['SA', 'SATotal']].sum(axis=1)
          else:
           df['SATotal'] = df['SA']
          df.drop('SAT1', inplace=True, axis=1)
          df.drop('SAT2', inplace=True, axis=1)
          df.drop('SADirect', inplace=True, axis=1)
          df.drop('SA', inplace=True, axis=1)
         
          
          
         
     if 'WAT1' in df.columns:
       
          df['WA'] = df[['WAT1', 'WAT2', 'WADirect']].sum(axis=1)
          if 'WATotal' in df.columns:
           df['WATotal'] = df[['WA', 'WATotal']].sum(axis=1)
          else:
           df['WATotal'] = df['WA']
          df.drop('WAT1', inplace=True, axis=1)
          df.drop('WAT2', inplace=True, axis=1)
          df.drop('WADirect', inplace=True, axis=1)
          df.drop('WA', inplace=True, axis=1)
          
          


     
        
         
          
     
     df.drop('NSWT1', inplace=True, axis=1)
     df.drop('NSWT2', inplace=True, axis=1)
     df.drop('NSWDirect', inplace=True, axis=1)
     df.drop('VICT1', inplace=True, axis=1)
     df.drop('VICT2', inplace=True, axis=1)
     df.drop('VICDirect', inplace=True, axis=1)
  
    
     df.loc[:, 'Total Stn'] = df.sum(axis=1)
     df.loc['Total Mkt', :] = df.sum(axis=0)

     if 'National-Total' not in df.columns:
      df = df[['NSWTotal', 'VICTotal', 'QLDTotal', 'SATotal', 'WATotal', 'Total Stn']]

     else:
      df = df[['NSWTotal', 'VICTotal', 'QLDTotal', 'SATotal', 'WATotal', 'National-Total', 'Total Stn']]
      

     df_incomplete, incomplete = incomplete_station_def()  
     if df is not None:
      if len(incomplete) != 0:
       
       header = ("Incomplete Station Data")
       message = ("The following stations have not been entered, please edit the following stations: ")
       network_stations = network_dict.get(current_user.network)
      

       stations_entered = ((len(network_stations)) - (len(incomplete)))
       progress_width = ((stations_entered/len(network_stations)) * 100)
       progress_width = round(progress_width,1)
      
       return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, contact=contact, message = message,  header = header, tables=[df.to_html(classes='data', header="true")], tables_incomplete = [df_incomplete.to_html(classes='incomplete')], progress_width = progress_width)
      else:
       header_complete = ("All Station Data Entered")
       message_complete = ("Please select Submit from the Select Action box to send your details to Milton Data")
       del df_incomplete
       return render_template("review_complete.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, contact=contact,  message_complete = message_complete, header_complete = header_complete, tables=[df.to_html(classes='data', header="true")])
     else:
      return render_template("review.html", form=form, form_1 = form_1, user_image=pic, network=current_user.network, contact=contact, tables_incomplete = [df_incomplete.to_html(classes='incomplete')])

     
  
     
    

 

 return render_template("review.html", form=form, form_1 = form_1, user_image=pic, contact=contact, network=current_user.network)



  



import csv
from io import StringIO

@app.route('/submit', methods=['GET', 'POST'])
def submit():
 contact = thisdict.get(current_user.email)
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
 if current_user.network == 'RadioSport':
    form_1 = DropdownForm_RadioSport()
 if current_user.network == '6IX':
    form_1 = DropdownForm_6IX()

 def filter_stations():
   network_stations = network_dict.get(current_user.network)
   
   concurrent_station_2SM = []
   concurrent_station_SEN = []
   concurrent_station_TAB = []
   concurrent_station_6IX = []
   concurrent_station_RadioSport = []
   concurrent_station_NineRadio = []
   concurrent_station_Nova = []
   concurrent_station_SCA = []
   concurrent_station_ACE = []
   concurrent_station_ARN = []

   for e in network_stations:
    if current_user.network=='2SM':
     if e in list_st_2SM:
      concurrent_station_2SM.append(e)
      
    elif current_user.network == '6IX':
     if e in list_st_6IX:
      concurrent_station_6IX.append(e)
      
    elif current_user.network == 'TAB':
     if e in list_st_TAB:
      concurrent_station_TAB.append(e)
     
    elif current_user.network == 'ACE':
     if e in list_st_ACE:
      concurrent_station_ACE.append(e)
      
    elif current_user.network == 'Nova':
     if e in list_st_Nova:
      concurrent_station_Nova.append(e)
    
    elif current_user.network == 'NineRadio':
     if e in list_st_NineRadio:
      concurrent_station_NineRadio.append(e)
      
    elif current_user.network == 'SEN':
     if e in list_st_SEN:
      concurrent_station_SEN.append(e)
      
    elif current_user.network == 'ARN':
     if e in list_st_ARN:
      concurrent_station_ARN.append(e)
     
    elif current_user.network == 'RadioSport':
     if e in list_st_RadioSport:
      concurrent_station_RadioSport.append(e)
      
    elif current_user.network == 'SCA':
     if e in list_st_SCA:
      concurrent_station_SCA.append(e)
      
   if current_user.network == '2SM':
     return concurrent_station_2SM
   if current_user.network == '6IX':
     return concurrent_station_6IX
   if current_user.network == 'TAB':
     return concurrent_station_TAB
   if current_user.network == 'ACE':
     return concurrent_station_ACE
   if current_user.network == 'SCA':
     return concurrent_station_SCA
   if current_user.network == 'Nova':
     return concurrent_station_Nova
   if current_user.network == 'NineRadio':
     return concurrent_station_NineRadio
   if current_user.network == 'RadioSport':
     return concurrent_station_RadioSport
   if current_user.network == 'ARN':
     return concurrent_station_ARN
   if current_user.network == 'SEN':
     return concurrent_station_SEN
 

 form_2 = RegisterForm()
 network_stations = network_dict.get(current_user.network) 
 if var_list:
   month = var_list[-1]
   if month == "":
    month = var_list[-2]
 
 if list_st:
     station = list_st[-1]
     if station == "":
         station = list_st[-2]
     if station not in network_stations:
       list_st.remove(station)

     name = month + "-" + network + "-" + contact + "-" + station + ".db"
   
     
     def submit_table(station_function, month_function):

        today = dt.datetime.now()
        first = today.replace(day=1)
        lastMonth = first - dt.timedelta(days=1)
        Month = lastMonth.strftime("%b %Y")
        Datetime = today.strftime("%Y-%m-%d-%H-%M")
        
        columns_list = df.columns.values.tolist()
        
       
        df_new_1 = pd.DataFrame(columns_list)
       
        df_new_1['DateTime'] = Datetime
        df_new_1['Network'] = network
        df_new_1['UserId'] = current_user.email
        df_new_1['UserName'] = contact
        df_new_1['Month'] = Month 
        df_new_1['MonthCode'] = month_function
        df_new_1['Station'] = station_function
        
        df_post = df.transpose()
        #df_post = df_post[:-1]
        
        column_1 = df_post[station_function]
        
      
      
        
       
        df_new_1['MktKey'] = df_new_1.iloc[:,7] + "_" + df_new_1.iloc[:,0]
        df_new_1['Station2'] = station_function
        revenue = column_1
        revenue.reset_index(drop=True, inplace=True)
       
        revenue = revenue.to_frame()
       
       
        df_new_1 = df_new_1.merge(revenue, left_index=True, right_index=True)
       
        
        # RENAMING COLUMNS IN DATAFRAME
      
        df_new_1.rename(columns={ df_new_1.columns[10]: 'Revenue' }, inplace = True)
        df_new_1.rename(columns={ df_new_1.columns[0]: 'Market_station'}, inplace = True)       
        df_new_1['Market'] = df_new_1['Market_station'].astype(str).str[:3]
        df_new_1['Level'] = df_new_1['Market_station'].astype(str).str[3:] 

        # Replace 'roTotal' to 'Total'
       
        df_new_1['Market'] = df_new_1['Market'].replace({'Nat' : 'National'}, regex=True)
        df_new_1['Market'] = df_new_1['Market'].replace({'WAT' : 'WA'}, regex=True)
        df_new_1['Market'] = df_new_1['Market'].replace({'WAD' : 'WA'}, regex=True)

        df_new_1['Market'] = df_new_1['Market'].replace({'SAD' : 'SA'}, regex=True)
        df_new_1['Market'] = df_new_1['Market'].replace({'SAT' : 'SA'}, regex=True)

        df_new_1['Level'] = df_new_1['Level'].replace({'ional-Total' : 'Total'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'1' : 'T1'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'2' : 'T2'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'irect' : 'Direct'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'otal' : 'Total'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'TTotal' : 'Total'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'DDirect' : 'Direct'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'TT1' : 'T1'}, regex=True)
        df_new_1['Level'] = df_new_1['Level'].replace({'TT2' : 'T2'}, regex=True)


        df_new_1 = df_new_1.iloc[: , 1:]
       
        df_new_1 = df_new_1[['DateTime', 'Network', 'UserId', 'UserName', 'Month', 'MonthCode', 'Station', 'MktKey', 'Station2', 'Market', 'Level', 'Revenue' ]]

        boolean_Station_Syd = df_new_1['Station2'].str.contains('Syd').any()
        boolean_Station_Mel = df_new_1['Station2'].str.contains('Mel').any()
        boolean_Station_Bri = df_new_1['Station2'].str.contains('Bri').any()
        boolean_Station_Ade = df_new_1['Station2'].str.contains('Ade').any()
        boolean_Station_Per = df_new_1['Station2'].str.contains('Per').any()
        boolean_Station_National = df_new_1['Station2'].str.contains('National').any()

        boolean_QLD = df_new_1['Market'].str.contains('QLD').any()
        boolean_WA = df_new_1['Market'].str.contains('WA').any()
        boolean_SA = df_new_1['Market'].str.contains('SA').any()
        print(df_new_1)

        def drop_QLD_row():

          indexNames_QLD_T1 = df_new_1[(df_new_1['Market'] == 'QLD') & (df_new_1['Level'] == 'T1')].index
          indexNames_QLD_T2 = df_new_1[(df_new_1['Market'] == 'QLD') & (df_new_1['Level'] == 'T2')].index
          indexNames_QLD_Direct = df_new_1[(df_new_1['Market'] == 'QLD') & (df_new_1['Level'] == 'Direct')].index

          df_new_1.drop(indexNames_QLD_T1 , inplace=True)
          df_new_1.drop(indexNames_QLD_T2 , inplace=True)
          df_new_1.drop(indexNames_QLD_Direct , inplace=True)

        def drop_WA_row():
          indexNames_WA_T1 = df_new_1[(df_new_1['Market'] == 'WA') & (df_new_1['Level'] == 'T1')].index
          indexNames_WA_T2 = df_new_1[(df_new_1['Market'] == 'WA') & (df_new_1['Level'] == 'T2')].index
          indexNames_WA_Direct = df_new_1[(df_new_1['Market'] == 'WA') & (df_new_1['Level'] == 'Direct')].index

          df_new_1.drop(indexNames_WA_T1 , inplace=True)
          df_new_1.drop(indexNames_WA_T2 , inplace=True)
          df_new_1.drop(indexNames_WA_Direct , inplace=True)

        def drop_SA_row():
           indexNames_SA_T1 = df_new_1[(df_new_1['Market'] == 'SA') & (df_new_1['Level'] == 'T1')].index
           indexNames_SA_T2 = df_new_1[(df_new_1['Market'] == 'SA') & (df_new_1['Level'] == 'T2')].index
           indexNames_SA_Direct = df_new_1[(df_new_1['Market'] == 'SA') & (df_new_1['Level'] == 'Direct')].index

           df_new_1.drop(indexNames_SA_T1 , inplace=True)
           df_new_1.drop(indexNames_SA_T2 , inplace=True)
           df_new_1.drop(indexNames_SA_Direct , inplace=True)
           
        def drop_Total_rows():
           indexNames_SA_Total = df_new_1[(df_new_1['Market'] == 'SA') & (df_new_1['Level'] == 'Total')].index
           indexNames_WA_Total = df_new_1[(df_new_1['Market'] == 'WA') & (df_new_1['Level'] == 'Total')].index
           indexNames_QLD_Total = df_new_1[(df_new_1['Market'] == 'QLD') & (df_new_1['Level'] == 'Total')].index

           df_new_1.drop(indexNames_SA_Total , inplace=True)
           df_new_1.drop(indexNames_WA_Total , inplace=True)
           df_new_1.drop(indexNames_QLD_Total, inplace=True)

        def drop_Syd_Mel_row():
           indexNames_Syd_T1 = df_new_1[(df_new_1['Market'] == 'NSW') & (df_new_1['Level'] == 'T1')].index
           indexNames_Syd_T2 = df_new_1[(df_new_1['Market'] == 'NSW') & (df_new_1['Level'] == 'T2')].index
           indexNames_Syd_Direct = df_new_1[(df_new_1['Market'] == 'NSW') & (df_new_1['Level'] == 'Direct')].index
           indexNames_Mel_T1 = df_new_1[(df_new_1['Market'] == 'VIC') & (df_new_1['Level'] == 'T1')].index
           indexNames_Mel_T2 = df_new_1[(df_new_1['Market'] == 'VIC') & (df_new_1['Level'] == 'T2')].index
           indexNames_Mel_Direct = df_new_1[(df_new_1['Market'] == 'VIC') & (df_new_1['Level'] == 'Direct')].index


           df_new_1.drop(indexNames_Syd_T1 , inplace=True)
           df_new_1.drop(indexNames_Syd_T2 , inplace=True)
           df_new_1.drop(indexNames_Syd_Direct , inplace=True)
           df_new_1.drop(indexNames_Mel_T1 , inplace=True)
           df_new_1.drop(indexNames_Mel_T2 , inplace=True)
           df_new_1.drop(indexNames_Mel_Direct , inplace=True)
        

        if boolean_Station_Syd == True or boolean_Station_Mel == True:

           indexNames_National_Total = df_new_1[(df_new_1['Market'] == 'National') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_National_Total, inplace=True)

           if boolean_QLD == True:
            drop_QLD_row()

        
           if boolean_WA == True:
            drop_WA_row()
          
         
           if boolean_SA == True:
             drop_SA_row()
            
        if boolean_Station_Bri == True:
           indexNames_National_Total = df_new_1[(df_new_1['Market'] == 'National') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_National_Total, inplace=True)

           indexNames_Bri_Total = df_new_1[(df_new_1['Market'] == 'QLD') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_Bri_Total , inplace=True)

           if boolean_WA == True:
            
            drop_WA_row()
          
         
           if boolean_SA == True:
             drop_SA_row()

        if boolean_Station_Ade == True:

           indexNames_National_Total = df_new_1[(df_new_1['Market'] == 'National') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_National_Total, inplace=True)

           indexNames_Ade_Total = df_new_1[(df_new_1['Market'] == 'SA') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_Ade_Total , inplace=True)

           if boolean_QLD == True:
            drop_QLD_row()

           if boolean_WA == True:
            drop_WA_row()
        
        if boolean_Station_Per == True:

           indexNames_National_Total = df_new_1[(df_new_1['Market'] == 'National') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_National_Total, inplace=True)

           indexNames_Per_Total = df_new_1[(df_new_1['Market'] == 'WA') & (df_new_1['Level'] == 'Total')].index
           df_new_1.drop(indexNames_Per_Total , inplace=True)

           if boolean_QLD == True:
            drop_QLD_row()
          
           if boolean_SA == True:
            drop_SA_row()
        
        if boolean_Station_National == True:
          
           drop_Syd_Mel_row()
           drop_QLD_row()
           drop_WA_row()
           drop_SA_row()
           drop_Total_rows()

        
        return df_new_1

     def table_to_s3(table_milton, df):
      
        x = dt.datetime.now()
        contact_new = contact.replace(" ","-")
        base_path = os.getcwd()
        name_submit =  network + "-" +  month + "-" +  x.strftime('%Y') + "-" + x.strftime('%m')  + "-" +  x.strftime('%d') + "-" + x.strftime('%H') + "-" + x.strftime('%M') + "-" + contact_new 
        csv_file = name_submit + ".csv"      
        sql_file = name_submit + ".sqlite"
        bucket = 'miltondata-radio1'
        s3 = boto3.client('s3', aws_access_key_id = 'access_key', aws_secret_access_key = 'secret_key')
        csv_path = os.path.join(base_path + "\\" + 'this_folder' + '\\' + name_submit + ".csv")
        table_milton.to_csv(csv_path)
        s3.upload_file(csv_path,'miltondata-radio1', name_submit + ".csv")
        sql_path = os.path.join(base_path + "\\" + 'this_folder' + '\\' + name_submit + ".sqlite")
        
        conn = sqlite3.connect(sql_path)
        table_milton.to_sql('/this_folder/' + sql_file, conn, if_exists='append', index = False)
        s3.upload_file(sql_path, 'miltondata-radio1', name_submit + ".sqlite")
          

     index = 0
     stations = []
     df = pd.DataFrame([])
     table_milton = pd.DataFrame([])
     review_station_list = []
     network_stations = network_dict.get(current_user.network)
     concurrent_station = filter_stations()


     for x in range(len(concurrent_station)):
      if len(concurrent_station) >= index:
       month = var_list[-1]
       station = concurrent_station[index]

       if station not in network_stations:
        del station 
        index = index + 1
       

       
       if station in review_station_list:
         del station
         index = index + 1
       

      

       else:
        review_station_list.append(station)
        name = month + "-" + network + "-" + contact + "-" + station + ".db"
    
        connection = sqlite3.connect(name)
        cursor = connection.cursor() 
        cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='Edit_table' ''')
        if cursor.fetchone()[0]==1 :
         cursor.execute("SELECT * FROM Edit_table ORDER BY ID DESC LIMIT 1;") 
         l = cursor.fetchall() 
        
        
         if station in station_edit_Bri:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDT1', 'QLDT2', 'QLDDirect', 'SATotal', 'WATotal'])
         if station in station_edit_Ade:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDTotal', 'SAT1', 'SAT2', 'SADirect', 'WATotal'])
         if station in station_edit_Per:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDTotal', 'SATotal', 'WAT1', 'WAT2', 'WADirect'])
         if station in station_edit_Mel_Syd:
          row_df = pd.DataFrame(data = l, columns = ['', 'NSWT1', 'NSWT2', 'NSWDirect', 'VICT1', 'VICT2', 'VICDirect', 'QLDTotal', 'SATotal', 'WATotal'])
         if station in station_edit_National:
          row_df = pd.DataFrame(data = l, columns = ['', 'National-Total'])

         pd.options.display.float_format = "{:,.2f}".format
         data = pd.DataFrame(row_df)
         data = row_df.iloc[: , 1:]
         df = df.append(data)
      
         stations.append(station)
              
     
         df = df.fillna(0)
         df.index = stations
    
         index = index + 1
         table = submit_table(station, month)
      
         table_milton = table_milton.append(table)
        
        else:
         index = index + 1
   
          
     
     table_milton = table_milton.reset_index(drop=True)
     df.loc['Total Mkt', :] = df.sum(axis=0)
     df.loc[:, 'Total Stn'] = df.sum(axis=1)
     

    

        
         
       
        
       
     if request.method == 'POST':
        submit_to_aws = []
        for i in network_stations:  
         if i not in station_table:
          submit_to_aws.append(i)
    
        incomplete = []
        for element in submit_to_aws:
         if element not in incomplete:
           incomplete.append(element)
      

      

       
        if len(incomplete) == 0:
         
         table_to_s3(table_milton, table)
       
         message_2 = 'Data Submitted to Milton Data'
         logoff_message = 'Please select Logoff from the Select Action box to finish your session. Thank you.'
         base_path = os.getcwd()
         s3 = boto3.client('s3', aws_access_key_id = 'access', aws_secret_access_key = 'secret')
         x = dt.datetime.now()
         logged_off = "Logged Off" + "-" + current_user.network + "-" + x.strftime('%Y') + "-" + x.strftime('%m')  + "-" +  x.strftime('%d') + "-" + x.strftime('%H') + "-" + x.strftime('%M') + "-" + current_user.email + ".txt"
         logged_off_path = os.path.join(base_path + "\\" + 'this_folder' + '\\' + logged_off)
         open(logged_off_path, 'a').close()
         s3.upload_file(logged_off_path, 'miltondata-radio1', logged_off )
         return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network = current_user.network,  logoff_message = logoff_message, message_2 = message_2, contact = contact, month = month, tables=[df.to_html(classes='data', header="true")])
        else:
         
         message_3 = 'Cannot submit table to Milton Data until all stations have been successfully edited' 
         message_4 = 'Return to the Review Page to identify the stations that require value updates'
         return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network = current_user.network,  message_3 = message_3, message_4 = message_4, contact = contact, month = month, tables=[df.to_html(classes='data', header="true")])
     
      
                 
            
    
        
       
       
      
       
       
      
     else:
        return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network = current_user.network,  contact = contact, month = month, tables=[df.to_html(classes='data', header="true")])
 else:
     return render_template("submit.html", form=form, form_1 = form_1, user_image=pic, network = current_user.network, contact = contact) 
   
import plotly.express as px
from pathlib import Path
import json
import plotly
import plotly.graph_objects as go

@app.route("/reporting",  methods=['GET', 'POST'])
def reporting():
 pic = os.path.join(app.config['UPLOAD_FOLDER'], 'cra-logo.jpg' )

 if current_user.network == 'SEN':
     form = DropdownForm_SEN()
 if current_user.network == 'TAB':
     form = DropdownForm_TAB()
 if current_user.network == 'SCA':
     form = DropdownForm_SCA()
 if current_user.network == 'NineRadio':
     form = DropdownForm_NineRadio()
 if current_user.network == 'Nova':
     form = DropdownForm_Nova()
 if current_user.network == 'ARN':
      form = DropdownForm_ARN()
 if current_user.network == 'ACE':
       form = DropdownForm_ACE()
 if current_user.network == '2SM':
        form = DropdownForm_2SM()
 if current_user.network == 'RadioSport':
        form = DropdownForm_RadioSport()

 
 if request.method == 'POST':
    dataset = pd.read_csv("CRA-2021M11DB-Revenue-000-final-anubhav-dummy-20210117-final.csv", index_col=False)
   
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
     dataset = dataset[['RevenueGroup', 'MktCurrent', 'MktPrevious', 'MktGrowth%', 'StnCurrent', 'StnPrevious', 'StnGrowth%', 'MktShrCurrent', 'MktShrPrevious', 'RankCurrent', '#StnsCurrent', 'RankPrevious', 'NumStnsPrevious']]
     dataset = dataset.reset_index(drop=True)
     dataset = dataset.round(2)
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Ade_Other'],'Adelaide')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Bri_Other'],'Brisbane')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Grand_Total'],'Grand-Total')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Interstate_Total'],'Interstate-Total')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Mel_T1'],'Melbourne T1 Agency')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Mel_T2'],'Melbourne T2 Agency')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Mel_Direct'],'Melbourne Direct')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Mel_Total'],'Total Melbourne')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Mel_TotalAgency'],'Total Melbourne Agency')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Syd_T1'],'Sydney T1 Agency')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Syd_T2'],'Sydney T2 Agency')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Syd_Direct'],'Sydney Direct')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Syd_Total'],'Total Sydney')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Syd_TotalAgency'],'Total Sydney Agency')
     dataset['RevenueGroup'] = dataset['RevenueGroup'].replace(['Per_Other'],'Perth')
     dataset = dataset.fillna(0)
    
     
     
     return dataset

    

  
    
    
    
  
   
    
    dataset = dataset[dataset.CalendarMonth == form.calendar_month.data]
    dataset = dataset[dataset.Period == form.period_select.data]
  
    dataset = dataset[dataset.Station == str(form.type4.data) + " " + "(DUMMY)"]
    dataset = table_format(dataset)

    market_growth = dataset[['MktGrowth%', 'RevenueGroup']]

    station_reporting_list = []
    station = form.type4.data
    station_reporting_list.append(station)
    
    station = station_reporting_list[-1]
   
    station_growth = dataset[['StnGrowth%', 'RevenueGroup']]

    mktshare_current = dataset[['MktShrCurrent', 'RevenueGroup']]
   
    mktshare_previous = dataset[['MktShrPrevious', 'RevenueGroup']]

    rank_previous = dataset[['RankPrevious', 'RevenueGroup']]
    rank_current = dataset[['RankCurrent', 'RevenueGroup']]


    if station in station_edit_Per:
     market_growth['RevenueGroup'] = ['Sydney T1 Agency', 'Sydney T2 Agency', 'Total Sydney Agency', 'Sydney Direct', 'Total Sydney', 'Melbourne T1 Agency', 'Melbourne T2 Agency', 'Total Melbourne Agency', 'Melbourne Direct', 'Melbourne Total',
     'Brisbane', 'Adelaide', 'Per_T1', 'Per_T2', 'Per_Total', 'Per_Direct', 'Per_TotalAgency', 'Interstate-Total', 'Grand-Total']

     station_growth['RevenueGroup'] = ['Sydney T1 Agency', 'Sydney T2 Agency', 'Total Sydney Agency', 'Sydney Direct', 'Total Sydney', 'Melbourne T1 Agency', 'Melbourne T2 Agency', 'Total Melbourne Agency', 'Melbourne Direct', 'Melbourne Total',
     'Brisbane', 'Adelaide', 'Per_T1', 'Per_T2', 'Per_Total', 'Per_Direct', 'Per_TotalAgency', 'Interstate-Total', 'Grand-Total']

     mktshare_current['RevenueGroup'] = ['Sydney T1 Agency', 'Sydney T2 Agency', 'Total Sydney Agency', 'Sydney Direct', 'Total Sydney', 'Melbourne T1 Agency', 'Melbourne T2 Agency', 'Total Melbourne Agency', 'Melbourne Direct', 'Melbourne Total',
     'Brisbane', 'Adelaide', 'Per_T1', 'Per_T2', 'Per_Total', 'Per_Direct', 'Per_TotalAgency', 'Interstate-Total', 'Grand-Total']

     mktshare_previous['RevenueGroup'] = ['Sydney T1 Agency', 'Sydney T2 Agency', 'Total Sydney Agency', 'Sydney Direct', 'Total Sydney', 'Melbourne T1 Agency', 'Melbourne T2 Agency', 'Total Melbourne Agency', 'Melbourne Direct', 'Melbourne Total',
     'Brisbane', 'Adelaide', 'Per_T1', 'Per_T2', 'Per_Total', 'Per_Direct', 'Per_TotalAgency', 'Interstate-Total', 'Grand-Total']

     rank_previous['RevenueGroup'] = ['Sydney T1 Agency', 'Sydney T2 Agency', 'Total Sydney Agency', 'Sydney Direct', 'Total Sydney', 'Melbourne T1 Agency', 'Melbourne T2 Agency', 'Total Melbourne Agency', 'Melbourne Direct', 'Melbourne Total',
     'Brisbane', 'Adelaide', 'Per_T1', 'Per_T2', 'Per_Total', 'Per_Direct', 'Per_TotalAgency', 'Interstate-Total', 'Grand-Total']

     rank_current['RevenueGroup'] = ['Sydney T1 Agency', 'Sydney T2 Agency', 'Total Sydney Agency', 'Sydney Direct', 'Total Sydney', 'Melbourne T1 Agency', 'Melbourne T2 Agency', 'Total Melbourne Agency', 'Melbourne Direct', 'Melbourne Total',
     'Brisbane', 'Adelaide', 'Per_T1', 'Per_T2', 'Per_Total', 'Per_Direct', 'Per_TotalAgency', 'Interstate-Total', 'Grand-Total']





    
   
   

   
   
    


# Plot
    fig = px.bar(market_growth, x= market_growth['RevenueGroup'], y= market_growth['MktGrowth%'], title= 'Market Growth %', color = market_growth['RevenueGroup'], text_auto=True)
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


    fig_2 = px.bar(station_growth, x= station_growth['RevenueGroup'], y= station_growth['StnGrowth%'], title= 'Station Growth %', color = station_growth['RevenueGroup'], text_auto=True)

    graphJSON_2 = json.dumps(fig_2, cls=plotly.utils.PlotlyJSONEncoder)

    fig_3 = go.Figure(data=[
      go.Bar(name = 'Mkt Share Previous', x = mktshare_previous['RevenueGroup'], y = mktshare_previous['MktShrPrevious']),
      go.Bar(name='Mkt Share Current', x = mktshare_current['RevenueGroup'], y = mktshare_current['MktShrCurrent'])
      
    ])

    fig_3.update_layout(barmode= 'group', title= 'Market Share Previous vs Market Share Current')

    graphJSON_3 = json.dumps(fig_3, cls=plotly.utils.PlotlyJSONEncoder)

    fig_4 = go.Figure(data=[
      go.Bar(name = 'Rank Previous', x = rank_previous['RevenueGroup'], y = rank_previous['RankPrevious']),
      go.Bar(name='Rank Current', x = rank_current['RevenueGroup'], y = rank_current['RankCurrent'])
      
    ])

    fig_4.update_layout(barmode= 'group', title= 'Rank Previous vs Rank Current')

    graphJSON_4 = json.dumps(fig_4, cls=plotly.utils.PlotlyJSONEncoder)

    link_name = "static/reports/Report_" + str(form.calendar_month.data) + "_" + str(form.type4.data) + "_" + str(form.period_select.data) + ".xlsx"
    
    dataset.to_excel(link_name)


    link = link_name    
         
     
    return render_template("reporting.html", form=form, user_image=pic, network=current_user.network, period = form.period_select.data, month = form.calendar_month.data, station = form.type4.data, link = link, tables=[dataset.to_html(classes='data', header="true")], graphJSON = graphJSON, graphJSON_2 = graphJSON_2,  graphJSON_3 = graphJSON_3, graphJSON_4 = graphJSON_4) 

 

       
 return render_template("reporting.html", user_image=pic, network = current_user.network, form=form, period = form.period_select.data, month = form.calendar_month.data, station = form.type4.data) 

   

 
   
  










     
    
      
   
          
     







@app.before_first_request
def create_tables():
    db.create_all()


if __name__ == "__main__":
    serve(app, listen='*:80')