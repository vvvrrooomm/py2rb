from flask_login import current_user
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# parent
class Organizers(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    first_name = Column(String(100))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users")
    reservations = relationship("Reservations")

class Users(db.Model):
    id = Column(Integer, autoincrement=True, primary_key=True)
    
class Reservations(db.Model):
    organizer_id = Column(Integer, ForeignKey("organizers.id"))
    organizer = relationship("Organizers", back_populates="reservations")
    