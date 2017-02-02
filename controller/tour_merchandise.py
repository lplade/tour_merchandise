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


@app.route('/')
def index():
    all_merch = db.query.queryall(Merch)
    return render_template("main.html", all_merch)


if __name__ == '__main__':
    app.run()

