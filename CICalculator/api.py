from flask import Blueprint
from flask_restful import Resource, Api

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

from CICalculator.resources.PaymentplanCollection import PaymentplanCollection
from CICalculator.resources.OpenPaymentplanCollection import OpenPaymentplanCollection
# from CICalculator.resources.ModelCollection import ModelCollection // modeli ei vielä valmis


api.add_resource(PaymentplanCollection, "/api/plans")
api.add_resource(OpenPaymentplanCollection, "/api/plans/open")
#api.add_resource(OpenPaymentplanCollection, "/api/models") tämä on sitten, kun saan noi modelit toimimaan.

@api_bp.route("/")
def index():
    return "toimii"
    
