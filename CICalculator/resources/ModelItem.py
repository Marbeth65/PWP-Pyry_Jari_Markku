from flask import request
from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle, Model
from CICalculator import db

class ModelItem(Resource):
    
    def get(self, handle, manufacturer, model, year):
        
        list = []
        model = Model.query.filter_by(manufacturer=manufacturer).filter_by(model=model).filter_by(year=year).filter_by(owner_name=handle).first()
        dict = {
        "model": model.model,
        "year": model.year,
        "manufacturer": model.manufacturer,
        "paymentplan-name": model.owner_name
        }
        list.append(dict)
        return list, 201
        
    def put(self, handle, manufacturer, model, year):
        ''' modifies but doesnt add new handle or paymentplan yet '''
        newmodel = request.json["model"]
        newmanufacturer = request.json["manufacturer"]
        newyear = request.json["year"]
        model = Model.query.filter_by(manufacturer=manufacturer).filter_by(model=model).filter_by(year=year).filter_by(owner_name=handle).update({
        "model": newmodel,
        "manufacturer": newmanufacturer,
        "year": newyear,
        })
        db.session.commit()
        
    def delete(self, handle, manufacturer, model, year):
        
        model = Model.query.filter_by(manufacturer=manufacturer).filter_by(model=model).filter_by(year=year).filter_by(owner_name=handle).first()
        db.session.delete(model)
        db.session.commit()
        
