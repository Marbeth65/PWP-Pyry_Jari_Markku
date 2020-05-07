from flask import Blueprint
from flask_restful import Resource, Api

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

from CICalculator.resources.PaymentplanCollection import PaymentplanCollection
from CICalculator.resources.OpenPaymentplanCollection import OpenPaymentplanCollection
from CICalculator.resources.ModelCollection import ModelCollection
from CICalculator.resources.ModelItem import ModelItem
from CICalculator.resources.PaymentplanItem import PaymentplanItem

api.add_resource(PaymentplanCollection, "/api/<handle>/plans")
api.add_resource(OpenPaymentplanCollection, "/api/<handle>/plans/open")
api.add_resource(ModelCollection, "/api/<handle>/models")
api.add_resource(ModelItem, "/api/<handle>/models/<manufacturer>/<model>/<year>")
api.add_resource(PaymentplanItem, "/api/<handle>/plans/<provider>/<price>/<months>")

@api_bp.route("/")
def index():
    return "toimii"
    
