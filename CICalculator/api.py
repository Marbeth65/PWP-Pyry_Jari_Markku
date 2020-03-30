from flask import Blueprint
from flask_restful import Resource, Api

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

from CICalculator.resources.PaymentplanCollection import PaymentplanCollection

api.add_resource(PaymentplanCollection, "/api")

@api_bp.route("/")
def index():
    return "toimii"
