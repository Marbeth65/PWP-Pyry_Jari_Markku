from flask import url_for

''' Hypermedia controls to "dummyhandle". MasonBuilder is taken and modified from 

    https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/implementing-rest-apis-with-flask/#generating-hypermedia
 '''

class MasonBuilder(dict):

    def add_control(self, control_name, href, **kwargs):
    
        if "@controls" not in self:
            self["@controls"] = {}
            
        self["@controls"][control_name] = kwargs
        self["@controls"][control_name]["href"] = href
        
        if "@namespaces" not in self:
            self["@namespaces"] = {                             # This should add namespace automatically
            "cicalc": "/CICalculator/link-relations/#"           
            }
        
    
class PaymentCollectionBuilder(MasonBuilder):
    pass

        
class CICalcBuilder(MasonBuilder):
    
    @staticmethod
    def generate_model_schema():
        schema = {
        "type": "object",
        "required": ["manufacturer", "model", "year"]
        }
        
        properties = schema["properties"] = {}
        
        properties["manufacturer"] = {
            "type": "string",
            "description": "manufacturer of model"
        }
        
        properties["model"] = {
            "type": "string"
        }
        
        properties["year"] = {
            "type": "number"
        }
        return schema
        
    @staticmethod
    def generate_payment_post_schema():
        schema = {
        "type": "object",
        "required": ["provider", "price", "months"]
        }
        
        properties = schema["properties"] = {}
        
        properties["provider"] = {
        "type": "string"
        }
        properties["price"] = {
        "type": "number"
        }
        
        properties["months"] = {
        "type": "number"
        }
        
        return schema
    
    def add_control_toggle(self, url):
    
        self.add_control("cicalc:toggle", url, method="PUT", description="Toggles plans open-field")
        
    def add_control_paymentplans_all(self):
        self.add_control("cicalc:plans-all", "/api/dummyhandle/plans", method="GET")
        
    def add_control_paymentplan_item(self, href):
    
        self.add_control("self", href, method="GET")
        
    def add_control_models_all(self):
    
        self.add_control("cicalc:models-all", "/api/dummyhandle/models", method="GET")
        
    def add_control_paymentplans_open(self):
        
        self.add_control("cicalc:plans-open", "/api/dummyhandle/plans/open", method="GET")

    def add_control_post_model(self):
        
        self.add_control("cicalc:add-model", "/api/dummyhandle/models", method="POST", schema=self.generate_model_schema())
        
    def add_control_append_plan(self, url):
        
        self.add_control("cicalc:append-plan", url, method="POST", schema=self.generate_payment_post_schema())
        
    def add_control_asso(self, url):
    
        self. add_control("cicalc:asso", url, method="GET")

    