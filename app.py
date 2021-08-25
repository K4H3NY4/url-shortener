from flask import Flask, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)
from flask_sqlalchemy import SQLAlchemy

import datetime
import random
import sqlite3
import bcrypt


app = Flask(__name__)


#==============================================================#
#config database


app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'some_random_jwt_secret_key'

db = SQLAlchemy(app)
app.secret_key = 'random secret key'

jwt = JWTManager(app)


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


""""

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


 """
 #==============================================================#


# from  app import db   ; db.create_all()   - to create database



#==============================================================#
#create api end points


@app.route('/')
def url_shortener():
    return 'url shortener'



"""
====================================================================
create user
====================================================================
"""
@app.route('/register', methods=['POST'])
def add_user():
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    email = request.json['email']
    password = request.json['password']
    password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


    try:
        new_user = Users(first_name,last_name,email,password_hashed)
        db.session.add(new_user)
        db.session.commit()

        user_profile = Users.query.filter_by(email=email).first()
        access_token = create_access_token(identity={"id": user_profile.id})

        return {"access_token":access_token},201
    except:
        return 'Email already exists', 406
 

"""
====================================================================
user login
====================================================================
""" 
@app.route('/login', methods=['POST'])
def login():  
   
    try:
        email = request.json['email']
        password = request.json['password']
        user_profile = Users.query.filter_by(email=email).first()
        password_hash = bcrypt.checkpw(password.encode('utf-8'), user_profile.password)

        if(password_hash == True):
            
            access_token = create_access_token(identity={"id": user_profile.id})

            return {"access_token":access_token}, 200

        else:

            return 'Authentication failed', 400    
    except:
        return 'Something went wrong', 409

    
"""
====================================================================
Change password
====================================================================
"""
@app.route('/change-password', methods=['PUT'])
@jwt_required()
def edit_password():
    try:
        users = get_jwt_identity()
        user_id = users['id'] 
        user = Users.query.get(user_id)
        new_password = request.json['new_password']
        confirm_password = request.json['confirm_password']

        if(new_password == confirm_password):
            password_hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password = password_hashed
            db.session.commit()
            return 'Password Successfully Changed'
        else:
            return 'Error: Passwords do not match'
    except:
        return 'login to change password'



"""
====================================================================
Forgot Password
====================================================================
"""
@app.route('/forgot-password', methods=['PUT'])
def forgot_password():
    try:
        email = request.json['email']
        user_email = Users.query.filter_by(email=email).first()
        email=user_email.email
        e = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        random.shuffle(e)
        easy_password = "" 
        password_gen = easy_password.join(e)
        password = password_gen[:7]
        password_hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_email.password = password_hashed
        db.session.commit()  
 
            
        return  (password) , 200
        #return jsonify(email=user_email.email)

    except:
        return 'Email does not exist'



"""
====================================================================
add link
====================================================================
"""
@app.route('/add-link', methods=['POST'])
@jwt_required()
def add_link():
    user = get_jwt_identity()
    user_id = user['id']   

    url = request.json['url']

    ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    ref = ref_gen[:5]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date

    new_link = Links(ref,url,user_id,created_at)
    db.session.add(new_link)
    db.session.commit()

    return 'localhost/' + (ref), 200



"""
====================================================================
add link guest
====================================================================
"""

@app.route('/guest', methods=['POST'])
def add_link_guest():
    
    user_id = 0   

    url = request.json['url']

    ref_seed = ['a','b','c','e','d','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']
    random.shuffle(ref_seed)
    ref_seed_empty = "" 
    ref_gen = ref_seed_empty.join(ref_seed)
    ref = ref_gen[:5]

    x = datetime.datetime.now()
    current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
    current_date = str(current_time)
    created_at = current_date

    new_link = Links(ref,url,user_id,created_at)
    db.session.add(new_link)
    db.session.commit()

    return 'localhost/' + (ref), 200






"""
====================================================================
 Call link
===================================================================
"""
@app.route('/<ref>', methods=['GET'])
def get_link(ref):

    try:
        link = Links.query.filter_by(ref=ref).first()
        url_ref = link.ref
        url = link.url


        # record visit 
        def record_visit(url_ref):
    
            ip_address = '127.0.0.1'
            device_used = 'Chrome'
            country = 'Kenya'
            town = 'Nairobi'

            x = datetime.datetime.now()
            current_time = x.strftime("%d""-""%B""-""%Y"" ""%H"":""%M"":""%S")
            current_date = str(current_time)
            created_at = current_date

            try:
                new_visits = VisitedLinks(url_ref,ip_address,device_used,country,town,created_at)
                db.session.add(new_visits)
                db.session.commit()

                return "Link added", 200
            except:
                return "link error", 202

        record_visit(url_ref)
        return url

    except:
        return 'No such link', 404




"""
====================================================================
 display link visits count
====================================================================
"""
@app.route('/link-count', methods=['POST'])
@jwt_required()
def link_count():

    user = get_jwt_identity()

    user_id = int(user['id']) 
    url_ref = request.json['url_ref']

    conn = sqlite3.connect('database.db')

    conn_count = conn.cursor()
    conn_count.execute("SELECT COUNT(url_ref) from visited_links WHERE url_ref = '"+ url_ref +"'")
    record = conn_count.fetchall()

    conn_confirm_owner = conn.cursor()
    conn_confirm_owner.execute("SELECT COUNT(ref) from links WHERE ref = ? and user_id = ?;", (url_ref,user_id))
    record_confirm = conn_confirm_owner.fetchall()

    if (record_confirm[0][0] == 1):
        return {"visited_count":record[0][0]}, 200
    else:
        return {"error":"Authentication Failed"}, 401




"""
====================================================================
delete link
====================================================================
"""

@app.route('/<ref>', methods=['DELETE'])
@jwt_required()
def delete_link(ref):
    user = get_jwt_identity()

    user_id = int(user['id'])

    try:
        link = Links.query.filter_by(ref=ref).first()
        
        conn = sqlite3.connect('database.db')
        conn_confirm_owner = conn.cursor()
        conn_confirm_owner.execute("SELECT COUNT(ref) from links WHERE ref = ? and user_id = ?;", (ref,user_id))
        record_confirm = conn_confirm_owner.fetchall()

        if (record_confirm[0][0] == 1):
            db.session.delete(link)
            db.session.commit()
            
            return 'Link Deleted', 200
        else:
            return 'Authentication Failed', 401

    except:
        return 'No such link', 404




"""
====================================================================
display all links
====================================================================
"""
@app.route('/links', methods=['POST'])
@jwt_required()
def display_links():
    user = get_jwt_identity()
    user_id = int(user['id'])
    links = Links.query.filter_by(user_id=user_id).all()

    output =[]
    for link in links:
            link_data={}
            link_data['id']=link.id
            link_data['ref']=link.ref
            link_data['url']=link.url
            link_data['created_at']=link.created_at
            output.append(link_data)

    return jsonify({"links":output})




"""
====================================================================
display link visits details
====================================================================
"""
@app.route('/link/<ref>', methods=['POST'])
@jwt_required()
def get_link_details(ref):
    user = get_jwt_identity()
    user_id = user['id'] 

    try:
        visitedlinks = VisitedLinks.query.filter_by(url_ref=ref).all()

        conn = sqlite3.connect('database.db')
        conn_confirm_owner = conn.cursor()
        conn_confirm_owner.execute("SELECT COUNT(ref) from links WHERE ref = ? and user_id = ?;", (ref,user_id))
        record_confirm = conn_confirm_owner.fetchall()

        output =[]
        for visitedlink in visitedlinks:
            visitedlink_data={}
            visitedlink_data['url_ref']=visitedlink.url_ref
            visitedlink_data['ip_address']=visitedlink.ip_address
            visitedlink_data['device_used']=visitedlink.device_used
            visitedlink_data['country']=visitedlink.country
            visitedlink_data['town']=visitedlink.town
            visitedlink_data['created_at']=visitedlink.created_at
            output.append(visitedlink_data)

        if (record_confirm[0][0] == 1):
            return jsonify({"user_messages":output}) , 200
        else:
            return {"error":"Authentication Failed"}, 401

    except:
        return 'No such link', 404




"""

# ========================== #

# add ad

# display ad

# record view

# display ad visits count

#========================== #

# top up account

"""






#==============================================================#
#start code & debug settings


if __name__ == "__main__":
    
    app.run(debug=True)
    

