from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle

class OpenPaymentplanCollection(Resource):
    
    def get(self, handle):
        '''
        listaa kaikki avoimet paymentplanit yhdelle handlelle
        '''
        kahva = Handle.query.filter_by(handle=handle).first()
        plans = kahva.paymentplans
        list = []
        for x in plans:
            if x.open:
                dict = {
                "price": x.price,
                "provider":x.provider,
                "open": x.open
                }
                list.append(dict)
            else:
                pass
        return list, 200
        
    