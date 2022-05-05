from utils.db import db


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(50), nullable=False)
    discount = db.Column(db.Integer, nullable=False)
    tax = db.Column(db.Integer, nullable=False)
    totalSale = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(50), nullable=True)

    

    def __init__(self, buyer, provider, discount, tax, totalSale=0, date=None) -> None:
        self.buyer = buyer
        self.provider = provider
        self.discount = discount
        self.tax = tax
        self.totalSale = totalSale
        self.date = date


    def __repr__(self) -> str:
        return f"Order({self.id}, {self.buyer}, '{self.provider}', '{self.discount}', '{self.tax}', '{self.totalSale}', '{self.date}')"
