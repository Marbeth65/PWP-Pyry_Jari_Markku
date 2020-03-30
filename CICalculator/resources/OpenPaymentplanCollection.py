from flask_restful import Resource
from CICalculator.models import Paymentplan

class OpenPaymentplanCollection(Resource):
    
    def get(self):
        '''
        listaa kaikki avoimet paymentplanit
        '''
        list = []
        list.append("toimii")
        return list, 201
        
    