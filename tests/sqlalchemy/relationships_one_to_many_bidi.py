from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Parent(Base):
    __tablename__ = "parent_table"
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")


class Child(Base):
    __tablename__ = "child_table"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent_table.id"))
    parent = relationship("Parent", back_populates="children")