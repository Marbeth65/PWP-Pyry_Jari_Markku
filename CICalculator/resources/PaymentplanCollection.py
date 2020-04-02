from flask_restful import Resource
from CICalculator.models import Handle, Paymentplan

'''
Serves as a collection of all paymentplans
'''

class PaymentplanCollection(Resource):
    
    def get(self):
        '''
        lists all paymentplans
        '''
        list = []
        
        handle = Handle.query.all()
        
        for x in handle:
            plans = x.paymentplans
            planlist = []
            for y in plans:
                planlist.append((y.price,
                                 y.provider,
                                 y.interestrate, 
                                 y.months, 
                                 y.payers, 
                                 y.open, 
                                 y.owner_name))
            list.append({
                "handle":x.handle,
                "name":x.name,
                "type":x.type,
                "plan":planlist
            })
            
        return list, 201
         
        
    
    def put(self):
        '''
        modify existing paymentplan by replacing the values with new ones
        '''
        list = []
        list.append("toimii")
        return list, 201
        
    def post(self):
        '''
        post a new paymentplan
        '''
        list = []
        list.append("toimii")
        return list, 201
        
    def delete(self):
        '''
        deletes a handle and everything related to that handle
        '''
        list = []
        list.append("toimii")
        return list, 201

print("PaymentplanCollection working")