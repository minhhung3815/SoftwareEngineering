import sqlite3

from flask import Blueprint
from flask_login import current_user, login_required

backend = Blueprint("backend", __name__)


@backend.route("/cart/clear", methods=["POST"])
@login_required
def clear_cart():
    con = sqlite3.connect("test.db")
    con.execute("DELETE FROM cart WHERE id = ?", (current_user.get_id(),))
    con.commit()
    con.close()
    return "", 204


@backend.route("/cart/items/<int:item_id>", methods=["DELETE"])
@login_required
def remove_cart_item(item_id: int):
    con = sqlite3.connect("test.db")
    user_id = current_user.get_id()
    con.execute("DELETE FROM cart WHERE id = ? AND food_id = ?", (user_id, item_id))
    con.commit()
    con.close()
    return "", 204
