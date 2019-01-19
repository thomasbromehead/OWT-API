from models import Base, Contact, Skill, User
from flask import Flask, jsonify, request, url_for, abort, g
import sqlalchemy as sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool
import time
import json
from sqlalchemy.orm.exc import UnmappedInstanceError, NoResultFound

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///contacts.db', poolclass=SingletonThreadPool)

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@auth.verify_password
def verify_password(username_or_token, password):
    # Try to see if it's a token first
    user_id = User.verify_auth_token(username_or_token)
    if user_id:
        user = session.query(User).filter_by(id=user_id).one()
    else:
        user = session.query(User).filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/v1/token')
# @auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})


@app.route('/api/v1/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        print
        "missing arguments"
        abort(400)

    if session.query(User).filter_by(username=username).first() is not None:
        print
        "existing user"
        user = session.query(User).filter_by(username=username).first()
        return jsonify(existing_user = {'message': 'user already exists'}), 200

    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()
    return jsonify(successfully_created_user = {'username': user.username}), 201



@app.route('/api/v1/contacts', methods=['GET', 'POST'])
# @auth.login_required
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
        else:
            skills = None
        print("JSON: ", request.json)
        contact = Contact(first_name=first_name, last_name=last_name,
                          full_name=full_name, email=email,
                          mobile=mobile, skills = skills)
        print("Contact: ", contact)
        print("Skills: ", contact.skills)
        session.add(contact)
        session.commit()
        return jsonify(contact=contact.serialize), 201



@app.route('/api/v1/contacts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @auth.login_required
def get_contact(id):
        contact = session.query(Contact).filter_by(id=id).first()
        try:
            if request.method == "GET":
                return jsonify(contact.serialize)

            elif request.method == "PUT":
                first_name = request.json.get('first_name')
                last_name = request.json.get('last_name')
                full_name = request.json.get('first_name')
                email = request.json.get('email')
                address = request.json.get('address')
                mobile = request.json.get('mobile')
                skills = request.json.get('skills')
                if first_name:
                    contact.first_name = first_name
                if last_name:
                    contact.last_name = last_name
                if full_name:
                    contact.full_name = full_name
                if address:
                    contact.address = address
                if email:
                    contact.email = email
                if mobile:
                    contact.mobile = mobile
                if skills:
                    for name in skills:
                        contact.skills.append(session.query(Skill).filter_by(name=str(name.lower())).one())
                    session.commit()
                return (jsonify({"Message":"Contact updated successfully"}, contact.serialize), 200)

            elif request.method == "DELETE":
                session.delete(contact)
                session.commit()
                return "Contact deleted!", 200
        except AttributeError:
            print(UnmappedInstanceError)
            return "Couldn't find person with id {}".format(id), 404 # Bad Request
        # except UnmappedInstanceError():
        #     print("unmapped")
        #     return "Couldn't find person with id {}".format(id), 400 

        


@app.route('/api/v1/skills', methods=['GET', 'POST'])
# @auth.login_required
def get_or_make_skill():
    if request.method == "GET":
        skills = session.query(Skill).all()
        if len(skills) == 0:
            return "No skills added yet, how sad!"
        return jsonify(skills=[skill.serialize for skill in skills])

    elif request.method == "POST":
        if request.json.get('name'):
            name = request.json.get('name').lower().strip()
        if request.json.get('level'):
            level = request.json.get('level')
        skill = Skill(name=name, level=level)
        session.add(skill)
        session.commit()
        return jsonify(skill.serialize), 201


@app.route('/api/v1/skills/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# @auth.login_required
def get_skill(id):
    skill = session.query(Skill).filter_by(id=id).one()
    if skill:
        if request.method == "GET":
            return jsonify(skill=skill.serialize)

        elif request.method == "PUT":
            name = request.json.get("name")
            level = request.json.get("level")
            if name:
                skill.name = name.lower().strip()
            if level:
                skill.level = level.lower().strip()
            session.commit()
            return jsonify(skill=skill.serialize)

        elif request.method == "DELETE":
            session.delete(skill)
            session.commit()
            return "{} was deleted successfully!".format(skill.name.capitalize())
    return "No skill found with ID {}".format(id)


@app.route('/api/v1/skills/<string:name>')
def who_has_that_skill(name):
    skill = session.query(Skill).filter_by(name=name).first()
    contacts = skill.contacts
    return jsonify(contacts_with_these_skills=[contact.serialize for contact in contacts])

# Create a skill
# curl -i -H "Content-Type: application/json" -d '{"name":"jacript","level":5}' localhost:5000/api/v1/skills
# --------------------

# Create a contact
# curl -H "Content-type:application/json" --data '{"contact":{"first_name":"Henri", "last_name":"Larruat", "full_name":"Henri Matthieu Larruat", "email": "henri@gmail.fr"}}' localhost:5000/api/v1/contacts

# --------------------
# Modify the skill to correct spelling
# curl --request PUT -H "Content-type:application/json" --data '{"name":"javascript"}' localhost:5000/api/v1/skills/1

# --------------------
# Modify the contact by adding him some kills
# curl -H "Content-type:application/json" --data '{"skills": ["javascript"]}' localhost:5000/api/v1/contacts/1

# --------------------
# Get contacts who are skilled in JS
# curl localhost:5000/api/v1/skills/javascript




if __name__ == '__main__':
    app.debug = True
    app.env = "development"
    # app.config['SECRET_KEY'] = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    app.run(host='0.0.0.0', port=5000)
