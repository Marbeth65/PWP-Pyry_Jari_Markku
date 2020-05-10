from flask import request
from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle, Model
from CICalculator import db
from sqlalchemy.exc import IntegrityError
from CICalculator.utils.hypermedia import CICalcBuilder

class ModelCollection(Resource):
    
    def get(self, handle):
        '''
        listaa kaikki modelit
        '''
        kahva = Handle.query.filter_by(handle=handle).first()
        plans = kahva.models
        list = []
        for x in plans:
            dict = CICalcBuilder({
            "manufacturer": x.manufacturer,
            "model": x.model,
            "year":x.year
            })
            href = "/api/dummyhandle/models/" + x.manufacturer + "/" + x.model + "/" + str(x.year)
            dict.add_control_paymentplan_item(href) # Reusing paymentplan name. This is really model item
            list.append(dict)
            
        response_body = CICalcBuilder({
        "items": list
        })
        response_body.add_control_post_model()
        response_body.add_control_paymentplans_all()
        return response_body, 200
        
    def post(self, handle):
        kahva = Handle.query.filter_by(handle=handle).first()
        try:
            item = Model(
            model=request.json["model"],
            manufacturer=request.json["manufacturer"],
            year=int(request.json["year"])
            )
        except KeyError:
            return "Couldnt find necessary fields", 400
        except ValueError:
            return "year must be integer", 400

        try:        
            db.session.add(item)
            kahva.models.append(item)
            db.session.commit()
        except IntegrityError:
            return "Model already exists", 409
        
        return "Success", 202