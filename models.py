from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, validates
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context
import random, string
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import re

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))


class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30))
    last_name = Column(String(80))
    full_name = Column(String(250))
    address = Column(String(250), nullable=True)
    email = Column(String(80))
    mobile = Column(String(80), nullable=True)
    skills = relationship("Skill",
                          secondary=Table("contact_skill", Base.metadata,
                                          Column("contact_id", Integer, ForeignKey("contact.id"), primary_key=True),
                                          Column("skill_id", Integer, ForeignKey("skill.id"), primary_key=True)
                                          ),
                          backref="contacts",
                          )

    @property
    def serialize(self):
        return {
            'id': self.id,
            'first-name': self.first_name,
            'last-name': self.last_name,
            'full-name': self.full_name,
            'address': self.address,
            'email': self.email,
            'mobile': self.mobile,
            'skills': self.skills
        }

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError("No email provided")
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')
        return email


class Skill(Base):
    __tablename__ = "skill"
    id = Column(Integer, primary_key=True)
    name = Column(String(80))
    level = Column(Integer)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'level': self.level
        }

    @validates('level')
    def validate_level(self, key, level):
        if level < 0 or level > 5:
            raise AssertionError("The level must be between 0 and 5")
        if not level:
            raise AssertionError("No level provided")
        return level


engine = create_engine('sqlite:///contacts.db')

Base.metadata.create_all(engine)
