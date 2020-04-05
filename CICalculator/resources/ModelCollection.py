from flask import request
from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle, Model
from CICalculator import db

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
        return list, 201
        
    def post(self, handle):
        item = Model(
        model=request.json["model"],
        manufacturer=request.json["manufacturer"],
        year=request.json["year"]
        )
        db.session.add(item)
        db.session.commit()
