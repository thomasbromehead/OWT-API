from models import Base, Contact, Skill
from flask import Flask, jsonify, request, url_for, abort, g
import sqlalchemy as sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import time
import json

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///contacts.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/api/v1/contacts', methods=['GET', 'POST'])
def get_make_contacts():
    if request.method == "GET":
        contacts = session.query(Contact).all()
        return jsonify(contacts=[contact.serialize for contact in contacts])
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
        else:
            mobile = None
        if request.json.get('contact').get('skills'):
            skills = request.json.get('contact').get('skills')
            print("Skills ", skills)
        else:
            skills = None
        print("JSON: ", request.json)
        contact = Contact(first_name=first_name, last_name=last_name,
                          full_name=full_name, email=email,
                          mobile=mobile)
        print("Contact: ", contact)
        print("Skills: ", contact.skills)
        session.add(contact)
        session.commit()
        return jsonify(contact=contact.serialize), 201


@app.route('/api/v1/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_contact(id):
    contact = session.query(Contact).filter_by(id=id).first()

    if request.method == "GET":
        if contact is not None:
            return jsonify(contact.serialize)
        return "No contact with id {} was found!".format(id)

    elif request.method == "PUT":
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        full_name = request.json.get('first_name')
        email = request.json.get('email')
        address = request.json.get('address')
        mobile = request.json.get('mobile')
        skills = request.json.get('skills')
        print('Email: ', email)
        print('Full_name: ', full_name)
        print('Skills: ', skills)
        if first_name:
            contact.first_name = first_name
        if last_name:
            contact.last_name = last_name
        if full_name:
            contact.full_name = full_name
        if address:
            contact.address = address
        if mobile:
            contact.mobile = mobile
        if skills:
            contact.skills = skills
        print('JSON: ', request.json)
        session.commit()
        return jsonify(contact=contact.serialize)

    elif request.method == "DELETE":
        session.delete(contact)
        session.commit()
        return "Contact deleted!"


@app.route('/api/v1/skills', methods=['GET', 'POST'])
def get_or_make_skill():
    if request.method == "GET":
        skills = session.query(Skill).all()
        if len(skills) == 0:
            return "No skills added yet, how sad!"
    return jsonify(skills=[skill.serialize for skill in skills])
    if request.method == "POST":
        if request.json.get('name'):
            name = request.json.get('name')
            print("Name:", name)
        if request.json.get('level'):
            level = request.json.get('level')
            print("Level ", level)
        skill = Skill(name=name, level=level)
        session.add(skill)
        session.commit()
        return jsonify(skill.serialize), 201


@app.route('/api/v1/skills/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_skill(id):
    skill = session.query(Skill).filter_by(id=id).one()
    if skill is not None:
        if request.method == "GET":
            print("Skill", skill)
            return jsonify(skill=skill.serialize)

        elif request.method == "PUT":
            name = request.json.get("name")
            level = request.json.get("level")
            if name:
                skill.name = name
            if level:
                skill.level = level
            session.commit()
            return jsonify(skill=skill.serialize)

        elif request.method == "DELETE":
            session.delete(skill)
            session.commit()
            return "{} was deleted successfully!".format(skill.name.capitalize())
    return "No skill found with ID {}".format(id)


# curl -i -H "Content-Type: application/json" -d '{"name":"javascript","level":5}' localhost:5000/api/v1/skills


if __name__ == '__main__':
    app.debug = True
    app.env = "development"
    # app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
