from flask import request
from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle, Model
from CICalculator import db
from sqlalchemy.exc import IntegrityError

class ModelCollection(Resource):
    
    def get(self, handle):
        '''
        listaa kaikki modelit
        '''
        kahva = Handle.query.filter_by(handle=handle).first()
        plans = kahva.models
        list = []
        for x in plans:
            dict = {
            "manufacturer": x.manufacturer,
            "model": x.model,
            "year":x.year
            }
            list.append(dict)
        return list, 200
        
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