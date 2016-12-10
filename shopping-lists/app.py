#!/usr/bin/python
# -!- coding: utf-8 -!-

from functools import wraps
from flask import Flask, request, redirect, render_template, make_response

import config
from services.shopping_lists import ShoppingLists

app = Flask(__name__)


def authenticated(func):
    @wraps(func)
    def wrapped_f(*args, **kwds):
        can_pass = False
        if config.COOKIE_KEY in request.cookies:
            can_pass = request.cookies[config.COOKIE_KEY] == config.COOKIE_PASS

        if can_pass:
            return func(*args, **kwds)
        else:
            return redirect("/login", code=302)
    return wrapped_f


@app.route("/", methods=["GET"])
@authenticated
def lists():
    lists = ShoppingLists(config).get_all_lists()
    return render_template("lists.html", lists=lists)


@app.route("/items/<list_name>", methods=["GET", "POST"])
@authenticated
def list_items(list_name):
    shopping_lists = ShoppingLists(config)
    if request.method == "POST":
        items_with_state = [key for key in request.form.keys()][0].split(",")
        shopping_lists.save_list(list_name, items_with_state)
        return "", 204
    else:
        items = shopping_lists.get_items(list_name)
        return render_template("items.html", list_name=list_name, items=items)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("pass") == config.PASS:
            response = make_response(redirect("/", code=302))
            # 1 year age
            response.set_cookie(key=config.COOKIE_KEY, value=config.COOKIE_PASS, max_age=535680)
            return response
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run()
