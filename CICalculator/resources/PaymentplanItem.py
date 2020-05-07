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
