from flask_restful import Resource
from CICalculator.models import Handle

'''
Serves as collection of all paymentplans
'''

class PaymentplanCollection(Resource):
    
    def get(self):
        '''
        listaa kaikki paymentplanit
        '''
        list = []
        list.append("toimii")
        return list, 201
    
    def put(self):
        '''
        muokkaa olemassa olevaa paymentplania korvaamalla arvot uusilla
        '''
        list = []
        list.append("toimii")
        return list, 201
        
    def post(self):
        '''
        postaa uuden paymentplanin
        '''
        list = []
        list.append("toimii")
        return list, 201
        
    def delete(self):
        '''
        poistaa handlen ja kaiken siihen liittyvän
        '''
        list = []
        list.append("toimii")
        return list, 201

print("PaymentplanCollection working")