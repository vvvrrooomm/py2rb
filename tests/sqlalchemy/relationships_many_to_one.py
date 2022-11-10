from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Parent(db.Model):
    __tablename__ = "parent_table"
    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey("child_table.id"))
    child = relationship("Child")


class Child(db.Model):
    __tablename__ = "child_table"
    id = Column(Integer, primary_key=True)