<<<<<<< HEAD
from flask import request
from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle, Model
from CICalculator import db

class PaymentplanItem(Resource):
    
    def get(self, handle, provider, price, months):
        plan = Paymentplan.query.filter_by(owner_name=handle).filter_by(provider=provider).filter_by(
        price=price).filter_by(months=months).first()
        if plan:
            d = {
            "provider": plan.provider,
            "price": plan.price,
            "months": plan.months,
            "payers": plan.payers,
            "interestrate": plan.interestrate,
            "open": plan.open
            }
            if plan.model_id != None:
                model = Model.query.get(plan.model_id)
                d["model"] = model.model
                d["manufacturer"] = model.manufacturer
                d["year"] = model.year
                
            else:
                d["model"] = "No model"
            return d, 200
        else:
            return "No paymentplan found", 404
            
    def put(self, handle, provider, price, months):
        plan = Paymentplan.query.filter_by(owner_name=handle).filter_by(provider=provider).filter_by(
        price=price).filter_by(months=months).first()
        if plan:
            Paymentplan.query.filter_by(owner_name=handle).filter_by(provider=provider).filter_by(
            price=price).filter_by(months=months).update({"open": not plan.open})
            db.session.commit()
            return "Success", 200
            
        else:
            return "paymentplan not found", 404
            
    def delete(self, handle, provider, price, months):
        plan = Paymentplan.query.filter_by(owner_name=handle).filter_by(provider=provider).filter_by(
        price=price).filter_by(months=months).first()
        if plan:
            db.session.delete(plan)
            db.session.commit()
            return "Success", 204
            
        else:
            return "Plan not found", 404
=======
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
>>>>>>> 6730eb8c65eaf87716484e1e9d5f03b1a1d81a16
