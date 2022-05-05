from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from forms.orderDetailCreateForm import OrderDetailCreateForm
from utils.db import db
from models.orders import Order
from models.orderdetails import OrderDetail

orderDetails = Blueprint("orderDetails", __name__, url_prefix="/orderDetails")


@orderDetails.route("/")
@login_required
def home():
    orderDetailList = OrderDetail.query.all()
    return render_template("orderDetails/homegeneral.html", user=current_user, items = orderDetailList)

@orderDetails.route("/home<int:orderId>")
@login_required
def homeByOrderId(orderId):
    currentOrder = Order.query.filter_by(id=orderId).first()
    orderDetailList = OrderDetail.query.filter_by(orderId=orderId).all()
    return render_template("orderDetails/home.html", order=currentOrder, user=current_user, items=orderDetailList, orderId=orderId)

@orderDetails.route("/create/<int:orderId>", methods=["GET", "POST"])
@login_required
def createByOrderId(orderId):
    form = OrderDetailCreateForm(orderId=orderId)
    if form.validate_on_submit():
        currentOrder = Order.query.filter_by(id=orderId).first()

        quantity = form.quantity.data
        description = form.description.data
        unitCost = form.unitCost.data
        totalCost = quantity * unitCost
        currentOrder.totalSale += totalCost

        newOrderDetail = OrderDetail(orderId, quantity, description, unitCost, totalCost)
        db.session.add(newOrderDetail)
        db.session.add(currentOrder)
        db.session.commit()
        return redirect(url_for("orderDetails.homeByOrderId", orderId=orderId))
    return render_template("orderDetails/create.html", form=form, user=current_user, orderId=orderId)

@orderDetails.route("/delete/<int:id>/<int:orderId>")
@login_required
def delete(id, orderId):
    currentOrderDetail = OrderDetail.query.get(id)
    
    #Eliminar el total
    currentOrder = Order.query.filter_by(id=orderId).first()
    currentOrder.totalSale -= currentOrderDetail.totalCost
    
    db.session.add(currentOrder)
    db.session.delete(currentOrderDetail)
    db.session.commit()
    
    return redirect(url_for("orderDetails.homeByOrderId", orderId=orderId))

@orderDetails.route("/update/<int:id>/<int:orderId>", methods=["GET", "POST"])
@login_required
def updateByOrderId(id, orderId):
    currentDetail = OrderDetail.query.filter_by(id=id).first()    
    form = OrderDetailCreateForm(orderId=orderId, quantity=currentDetail.quantity, description=currentDetail.description, unitCost=currentDetail.unitCost)
    if form.validate_on_submit():
        currentOrder = Order.query.filter_by(id=orderId).first()
        currentOrder.totalSale -= currentDetail.totalCost

        currentDetail.quantity = form.quantity.data
        currentDetail.description = form.description.data
        currentDetail.unitCost = form.unitCost.data
        currentDetail.totalCost = currentDetail.quantity * currentDetail.unitCost
        currentOrder.totalSale += currentDetail.totalCost

        db.session.add(currentDetail)
        db.session.add(currentOrder)
        db.session.commit()
        print(id, orderId)
        return redirect(url_for("orderDetails.homeByOrderId",id=id,  orderId=orderId))
    return render_template("orderDetails/update.html", form=form, user=current_user, id=id, orderId=orderId)        
        
@orderDetails.route("/report/<int:orderId>")
@login_required
def report(orderId):
    currentOrder = Order.query.filter_by(id=orderId).first()
    orderDetailList = OrderDetail.query.filter_by(orderId=orderId).all()
    total_con_descuento = currentOrder.totalSale*(1-(currentOrder.discount)/100)
    total_impuesto = round(total_con_descuento*(1+(currentOrder.tax)/100),2)
    return render_template("orderDetails/report.html", order=currentOrder, user=current_user, items=orderDetailList, total_ajustado =total_impuesto)
