from flask import request, abort
from flask_restful import Resource
from CICalculator.models import Paymentplan, Handle, Model
from CICalculator import db
from CICalculator.utils.hypermedia import CICalcBuilder

class ModelItem(Resource):
    
    def get(self, handle, manufacturer, model, year):
        
        model = Model.query.filter_by(manufacturer=manufacturer).filter_by(model=model).filter_by(year=year).filter_by(owner_name=handle).first()
        if model:
            paymentplans = []
            for x in model.paymentplans:
                paymentplans.append(x.provider)
            dict = CICalcBuilder({
            "model": model.model,
            "year": model.year,
            "manufacturer": model.manufacturer,
            "handle-name": model.owner_name,
            "paymentplans": paymentplans
            })
            dict.add_control_models_all()
            url = "/api/dummyhandle/models/" + model.manufacturer + "/" + model.model + "/" + str(model.year)
            dict.add_control_append_plan(url)
            return dict, 200
            
        else:
            return "No model found", 404
        
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
        return "", 204
        
    def delete(self, handle, manufacturer, model, year):
        
        model = Model.query.filter_by(manufacturer=manufacturer).filter_by(model=model).filter_by(year=year).filter_by(owner_name=handle).first()
        db.session.delete(model)
        db.session.commit()
        return "", 204
        
    def post(self, handle, manufacturer, model, year):
        
        ''' posts a new paymentplan to the model '''
        
        model = Model.query.filter_by(manufacturer=manufacturer).filter_by(model=model).filter_by(year=year).filter_by(owner_name=handle).first()
        if model:
            try:
                paymentplan_provider = request.json["paymentplan_provider"]
                paymentplan_price = float(request.json["paymentplan_price"])
                paymentplan_months = int(request.json["paymentplan_months"])
            except ValueError:
                return "Paymentplan price and months must be numbers", 400
            plan = Paymentplan.query.filter_by(owner_name=handle).filter_by(provider=paymentplan_provider).filter_by(
            price=paymentplan_price).filter_by(months=paymentplan_months).first()
            
            model.paymentplans.append(plan)
            db.session.commit()
            return "Added", 201
        else:
            return "Model not found", 404
        
        
