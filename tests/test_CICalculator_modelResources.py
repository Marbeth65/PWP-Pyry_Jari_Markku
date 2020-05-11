import pytest
import tempfile
import os
import random
import json

from CICalculator import create_app, db
from CICalculator.models import  Handle, Paymentplan, Model
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def client():
    print("")
    print("Aloitus")
    
    db_fd, db_fname = tempfile.mkstemp()
    config = {
    "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
    "TESTING": True
    }
    
    app = create_app(config)
    
    app.app_context().push()
    db.create_all()
    
    _populate_db()
    
    yield app.test_client()
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
    print("Lopetus")
    
def _get_model():
    return {"model": "compact", "manufacturer": "BMW", "year": 2000}

    
def _populate_db():
    item = Handle(
    handle="dummyhandle",
    name="dummyname",
    type="dummytype"
    )
    db.session.add(item)
    db.session.commit()
    
    handle = Handle.query.first()
    
    for x in range(15):
        item = Paymentplan(
        price = 1000.0,
        provider = "dummyprovider-{}".format(x),
        interestrate = 0.0,
        months = 1,
        payers = 1
        )
        if x == 3 or x == 9 or x == 12:
            item.open = False
        db.session.add(item)
        handle.paymentplans.append(item)        
        
    db.session.commit()
    
    item = Model(
    manufacturer = "Toyota",
    model = "Corolla",
    year = 2007
    )
    handle.models.append(item)
    db.session.add(item)
    db.session.commit()
    
    item = Model(
    manufacturer = "Volkswagen",
    model = "Jetta",
    year = 2009
    )
    handle.models.append(item)
    db.session.add(item)
    db.session.commit()
    
    for x in range(1, 6):
        model = Model.query.first()
        plan = Paymentplan.query.get(x)
        model.paymentplans.append(plan)
        db.session.commit()
             
    for x in range(6, 11):
        model = Model.query.get(2)
        plan = Paymentplan.query.get(x)
        model.paymentplans.append(plan)
        db.session.commit()

def test_model_unique(client):
    ''' Tests that you cannot submit two similar models'''
    
    item = Model(
    manufacturer = "Volkswagen",
    model = "Jetta",
    year = 2009
    )
    db.session.add(item)
    with pytest.raises(IntegrityError):
        db.session.commit()
        
def test_paymentplan_unique(client):
    ''' Tests that you cant submit two similar paymentplans '''
    
    item = Paymentplan(
    price=1000.0,
    provider="uniqueprov",
    payers=1,
    months=1
    )
    db.session.add(item)
    db.session.commit()
    item = Paymentplan(
    price=1000.0,
    provider="uniqueprov",
    payers=1,
    months=1,
    interestrate=1.23
    )
    db.session.add(item)
    with pytest.raises(IntegrityError):
        db.session.commit()    

class TestModelItem(object):

    RESOURCE_URL = "/api/dummyhandle/models/Toyota/Corolla/2007"
    PAYMENTPLAN_URL = "/api/dummyhandle/plans/dummyprovider-12/1000.0/1"
    WRONG_RESOURCE_URL = "/api/dummyhandle/models/Toyota/Corolla/2010"
    MODIFIED_URL = "/api/dummyhandle/models/BMW/compact/2000"
    
    def test_get(self, client):
        # tests that get request is valid
    
        resp = client.get(self.RESOURCE_URL)
        body = json.loads(resp.data)
        assert resp.status_code == 200
        
    def test_post(self, client):
        # Tests that posting to model works
        valid = {"paymentplan_price":1000.0, "paymentplan_provider":"dummyprovider-0", "paymentplan_months":1}
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        
        # Tests that invalid numeral value throws 400 error
        unvalid = {"paymentplan_price":1000.0, "paymentplan_provider":"dummyprovider-0", "paymentplan_months":"asd"}
        resp = client.post(self.RESOURCE_URL, json=unvalid)
        print(resp.status_code)
        assert resp.status_code == 400
        
        # Tests that appending to model works. gets payment with no model appended
        resp = client.get(self.PAYMENTPLAN_URL)
        body = json.loads(resp.data)
        assert body["model"] == "No model"
        
        valid = {"paymentplan_price":1000.0, "paymentplan_provider":"dummyprovider-12", "paymentplan_months":1} # paymentplan to be appended to request body
        resp = client.post(self.RESOURCE_URL, json=valid)
        
        resp = client.get(self.PAYMENTPLAN_URL)
        body = json.loads(resp.data)                # Now paymentplan shows appended model in its model slots.
        assert body["model"] == "Corolla"
        assert body["manufacturer"] == "Toyota"
        
        resp = client.post(self.WRONG_RESOURCE_URL, json=valid)
        assert resp.status_code == 404
        
    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 204  # Tests that code is right
        
        resp = client.get(self.RESOURCE_URL)
        body = json.loads(resp.data)    # Assures that URL of the item vanished after delete leading to 404 error
        assert resp.status_code == 404 

    def test_put(self, client):
        # Tests that model is modified by put. Correct URL vanishes after edit.
        
        valid = _get_model()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 204
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404 # After modification changes the url is also modified meaning that RESOURCE_URL no longer works
        
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
              
        
class TestModelCollection(object):
    
    RESOURCE_URL = "/api/dummyhandle/models"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        assert len(body) == 2 # Populate_db creates two models so correct lenght is 2
        
    def test_post(self, client):
        valid = _get_model()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 202
        
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        
        body = json.loads(resp.data)
        assert len(body) == 3 # Populate_db creates two models so correct lenght is 2
        
        new = body[2]
        assert new["manufacturer"] == "BMW"
        assert new["model"] == "compact"
        
    def test_post_400_error(self, client):
        unvalid = {"petteri": "lol"}
        resp = client.post(self.RESOURCE_URL, json=unvalid)
        assert resp.status_code == 400                      # Tests that missing keys result to 400 error
        
        unvalid = _get_model()
        unvalid["year"] = "asd"
        resp = client.post(self.RESOURCE_URL, json=unvalid)
        assert resp.status_code == 400                      # Tests that invalid integer results to 400 error
    
    def test_integrityError(self, client):
        duplicate = {"manufacturer":"Toyota", "model":"Corolla", "year": 2007} # Tests that posting duplicate model results to 409 error
        resp = client.post(self.RESOURCE_URL, json=duplicate)
        assert resp.status_code == 409

        
        
        
        
        
        
        
        
        
        
        
        
