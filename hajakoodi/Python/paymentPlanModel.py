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
    
'''
carPrice0 + interest = total price for the car
totalPrice / paymentMonths = monthly payment
monthlyPayment / no_of_payers = payers' share of the monthly payment
'''