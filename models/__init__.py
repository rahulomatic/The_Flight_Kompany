from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .flight import Flight
from .booking import Booking
