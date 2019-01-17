from models import Base, Contact, Skill
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import time

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()


engine = create_engine('sqlite:///contacts.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/contacts', methods = ['GET', 'POST'])
def do_this():
    if request.method == "GET":
        contacts = session.query(Contact).all()
        return jsonify(contacts = [contact.serialize for contact in contacts])
    elif request.method == "POST":
        print("this is a post")
        if request.json.get('contact').get('first_name'):
            first_name = request.json.get('contact').get('first_name', '')
        if request.json.get('contact').get('last_name', ''):
            last_name = request.json.get('contact').get('last_name', '')
        else:
            last_name = None
        if request.json.get('contact').get('full_name'):
            full_name = request.json.get('contact').get('full_name', '')
            print("Full Name ", full_name)
        else:
            full_name = None
        if request.json.get('contact').get('address'):
            address = request.json.get('contact').get('address', '')
            print("Address :", address)
        else:
            address = None
        if request.json.get('contact').get('email'):
            email = request.json.get('contact').get('email', '')
            print("Email: ", email)
        else:
            email = None
        if request.json.get('contact').get('mobile'):
            mobile = request.json.get('contact').get('mobile')
            print("Mobile: ", mobile)
        else :
            mobile = None
        if request.json.get('contact').get('skills'):
            skills = request.json.get('contact').get('skills')
            print("Skills ", skills)
        else:
            skills = None
        print("JSON: ", request.json)
        contact = Contact(first_name = first_name, last_name = last_name,
                        full_name = full_name, email = email,
                        mobile = mobile)
        print("Contact: ", contact)
        session.add(contact)
        session.commit()
        return jsonify(contact = contact.serialize), 201

@app.route('/contacts/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
def do_that():
    return "e"

@app.route('/skills', methods = ['GET', 'POST'])
def do_this_too():
    return "hey"


if __name__ == '__main__':
    app.debug = True
    app.env = "development"
    #app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
