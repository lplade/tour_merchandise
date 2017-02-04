#!/usr/bin/python3

# note that the Flask imports are in orm.py
from model.orm import *
from flask import render_template

# tell flask about our folder setup
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))  # ../
view_dir = os.path.join(base_dir, "view")  # ../view
template_dir = os.path.join(view_dir, "templates")  # ../view/templates
static_dir = os.path.join(view_dir, "static")  # ../view/static

print(template_dir)

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)


"""
ROUTES
"""


@app.route("/")
def index():
    all_merch = Merch.query.all()
    return render_template("main.html", all_merch=all_merch)


@app.route("/tshirts")
def tshirt_list():
    all_styles = TShirtStyle.query.all()
    all_sizes = TShirtSize.query.all()
    all_tshirts = TShirt.query.all()
    return render_template("tshirts.html", all_tshirts=all_tshirts)


@app.route("/albums")
def album_list():
    all_albums = Album.query.all()
    return render_template("albums.html", all_albums=all_albums)


@app.route("/addnew")
def add_new_merch():
    # Need all the support tables for
    all_styles = TShirtStyle.query.all()
    all_sizes = TShirtSize.query.all()
    all_formats = Format.query.all()


@app.route("/maintenance")
def db_maintenance():
    all_sizes = TShirtSize.query.all()
    all_formats = Format.query.all()
    return render_template("maintenance.html",
                           all_sizes=all_sizes,
                           all_formats=all_formats)

if __name__ == "__main__":
    app.run()

