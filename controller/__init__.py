#!/usr/bin/python3

# note that the Flask imports are in orm.py
from model.orm import *
from flask import render_template, request, flash, redirect, url_for

# tell flask about our folder setup
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # ../
view_dir = os.path.join(base_dir, "view")  # ../view
template_dir = os.path.join(view_dir, "templates")  # ../view/templates
static_dir = os.path.join(view_dir, "static")  # ../view/static

# print(template_dir)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


"""
ROUTES
"""


@app.route("/")
def index():
    all_merch = Merch.query.all()
    return render_template("main.html", all_merch=all_merch)


@app.route("/tshirts", methods=["POST", "GET"])
def tshirt_list():
    """
    Renders a list of all TShirts, and allows submission of new TShirt by form
    :return:
    """
    error = None
    if request.method == "POST":
        try:
            t_shirt = TShirt(cost=float(request.form["price"]),
                             inventory=int(request.form["inventory"]),
                             style=request.form["style"],
                             size=request.form["size"])
            t_shirt.description = t_shirt.generate_description()
            db.session.add(t_shirt)
            db.session.commit()
            # TODO figure out flash
            # flash("New t-shirt SKU was added successfully")
        except KeyError:
            error = "Key error! " + str(request)

    all_tshirts = TShirt.query.all()
    sizes = TShirt.sizes

    return render_template("tshirts.html",
                           all_tshirts=all_tshirts,
                           sizes=sizes,
                           error=error)

@app.route("/tshirt/<int:merch_id>", methods=["POST", "GET"])
def tshirt_properties(merch_id):
    """
    Display properties for a single t-shirt.
    Allows us to update or delete record.
    :param merch_id:
    :return:
    """

    # Would prefer to use HTTP PUT. This appears to be not straightforward.

    error = None
    info = None

    tshirt = TShirt.query.get(merch_id)
    if tshirt is None:
        return render_template("notfound.html",
                               merch_id=merch_id)
    elif request.method == "POST":
        try:
            # Update the stored object with new values from form
            tshirt.cost = float(request.form["price"])
            tshirt.inventory = int(request.form["inventory"])
            tshirt.style = request.form["style"]
            tshirt.size = request.form["size"]
            tshirt.description = tshirt.generate_description()

            db.session.commit()
            info = "Record updated"

        except KeyError:
            error = "Key error! " + str(request)

    # Regardless of whether GET or returning from POST, display details

    sizes = TShirt.sizes
    return render_template("tshirt.html",
                           tshirt=tshirt,
                           sizes=sizes,
                           error=error,
                           info=info)


@app.route("/albums", methods=["POST", "GET"])
def album_list():
    """
    Renders a list of all Albums, and allows submission of new Album by form
    :return:
    """
    error = None
    if request.method == "POST":
        try:
            album = Album(cost=float(request.form["price"]),
                          inventory=int(request.form["inventory"]),
                          title=request.form("title"),
                          rec_format=request.form("format"))
            album.description = album.generate_description()
            db.session.add(album)
            db.session.commit()
        except KeyError:
            error = "Key error! " + str(request)

    all_albums = Album.query.all()
    formats = Album.formats

    return render_template("albums.html",
                           all_albums=all_albums,
                           formats=formats,
                           error=error)

# pretty useful:
# https://techarena51.com/index.php/flask-sqlalchemy-tutorial/


@app.route("/album/<int:merch_id>", methods=["POST", "GET"])
def album_properties(merch_id):
    """
    Display properties for a single t-shirt.
    Allows us to update or delete record.
    :param merch_id:
    :return:
    """

    # Would prefer to use HTTP PUT. This appears to be not straightforward.

    error = None
    info = None

    album = Album.query.get(merch_id)
    if album is None:
        return render_template("notfound.html",
                               merch_id=merch_id)
    elif request.method == "POST":
        try:
            # Update the stored object with new values from form
            album.cost = float(request.form["price"])
            album.inventory = int(request.form["inventory"])
            album.title = request.form["title"]
            album.rec_format = request.form["rec_format"]
            album.description = album.generate_description()

            db.session.commit()
            info = "Record updated"

        except KeyError:
            error = "Key error! " + str(request)

    # Regardless of whether GET or returning from POST, display details

    formats = Album.formats
    return render_template("album.html",
                           album=album,
                           formats=formats,
                           error=error,
                           info=info)


@app.route("/events")
def event_list():
    all_events = Event.query.all()
    return render_template("events.html", all_events=all_events)

if __name__ == "__main__":
    app.run()

