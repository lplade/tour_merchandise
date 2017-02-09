import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

# Do this to put the db in the base folder
# Double .dirname() = parent dir


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "merch.db")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Squelch warnings
db = SQLAlchemy(app)


# Parent class to TShirt, Album. This corresponds to a SKU.
class Merch(db.Model):
    merch_id = db.Column(db.Integer, primary_key=True)
    # We store a description as a common field to display for all subclasses
    # controller should call generate_description() before committing object.
    description = db.Column(db.String(64))
    price = db.Column(db.Float)
    inventory = db.Column(db.Integer)
    type = db.Column(db.String(12))
    # this is the discriminator field, and should be one of
    # * 'tshirt'
    # * 'album'
    #
    # http://docs.sqlalchemy.org/en/latest/orm/inheritance.html
    __mapper_args__ = {
        "polymorphic_identity": "merch",
        "polymorphic_on": type
    }

    def __init__(self, price, inventory):
        self.price = price
        self.inventory = inventory


# subclass of Merch
class TShirt(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "t_shirt"
    }

    sizes = ["S", "M", "L", "XL", "XXL", "XXXL"]
    # This goes into form fields

    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id", ondelete="CASCADE"),
                         primary_key=True)
    style = db.Column(db.String(64))
    size = db.Column(db.String(3))

    def __init__(self, price, inventory, style, size):
        super().__init__(price, inventory)
        self.style = style
        self.size = size  # TODO integrity constraint

    def generate_description(self):
        return "{} t-shirt, {}".format(self.style, self.size)


# subclass of Merch
class Album(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "album"
    }

    formats = ["CD", "vinyl"]

    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id", ondelete="CASCADE"),
                         primary_key=True)
    title = db.Column(db.String(80))
    rec_format = db.Column(db.String(5))

    def __init__(self, price, inventory, title, rec_format):
        super().__init__(price, inventory)
        self.title = title
        self.rec_format = rec_format  # TODO integrity constraint

    def generate_description(self):
        return "{}, on {}".format(self.title, self.rec_format)


# list of events with opportunities to sell merch
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(12))  # longer for non-US
    country = db.Column(db.String(80))
    event_date = db.Column(db.Date)

    def __init__(self, venue_name, city, state, country, date_string):
        self.venue_name = venue_name
        self.city = city
        self.state = state
        self.country = country
        # Convert a string to datetime.date object
        self.event_date = self.string_to_date(date_string)

    @staticmethod
    def string_to_date(date_string):
        """
        Converts a sting in YYYY-MM-DD format to a datetime.date object
        :param date_string:
        :return:
        """
        return datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

    @staticmethod
    def date_to_string(_date):
        """
        Converts a datetime.date object to a YYYY-MM-DD string
        :param _date:
        :return:
        """
        return _date.strftime("%Y-%m-%d")


# list of items sold per event
# http://flask-sqlalchemy.pocoo.org/2.1/models/#many-to-many-relationships
# In SQLAlchemy terms, this is an "Association Object"
class MerchSold(db.Model):
    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id"),
                         primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey("event.event_id"),
                         primary_key=True)
    items_sold = db.Column(db.Integer)
