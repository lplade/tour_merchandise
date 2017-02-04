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

    def __repr__(self):
        # we shouldn't ever really use the repr of this superclass
        return "ID %3d:  Cost: $%5.2f Inv: %4d" % format(
            self.merch_id, self.cost, self.inventory
        )


# subclass of Merch
class TShirt(Merch):
    __mapper_args__ = {
        "polymorphic_identity": "t_shirt"
    }
    merch_id = db.Column(db.Integer,
                         db.ForeignKey("merch.merch_id"),
                         primary_key=True)
    style_id = db.Column(db.Integer, db.ForeignKey("t_shirt_style.style_id"))
    size_code = db.Column(db.Integer)

    def __init__(self, cost, inventory, style_id, size_code):
        super().__init__(cost, inventory)
        self.style_id = style_id
        self.size_code = size_code

    def __repr__(self):
        return "ID %3d:  Cost: $%5.2f  Inv: %4d  Style: %r  Size: %r" % format(
            self.merch_id, self.cost, self.inventory,
            self.style_id, self.size_code
            # TODO lookup and display correct strings
        )


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

    def __init__(self, cost, inventory, title, formot_code):
        super().__init__(cost, inventory)
        self.title = title
        self.format_code = formot_code

    def __repr__(self):
        return "ID %3d:  Cost: $%5.2f  Inv: %4d  Title: %r  Format: %r" % \
                format(
                    self.merch_id, self.cost, self.inventory,
                    self.title, self.format_code
                    # TODO lookup and display correct strings
                )


# table to map t-shirt style name
class TShirtStyle(db.Model):
    style_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(80))

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description


# table to map t-shirt size name
class TShirtSize(db.Model):
    size_id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String(4))

    def __init__(self, size):
        self.size = size

    def __repr__(self):
        return self.size

    @staticmethod
    def populate_default():
        """
        Use to put some standard options in a new db
        :return:
        """
        _sizes = ["S", "M", "L", "XL", "XXL", "XXL"]
        for s in _sizes:
            new_size = TShirtSize(s)
            db.session.add(new_size)
        db.session.commit()


# table to map album format name
class Format(db.Model):
    format_code = db.Column(db.Integer, primary_key=True)
    media_format = db.Column(db.String(5))  # "Vinyl" or "CD"

    def __init__(self, media_format):
        self.media_format = media_format

    def __repr__(self):
        return self.media_format

    @staticmethod
    def populate_default():
        """
        Use to put some standard options in a new db
        :return:
        """
        _formats = ["CD", "vinyl"]
        for f in _formats:
            new_format = Format(f)
            db.session.add(new_format)
        db.session.commit()


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
