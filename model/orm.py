import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Do this to put the db in the base folder
# Double .dirname() = parent dir
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "merch.db")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


# Parent class to TShirt, Album. This corresponds to a SKU.
class Merch(db.Model):
    merch_id = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(32))  # autogenerate from controller
    description = db.Column(db.String(64))  # autogenerate from controller
    cost = db.Column(db.Float)
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

    def __init__(self, cost, inventory):
        self.cost = cost
        self.inventory = inventory


# subclass of Merch
class TShirt(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "t_shirt"
    }

    sizes = ["S", "M", "L", "XL", "XXL", "XXL"]

    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id"),
                         primary_key=True)
    size_code = db.Column(db.Integer)
    style = db.Column(db.String(64))
    size = db.Column(db.String(3))

    def __init__(self, cost, inventory, style, size):
        super().__init__(cost, inventory)
        self.style_id = style
        self.size_code = size  # TODO integrity constraint


# subclass of Merch
class Album(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "album"
    }

    formats = ["CD", "vinyl"]

    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id"),
                         primary_key=True)
    title = db.Column(db.String(80))
    rec_format = db.Column(db.String(5))

    def __init__(self, cost, inventory, title, rec_format):
        super().__init__(cost, inventory)
        self.title = title
        self.rec_format = rec_format  # TODO integrity constraint


# list of events with opportunities to sell merch
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(12))  # longer for non-US
    country = db.column(db.String(80))
    date = db.Column(db.Date)

    def __init__(self, venue_name, city, state, country, date):
        self.venue_name = venue_name
        self.city = city
        self.state = state
        self.country = country
        self.date = date

    def __repr__(self):
        return "ID %3d:  Venue: %r  City: %r  State: %r  " \
               "Country: %r  Date: %r" % format(
                    self.event_id, self.venue_name, self.city,
                    self.state, self.country, self.date
                )


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
