#!/usr/bin/python3

# note that the Flask imports are in orm.py
from model.orm import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()

