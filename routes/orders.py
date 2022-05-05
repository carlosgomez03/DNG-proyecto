from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from forms.orderCreateForm import OrderCreateForm
from utils.db import db
from models.orders import Order
from models.orderdetails import OrderDetail
from datetime import date

orders = Blueprint("orders", __name__, url_prefix="/orders")


@orders.route("/")
@login_required
def home():
    orderList = Order.query.all()
    return render_template("orders/home.html", items=orderList, user=current_user)


@orders.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = OrderCreateForm(provider=current_user.username)
    if form.validate_on_submit():
        buyer = form.buyer.data
        provider = form.provider.data
        discount = form.discount.data
        tax = form.tax.data
        newOrder = Order(buyer, provider, discount, tax)
        db.session.add(newOrder)
        db.session.commit()
        return redirect(url_for("orders.home"))
    return render_template("orders/create.html", form=form)


@orders.route("/finalize/<int:id>")
@login_required
def finalize(id):
    currentOrder = Order.query.get(id)
    currentDate = date.today().isoformat()
    currentOrder.date = currentDate
    db.session.add(currentOrder)
    db.session.commit()
    return redirect(url_for("orders.home"))

@orders.route("/delete/<int:id>")
@login_required
def delete(id):
    currentOrder = Order.query.get(id)
    OrderDetail.query.filter_by(orderId=id).delete()
    
    db.session.delete(currentOrder)
    db.session.commit()
    return redirect(url_for("orders.home"))