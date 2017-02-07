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
            # flash("New t-shirt SKU was added successfully")
        except KeyError:
            error = "Key error! " + str(request)

    all_tshirts = TShirt.query.all()
    sizes = TShirt.sizes

    return render_template("tshirts.html",
                           all_tshirts=all_tshirts,
                           sizes=sizes,
                           error=error)


@app.route("/albums")
def album_list():
    all_albums = Album.query.all()
    return render_template("albums.html", all_albums=all_albums)

# pretty useful:
# https://techarena51.com/index.php/flask-sqlalchemy-tutorial/


@app.route("/events")
def event_list():
    all_events = Event.query.all()
    return render_template("events.html", all_events=all_events)

if __name__ == "__main__":
    app.run()

