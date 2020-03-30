from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import resurssifunktio

'''
This Flask application receives and sends messages. The function add_payment receives
data in application/json format.
For testing you need to run this application in order to create the necessary database.
After that you need to use command set FLASK_APP=<program_name.py>. This works in Windows.
In different OS you may need to use different command.
Then you can start the server and send the GET and POST requests.
'''
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///paymentdatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "This is the front page"
    
@app.route("/payments/add/", methods=["POST"])
def add_payment():                                # Function to save plan to the database
    handle = request.json["handle"]               # Payment name

    carprice = request.json["carprice"]           # Price of the car
    downpayment = request.json["downpayment"]     # Down payment for the car
    totalprice = request.json["totalprice"]       # Total price of the car, includes car price, interest and additional costs
    paymentmonths = request.json["paymentmonths"] # How many months in the payment plan
    monthlypayment = request.json["monthlypayment"]   # Calculate the monthly payment
    no_of_payers = request.json["no_of_payers"]         # the amount of people that share the payment
    interestrate = request.json["interestrate"]         # interestrate
    payerpayment = request.json["payerpayment"]         # the amount of payment for each individual
 
    plan = Paymentplan(                                 # Simply add the paymentplan to the database
    handle = handle,
    carprice = carprice,
    downpayment = downpayment,
    no_of_payers = no_of_payers,
    paymentmonths = paymentmonths,
    interestrate = interestrate,
    totalprice = totalprice,
    monthlypayment = monthlypayment,
    payerpayment = payerpayment
    )
    
    db.session.add(plan)                     
    db.session.commit()                           # Commit information to the database

    return "Success", 201


@app.route("/plans/<handle>", methods=["GET"])
def get_inventory(handle):                                          # Find all the payments for a handle
    lista = Paymentplan.query.filter_by(handle=handle).all()
    if len(lista) == 0:
        return "Couldn't find paymentplans"
    jsonifylist = []
    indeksi = 0
    for x in lista:
        item = lista[indeksi]
        jsonifylist.append({
        "handle": item.handle,
        "carprice": item.carprice,
        "downpayment": item.downpayment,
        "no_of_payers": item.no_of_payers,
        "paymentmonths": item.paymentmonths,
        "interestrate": item.interestrate,
        "totalprice": item.totalprice,
        "monthlypayment": item.monthlypayment,
        "payerpayment": item.payerpayment
        })
        indeksi = indeksi + 1
    return jsonify(jsonifylist)
 

class Carmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True)             # carModel ID
    paymentID = db.Column(db.Integer, db.ForeignKey("paymentplan.id"))
    manufacturer = db.Column(db.String(50), nullable=False)  # car manufacturer
    carModel = db.Column(db.String(50), nullable=False)      # car model
    year = db.Column(db.Integer, nullable=False)             # model year
    mileage = db.Column(db.Integer, nullable=False)          # miles driven
    planName = db.relationship("Paymentplan", back_populates="userPlan")
    
        
class Paymentplan(db.Model):                               # Model for payment plan
    id = db.Column(db.Integer, primary_key=True)           # plan ID
    handle = db.Column(db.String(50), nullable=False)      # name for the payment plan
    carprice = db.Column(db.Float, nullable=False)         # price of the car
    downpayment = db.Column(db.Float, nullable=False)      # amount of down payment if any
    no_of_payers = db.Column(db.Integer, nullable=False)   # number of people sharing payment
    paymentmonths = db.Column(db.Integer, nullable=False)  # period of payments
    interestrate = db.Column(db.Float, nullable=False)     # interest for payments
    totalprice = db.Column(db.Float, nullable=False)       # carPrice + interest
    monthlypayment = db.Column(db.Float, nullable=False)   # totalPrice / paymentMonths
    payerpayment = db.Column(db.Float, nullable=False)     # monthly payment for each payer
    userPlan = db.relationship("Carmodel", back_populates="planName")
    
if __name__ == "__main__":                                 # Create the database
    db.create_all()