from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# in sqlalchemy only exists as bidirectional version:
# One To One is essentially a bidirectional relationship with a scalar 
# attribute on both sides. Within the ORM, “one-to-one” is considered 
# as a convention where the ORM expects that only one related row will 
# exist for any parent row.
class Parent(db.Model):
    __tablename__ = "parent_table"
    id = Column(Integer, primary_key=True)

    # previously one-to-many Parent.children is now
    # one-to-one Parent.child
    child = relationship("Child", back_populates="parent", uselist=False)


class Child(db.Model):
    __tablename__ = "child_table"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent_table.id"))

    # many-to-one side remains, see tip below
    parent = relationship("Parent", back_populates="child")