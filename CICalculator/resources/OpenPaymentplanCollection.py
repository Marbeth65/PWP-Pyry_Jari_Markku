from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle
from CICalculator.utils.hypermedia import CICalcBuilder

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
                dict = CICalcBuilder({
                "price": x.price,
                "provider":x.provider,
                "months": x.months,
                "open": x.open
                })
                href = "/api/dummyhandle/plans/" + x.provider + "/" + str(x.price) + "/" + str(x.months)
                dict.add_control_paymentplan_item(href)
                list.append(dict)
            else:
                pass
                
        response_body = CICalcBuilder({
        "items": list
        })
        response_body.add_control_paymentplans_all()
        
        return response_body, 200
        
    