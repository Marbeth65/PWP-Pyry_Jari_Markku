from flask_restful import Resource
<<<<<<< HEAD
from CICalculator.models import Handle, Paymentplan, Model
from flask import request
from CICalculator import db
from sqlalchemy.exc import IntegrityError
=======
from CICalculator.models import Handle, Paymentplan, Model, db

>>>>>>> 6730eb8c65eaf87716484e1e9d5f03b1a1d81a16
'''
Serves as a collection of all paymentplans
'''

class PaymentplanCollection(Resource):
    
    def get(self, handle):
        '''
        lists all paymentplans
        '''
<<<<<<< HEAD
        list = []
        kahva = Handle.query.filter_by(handle=handle).first()
        plans = kahva.paymentplans
        
        for x in plans:
            d = {
            "provider": x.provider,
            "price": x.price,
            "months": x.months,
            }
            if x.model_id != None:
                model = Model.query.get(x.model_id)
                d["model"] = model.model
                d["manufacturer"] = model.manufacturer
                d["year"] = model.year
                
            else:
                d["model"] = "No model"
                
            list.append(d)
        
        return list, 200
=======
        lista = []
        
        count = Handle.query.count()

        for i in range(1, count+1):
            handle = Handle.query.get(i)
            paymentplan = Paymentplan.query.get(i)
            model = Model.query.get(i)
            lista.append({
                "handle":handle.handle,
                "name":handle.name,
                "type":handle.type,
                "price":paymentplan.price,
                "provider":paymentplan.provider,
                "interestrate":paymentplan.interestrate,
                "months":paymentplan.months,
                "payers":paymentplan.payers,
                "open":paymentplan.open,
                "manufacturer":model.manufacturer,
                "model":model.model,
                "year":model.year
                })
            db.session.commit()
        
        return lista, 201
>>>>>>> 6730eb8c65eaf87716484e1e9d5f03b1a1d81a16
           
    
    def put(self, handle):
        '''
        modify existing handle by replacing the values with new ones
        '''
<<<<<<< HEAD
        handle = handle
        try:
            name = request.json["name"]
            type = request.json["type"]
        except KeyError:
            return "Invalid request - missing fields", 400
        Handle.query.filter_by(handle=handle).update({
            "name": name,
            "type": type   
        })
        db.session.commit()
        return "", 200
=======
        pass
>>>>>>> 6730eb8c65eaf87716484e1e9d5f03b1a1d81a16
        
        
    def post(self, handle):
        '''
        post a new paymentplan
        '''
        handle = Handle.query.filter_by(handle=handle).first()
        try:
            item = Paymentplan(
            price = request.json["price"],
            provider = request.json["provider"],
            months = request.json["months"],
            payers = request.json["payers"],
            )
        except KeyError:
            return "Invalid request - missing keys", 400
        if "interestrate" in request.json:
            item.interestrate = request.json["interestrate"]
        
        try:
            db.session.add(item)
            handle.paymentplans.append(item)
            db.session.commit()
        except IntegrityError:
            return "Similart plan already exists", 409
        return "", 201

        
    def delete(self, handle):
        '''
        deletes the handle
        '''
        item = Handle.query.filter_by(handle=handle).first()
        db.session.delete(item)
        db.session.commit()

        return "", 204

print("PaymentplanCollection working")