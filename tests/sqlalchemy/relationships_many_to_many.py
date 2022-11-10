from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Association(db.Model):
    __tablename__ = "association_table"
    left_id = Column(ForeignKey("left_table.id"), primary_key=True)
    right_id = Column(ForeignKey("right_table.id"), primary_key=True)
    extra_data = Column(String(50))
    child = relationship("Child", back_populates="parents")
    parent = relationship("Parent", back_populates="children")


class Parent(db.Model):
    __tablename__ = "left_table"
    id = Column(Integer, primary_key=True)
    children = relationship("Association", back_populates="parent")


class Child(db.Model):
    __tablename__ = "right_table"
    id = Column(Integer, primary_key=True)
    parents = relationship("Association", back_populates="child")