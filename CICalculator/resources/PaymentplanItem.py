from flask_restful import Resource
from CICalculator.models import Handle, Paymentplan, Model, db

'''
Serves as a collection of all paymentplans
'''

class PaymentplanItem(Resource):
    
    def get(self, handle):
        '''
        lists all paymentplans
        '''
        lista = []
        
        handle = request.json["handle"]
        item = Handle.query.filter_by(handle=handle).first()
        paymentplan = Paymentplan.query.filter_by(handle=handle).first()
        lista.append({
            "handle":handle.handle,
            "name":handle.name,
            "type":handle.type,
            "price":paymentplan.price,
            "provider":paymentplan.provider,
            "interestrate":paymentplan.interestrate,
            "months":paymentplan.months,
            "payers":paymentplan.payers,
            "open":paymentplan.open
        })
        db.session.commit()
        
        return lista, 201
           
    
    def put(self):
        '''
        modify existing paymentplan by replacing the values with new ones
        '''
        pass
        
        
    def post(self):
        '''
        post a new paymentplan
        '''
        
        if not request.json:
            abort(415)
            
        try:
            item = Handle(
                handle=request.json["handle"],
                name=request.json["name"],
                type=request.json["type"],
            )
            db.session.add(item)
            db.session.commit()
        except KeyError:
            abort(400)
        except IntegrityError:
            abort(409)
        
        return "", 201

        
    def delete(self):
        '''
        deletes a handle and everything related to that handle
        '''
        handle = request.json["handle"]
        item = Handle.query.filter_by(handle=handle).first()
        db.session.delete(item)
        db.session.commit()

        return "", 201

print("PaymentplanItem working")
