import sqlite3

from flask import Blueprint, abort, request
from flask_login import current_user, login_required

backend = Blueprint("backend", __name__)


@backend.route("/cart/clear", methods=["POST"])
@login_required
def clear_cart():
    con = sqlite3.connect("test.db")
    user_id = int(current_user.get_id())
    con.execute("DELETE FROM cart WHERE id = ?", (user_id,))
    con.commit()
    con.close()
    return "", 204


@backend.route("/cart/items/<int:item_id>", methods=["DELETE"])
@login_required
def remove_cart_item(item_id: int):
    con = sqlite3.connect("test.db")
    user_id = int(current_user.get_id())
    con.execute("DELETE FROM cart WHERE id = ? AND food_id = ?", (user_id, item_id))
    con.commit()
    con.close()
    return "", 204


@backend.route("/cart", methods=["POST"])
@login_required
def add_cart_item():
    data = request.get_json()
    if data is None:
        abort(400)

    con = sqlite3.connect("test.db")
    con.row_factory = sqlite3.Row
    cur = con.execute("SELECT * FROM food WHERE id = ?", (data["item_id"],))
    food = cur.fetchone()

    params = {
        "user_id": int(current_user.get_id()),
        "food_name": food["name"],
        "quantity": data["quantity"],
        "path": food["path"],
        "food_id": data["item_id"],
        "price": food["price"],
    }
    con.execute(
        """
        INSERT INTO cart(id, food_name, amount, path, food_id, price)
        VALUES (:user_id, :food_name, :quantity, :path, :food_id, :price)
        ON CONFLICT (id, food_id) DO
        UPDATE SET amount = amount + :quantity
    """,
        params,
    )
    con.commit()
    con.close()
    return "", 204
