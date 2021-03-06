#!/usr/bin/python3

# note that the Flask imports are in orm.py
from model.orm import *
from flask import render_template, request, flash, redirect, url_for

# tell flask about our folder setup
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # ../
view_dir = os.path.join(base_dir, "view")  # ../view
template_dir = os.path.join(view_dir, "templates")  # ../view/templates
static_dir = os.path.join(view_dir, "static")  # ../view/static

# print(static_dir)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


@app.template_filter("mydate")
def format_date(value, format="%Y-%m-%d"):
    """
    Create a custom formatter for Jinja2 so it doesn't choke on datetime.date objects
    :param value:
    :param format:
    :return:
    """
    return value.strftime(format)

app.jinja_env.filters['mydate'] = format_date

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
            t_shirt = TShirt(price=float(request.form["price"]),
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
            tshirt.price = float(request.form["price"])
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
            album = Album(price=float(request.form["price"]),
                          inventory=int(request.form["inventory"]),
                          title=request.form["title"],
                          rec_format=request.form["format"])
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
            album.price = float(request.form["price"])
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


@app.route("/delete/<int:merch_id>", methods=["GET"])
def delete_merch(merch_id):
    """
    Delete an item.
    Need to pass merch_id and type (t_shirt or album) via form
    In the real world, this is a disastrously insecure implementation.
    :return:
    """
    # Would prefer to use HTTP DELETE instead of GET
    # will have to review http://flask.pocoo.org/snippets/1/

    error = None
    info = None

    merch = Merch.query.get(merch_id)
    db.session.delete(merch)
    db.session.commit()

    return redirect("/", code=303)
    # TODO pass some feedback


@app.route("/events", methods=["POST", "GET"])
def event_list():
    """

    :return:
    """
    error = None
    info = None

    if request.method == "POST":
        try:
            event = Event(venue_name=request.form["venue_name"],
                          city=request.form["city"],
                          state=request.form["state"],
                          country=request.form["country"],
                          date_string=request.form["event_date"]
                          )
            db.session.add(event)
            db.session.commit()
        except KeyError:
            error = "Key error!" + str(request)

    all_events = Event.query.all()

    return render_template("events.html", all_events=all_events, error=error, info=info)


@app.route("/event/<int:event_id>", methods=["POST", "GET"])
def event_properties(event_id):
    error = None
    info = None

    event = Event.query.get(event_id)
    if event is None:
        return render_template("enotfound.html",
                               event_id=event_id)
    elif request.method == "POST":
        try:
            # Update the stored object with new value from form
            event.venue_name = request.form["venue_name"]
            event.city = request.form["city"]
            event.state = request.form["state"]
            event.country = request.form["country"]
            print(request.form["event_date"])
            event.event_date = event.string_to_date(request.form["event_date"])

            db.session.commit()
            info = "Record updated"

        except KeyError:
            error = "Key error! " + str(request)

    # Regardless of whether GET or returning from POST, display details

    return render_template("event.html",
                           event=event,
                           error=error,
                           info=info)


@app.route("/delete_event/<int:event_id>", methods=["GET"])
def delete_event(event_id):
    error = None
    info = None

    event = Event.query.get(event_id)
    db.session.delete(event)
    db.session.commit()

    return redirect("/events", code=303)
    # TODO pass some feedback


@app.route("/merchevent/<int:event_id>", methods=["POST", "GET"])
def merch_event(event_id):

    error = None
    info = None

    # Here is where we deleted a bunch of awful code to manually map
    # data between related tables before figuring out how to make the
    # ORM handle it

    all_merch = Merch.query.all()
    event = Event.query.get(event_id)
    if event is None:
        return render_template("enotfound.html",
                               event_id=event_id)
    elif request.method == "POST":
        _merch_id = int(request.form["merch_id"])
        _num_sold = int(request.form["num_sold"])

        found_entry = None
        # first, check if that MerchSold is in the table
        for item in event.merch_sold_list:
            if item.merch_id == _merch_id:
                found_entry = item
        # if not, add it to the table
        if found_entry is None:
            merch = Merch.query.get(_merch_id)
            # TODO handle failure of above
            merch_sold = MerchSold(
                merch=merch, event=event, items_sold=_num_sold
            )
            db.session.add(merch_sold)
        # otherwise, update the value
        else:
            found_entry.sell_merch(_num_sold)

        db.session.commit()
        info = "Updated"

    return render_template("merchevent.html",
                           error=error,
                           info=info,
                           all_merch=all_merch,
                           event=event)


@app.route("/<path:path>")
def serve_static(path):
    """
    Assume any request not matching above routes is request for static resource
    :param path:
    :return:
    """
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run()

