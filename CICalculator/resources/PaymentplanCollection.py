from flask_restful import Resource
from CICalculator.models import Handle

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
                planlist.append({
                    "price":y.price,
                    "provider":y.provider,
                    "interestrate":y.interestrate, 
                    "months":y.months, 
                    "payers":y.payers, 
                    "open":y.open, 
                    "owner_name":y.owner_name})
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
        handle = request.json["handle"]
        name = request.json["name"]
        type = request.json["type"]
        
        Handle.query.filter_by(handle=handle).update({
            "name": name,
            "type": type   
        })
        db.session.commit()
        return "", 201
        
        
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

print("PaymentplanCollection working")