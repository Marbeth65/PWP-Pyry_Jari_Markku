from flask_restful import Resource
from CICalculator.models import Handle, Paymentplan, Model
from flask import request, url_for
from CICalculator import db
from sqlalchemy.exc import IntegrityError
from CICalculator.utils.hypermedia import CICalcBuilder
'''
Serves as a collection of all paymentplans
'''

class PaymentplanCollection(Resource):
    
    def get(self, handle):
        '''
        lists all paymentplans
        '''
        list = []
        kahva = Handle.query.filter_by(handle=handle).first()
        plans = kahva.paymentplans
        
        for x in plans:
            d = CICalcBuilder({
            "provider": x.provider,
            "price": x.price,
            "months": x.months,
            })
            href = "/api/dummyhandle/plans/" + x.provider + "/" + str(x.price) + "/" + str(x.months) # Not gonna mess with url_for_function
            d.add_control_paymentplan_item(href)
            if x.model_id != None:
                model = Model.query.get(x.model_id)
                d["model"] = model.model
                d["manufacturer"] = model.manufacturer
                d["year"] = model.year
                
            else:
                d["model"] = "No model"
                
            list.append(d)
        
        response_body = CICalcBuilder({
        "items":list
        })
        response_body.add_control_models_all()
        response_body.add_control_paymentplans_open()
        return response_body, 200
           
    
    def put(self, handle):
        '''
        modify existing handle by replacing the values with new ones
        '''
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
            return "Similar plan already exists", 409
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