
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import random
import datetime

app = Flask(__name__)





#==============================================================#
#config database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#==============================================================#
# Create class and methods

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)


    def __init__(self,first_name,last_name,email,password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password



class Links(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ref = db.Column(db.String, unique=True)
    url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.String)


    def __init__(self,ref,url,user_id,created_at):
        self.ref = ref
        self.url = url
        self.user_id = user_id
        self.created_at = created_at



class VisitedLinks(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    url_ref = db.Column(db.String)
    ip_address = db.Column(db.String)
    device_used = db.Column(db.String)
    country = db.Column(db.String)
    town = db.Column(db.String)
    created_at = db.Column(db.String)


    def __init__(self,url_ref,ip_address,device_used,country,town,created_at):
        self.url_ref = url_ref
        self.ip_address = ip_address
        self.device_used = device_used
        self.country = country
        self.town = town
        self.created_at = created_at




class Ads(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ref = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ad_title = db.Column(db.String)
    ad_photo = db.Column(db.String)
    ad_link = db.Column(db.String)
    budget = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.String)


    def __init__(self,ref,user_id,ad_title,ad_photo,ad_link,budget,status,created_at):
        self.ref = ref
        self.user_id = user_id
        self.ad_title = ad_title
        self.ad_photo = ad_photo
        self.ad_link = ad_link
        self.budget = budget
        self.status = status
        self.created_at = created_at




class ViewedAds(db.Model):

    id = db.Column(db.Integer, primary_key= True)
    ad_ref = db.Column(db.String)
    ip_address = db.Column(db.String)
    country = db.Column(db.String)
    town = db.Column(db.String)
    created_at = db.Column(db.String)


    def __init__(self,ad_ref,ip_address,country,town,created_at):
        self.ad_ref = ad_ref
        self.ip_address = ip_address
        self.country = country
        self.town = town
        self.created_at = created_at





class Wallet(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    amount = db.Column(db.Integer)
    mpesa_code = db.Column(db.String)
    user_phone = db.Column(db.String)
    status = db.Column(db.String)
    created_at = db.Column(db.String)

    def __init__(self,user_id,top_up,mpesa_code,user_phone,status,created_at):
        self.user_id = user_id
        self.top_up = top_up
        self.mpesa_code = mpesa_code
        self.user_phone = user_phone
        self.status = status
        self.created_at = created_at




#==============================================================#
# from  app import db   ; db.create_all()   - to create database



#==============================================================#
#create api end points


@app.route('/')
def url_shortener():
    return '<h1>url shortener</h1>'




#============================= #
# create user

# login user

# change password

# ============================ #

# add link

# display link

# record visit 

# display link visits count

# deactivate link

# ========================== #

# add ad

# display ad

# record view

# display ad visits count

#========================== #

# top up account









#==============================================================#
#start code & debug settings


if __name__ == "__main__":
    
    app.run(debug=True)
    

