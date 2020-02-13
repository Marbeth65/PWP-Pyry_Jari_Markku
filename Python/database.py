
from flask import Flask, request, json, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine import Engine
from sqlalchemy import event

app = Flask("carpayment")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///carpayment.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.relationship("PaymentPlan", back_populates="user_keyword")
    phone = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String, nullable=True)


class PaymentPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_keyword = db.relationship("User", back_populates="keyword")
    carprice = db.Column(db.Float, nullable=True)
    downpayment = db.Column(db.Float, nullable=True)
    interest_rate = db.Column(db.Float, nullable=True)
    yearly_interest_rate = db.Column(db.Float, nullable=True)
    monthly_payment = db.Column(db.Float, nullable=True)
    amount_of_interest = db.Column(db.Float, nullable=True)
    total_price = db.Column(db.Float, nullable=True)
    people_sharing = db.Column(db.Integer, nullable=True)
    
"""
@app.route("/products/add/", methods=['GET', 'POST'])
def add_product():
    # This branch adds the product to the databaseinte
    try:
        product_name = request.json["handle"]
        handle = Product.query.filter_by(name=product_name).first()
        if handle:
            weight = float(request.json["weight"])
            price =  float(request.json["price"])
            product = Product(product_name=handle, weight=weight, price=price)
            db.session.add(product)
            db.session.commit()
            return 'Successful', 201
        else:
            return KeyError
    
        elif handle == Product.query.filter_by(name=product_name):
            return 'Handle already exists', 409
        elif request.json == None:
            return 'Request content type must be JSON', 415
        elif request.method != 'POST':
            return 'POST method required', 405
        else:
            pass
            
    except (KeyError, ValueError, IntegrityError):
        return 'Incomplete request - missing fields', 400


@app.route("/storage/<product>/add/", methods=["POST"])
def add_to_storage(product):
    # This branch adds the product to the storage
    try:
        product = Product.query.filter_by(name=product).first()
        if product:
            location = request.json["location"]
            qty =  int(request.json["qty"])
            inv = Inventory(product=product, location=location, quantity=qty)
            db.session.add(inv)
            db.session.commit()
            return 'Successful', 201
        elif product == Product.query.filter_by(name=product):
            return 'Product not found', 404
        elif request.json == None:
            return 'Request content type must be JSON', 415
        elif request.method != 'POST':
            return 'POST method required', 405
        else:
            pass
            
    except (KeyError, ValueError, IntegrityError):
        return 'Incomplete request - missing fields', 400
    
    

@app.route("/storage/", methods=["GET"])
def get_inventory():
    # This branch reads the data from storage
    try:
        handle_name = request.json["handle"]
        handle = Product.query.filter_by(name=handle_name).first()
        if handle:
            weight = float(request.json["weight"])
            price =  float(request.json["price"])
            location = inventory.location
            qty = inventory.quantity
        elif request.method != 'GET':
            return 'POST method required', 405
        else:
            pass
    except (KeyError, ValueError, IntegrityError):
        return 'Incomplete request - missing fields', 400
        
 """

    