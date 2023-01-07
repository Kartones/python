#!/usr/bin/python
# -!- coding: utf-8 -!-

from functools import wraps
from flask import Flask, request, redirect, render_template, make_response

import config
from services.shopping_lists import ShoppingLists

app = Flask(__name__)


def item_sort_function(item):
    return int(item[1])


def authenticated(func):
    @wraps(func)
    def wrapped_f(*args, **kwds):
        can_pass = False
        if config.COOKIE_KEY in request.cookies:
            can_pass = request.cookies[config.COOKIE_KEY] == config.COOKIE_PASS

        if can_pass:
            return func(*args, **kwds)
        else:
            return redirect("{}login".format(config.BASE_URL_PATH), code=302)
    return wrapped_f


@app.route("/", methods=["GET"])
@authenticated
def lists():
    lists = ShoppingLists(config).get_all_lists()
    return render_template("lists.html", lists=lists, base_url_path=config.BASE_URL_PATH)


@app.route("/items/<list_name>", methods=["GET", "POST"])
@authenticated
def list_items(list_name):
    shopping_lists = ShoppingLists(config)
    if request.method == "POST":
        form_data = [key for key in request.form.keys()]
        action, item_name = form_data[0].split(config.SEPARATOR) if form_data else (None, None)
        shopping_lists.save_list_item_action(list_name, item_name, action)
        return "", 204
    else:
        items = shopping_lists.get_items(list_name)
        order_by = request.args.get("order_by")
        if order_by == "state":
            items = sorted(items, key=item_sort_function, reverse=True)

        return render_template(
            "items.html",
            list_name=list_name, items=items,
            base_url_path=config.BASE_URL_PATH,
            separator=config.SEPARATOR
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("pass") == config.PASS:
            response = make_response(redirect(config.BASE_URL_PATH, code=302))
            # 1 year age
            response.set_cookie(key=config.COOKIE_KEY, value=config.COOKIE_PASS, max_age=31536000)
            return response
        else:
            return render_template("login.html", base_url_path=config.BASE_URL_PATH)
    else:
        return render_template("login.html", base_url_path=config.BASE_URL_PATH)


if __name__ == "__main__":
    app.run(debug=config.DEBUG, host=config.HOST_IP)
