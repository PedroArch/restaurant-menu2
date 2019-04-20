from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine("sqlite:///restaurantmenu.db")
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
@app.route("/restaurants/")
def show_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template("restaurants.html", restaurants=restaurants)


@app.route("/restaurants/new", methods=["GET", "POST"])
def new_restaurant():
    if request.method == "POST":
        restaurant = Restaurant(name=request.form['name'])
        session.add(restaurant)
        session.commit()
        flash("New restaurant created!")

        return redirect(url_for("show_restaurants"))
    else:
        return render_template("new_restaurant.html")


@app.route("/restaurants/<int:restaurant_id>/edit", methods=["GET", "POST"])
def edit_restaurant(restaurant_id):

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        restaurant.name = request.form['name']

        session.add(restaurant)
        session.commit()
        flash("Restaurant succcessfully edit")

        return redirect(url_for("show_restaurants"))

    else:
        return render_template("edit_restaurant.html", restaurant_id=restaurant_id, restaurant=restaurant)


@app.route("/restaurants/<int:restaurant_id>/delete", methods=["GET", "POST"])
def delete_restaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == "POST":
        session.delete(restaurant)
        session.commit()
        flash("Restaurant succcessfully deleted")

        return redirect(url_for("show_restaurants"))
    else:
        return render_template("delete_restaurant.html", restaurant_id=restaurant_id, restaurant=restaurant)


@app.route("/restaurants/<int:restaurant_id>")
@app.route("/restaurants/<int:restaurant_id>/menu/")
def show_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template("menu.html", restaurant=restaurant, items=items)


@app.route("/restaurants/<int:restaurant_id>/menu/new", methods=["GET", "POST"])
def new_menu_item(restaurant_id):
    if request.method == "POST":
        new_item = MenuItem(name = request.form['name'],
                            description = request.form['description'],
                            price = request.form['price'],
                            course = request.form['course'],
                            restaurant_id = restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New menu item created!")

        return redirect(url_for('show_menu', restaurant_id = restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant_id=restaurant_id)


@app.route("/restaurants/<int:restaurant_id>/menu/<int:item_id>/edit", methods=["GET", "POST"])
def edit_menu_item(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == "POST":
        item.name = request.form['name']
        item.description = request.form['description']
        item.price = request.form['price']
        item.course = request.form['course']
        item.restaurant_id = restaurant_id

        session.add(item)
        session.commit()
        flash("Menu Item succcessfully edited")

        return redirect(url_for("show_menu", restaurant_id=restaurant_id))

    else:
        return render_template("edit_menu_item.html", restaurant_id=restaurant_id, item_id=item_id, item=item)


@app.route("/restaurants/<int:restaurant_id>/menu/<int:item_id>/delete", methods=["GET", "POST"])
def delete_menu_item(restaurant_id, item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    item = session.query(MenuItem).filter_by(id=item_id).one()
    if request.method == "POST":
        session.delete(item)
        session.commit()
        flash("Menu Item succcessfully deleted")

        return redirect(url_for("show_menu", restaurant_id=restaurant_id))
    else:
        return render_template("delete_menu_item.html", restaurant_id= restaurant_id, item_id = item_id, item=item)


# JSONify endpoints

@app.route("/restaurants/JSON")
def JSON_restaurants():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[restaurant.serialize for restaurant in restaurants])

@app.route("/restaurants/<int:restaurant_id>/JSON")
def JSON_menu_restaurant(restaurant_id):
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItem=[item.serialize for item in items])

@app.route("/restaurants/<int:restaurant_id>/menu/<int:item_id>/JSON")
def JSON_menu_item(restaurant_id, item_id):
    item = session.query(MenuItem).filter_by(id=item_id).one()
    return jsonify(MenuItem=[item.serialize])

# End of File #
if __name__ == "__main__":
    app.secret_key = "SUPER_SECRECT_KEY"
    app.debug = True
    app.run(host="0.0.0.0", port=5000, threaded=False)
