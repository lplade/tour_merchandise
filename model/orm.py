from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///merch.db"
db = SQLAlchemy(app)


# Parent class to TShirt,
class Merch(db.Model):
    merch_id = db.Column(db.Integer, primary_key=True)
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

    def __repr__(self):
        pass


# subclass of Merch
class TShirt(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "tshirt"
    }
    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id"),
                         primary_key=True)
    style_id = db.Column(db.Integer, db.ForeignKey("tshirtstyle.style_id"))
    size_code = db.Column(db.Integer)


# subclass of Merch
class Album(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "album"
    }
    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id"),
                         primary_key=True)
    title = db.Column(db.String(80))
    format_code = db.Column(db.Integer, db.ForeignKey("format.format_code"))


# table to map t-shirt style name
class TShirtStyle(db.Model):
    style_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))


# table to map t-shirt size name
class TShirtSize(db.Model):
    size_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(4))


# table to map album format name
class Format(db.Model):
    format_code = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String(5))  # "Vinyl" or "CD"


# list of events with opportunities to sell merch
class Event(db.Model):
    event_id = db.Column(db.Integer, primary_key=True)
    venue_name = db.Column(db.String(80))
    city = db.Column(db.String(80))
    state = db.Column(db.String(12))  # longer for non-US
    country = db.column(db.String(80))
    date = db.Column(db.Date)


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
