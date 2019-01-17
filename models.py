from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()



class Contact(Base):
    __tablename__ = "contact"
    id = Column(Integer, primary_key=True)
    firstname = Column(String(30))
    lastname = Column(String(80))
    address = Column(String(250), nullable = True)
    email = Column(String(80), nullable = True)
    mobile = Column(String(80), nullable = True)
    skills = relationship("Skill",
        secondary = Table("contact_skill", Base.metadata,
                        Column("contact_id", Integer, ForeignKey("contact.id"), primary_key = True),
                        Column("skill_id", Integer, ForeignKey("skill.id"), primary_key=True)
                        ),
        backref = "contacts"
    )

class Skill(Base):
    __tablename__ = "skills"
    id = Column(Integer, primary_key = True)
    name = firstname = Column(String(80))
    level = Column(Integer, set max min)


engine = create_engine("sqlite:///contacts.db")