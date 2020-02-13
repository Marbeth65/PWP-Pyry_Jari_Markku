from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

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
    carPrice = request.json["carPrice"]           # Price of the car
    downPayment = request.json["downPayment"]     # Down payment for the car
    totalPrice = request.json["totalPrice"]       # Total price of the car, includes car price, 
                                                  # interest and additional costs
    paymentMonths = request.json["paymentMonths"] # How many months in the payment plan
    montlyPayment = totalPrice / paymentMonths    # Calculate the monthly payment
    
    plan = Paymentplan(
    handle = handle,
    carPrice = carPrice,
    totalPrice = totalPrice,
    paymentMonths = paymentMonths,
    montlyPayment = montlyPayment
    )
    db.session.add(plan)                     
    db.session.commit()                           # Save information to the database
    return "Handle is {handle}, totalPrice is {totalPrice:.2f}, months to pay is {paymentMonths}, single payer pays {payerPayment:.2f}".format(handle=handle, totalPric=totalPrice, paymentMonths=paymentMonths, payerPayment=payerPayment), 201

    
@app.route("/plans/", methods=["GET"])
def get_inventory():                              # Read the whole database of saved payment plans
    lista = Paymentplan.query.all()        
    jsonifylist = []
    sanakirja = {}
    index = 1
    for x in lista:
        item = Paymentplan.query.get(index)
        jsonifylist.append({
        "handle": item.handle,
        "totalPrice": item.totalPrice,
        "paymentMonths": item.paymentMonths,
        "payerPayment": item.payerPayment
        })
        index = index + 1
    return jsonify(jsonifylist)
    
    
class Paymentplan(db.Model):                               # Model for payment plan
    id = db.Column(db.Integer, primary_key=True)           # plan ID
    handle = db.Column(db.String(50), nullable=False)      # name for the payment plan
    carPrice = db.Column(db.Float, nullable=False)         # price of the car
    downPayment = db.Column(db.Float, nullable=True)       # amount of down payment if any
    no_of_payers = db.Column(db.Integer, nullable=False)   # number of people sharing payment
    paymentMonths = db.Column(db.Integer, nullable=False)  # period of payments
    interestRate = db.Column(db.Float, nullable=False)     # interest for payments
    totalPrice = db.Column(db.Float, nullable=False)       # carPrice + interest
    monthlyPayment = db.Column(db.Float, nullable=False)   # totalPrice / paymentMonths
    payerPayment = db.Column(db.Float, nullable=False)     # monthly payment for each payer
    
    
if __name__ == "__main__":                                 # Create the database
    db.create_all()