import pytest
import tempfile
import os
import json

from sqlalchemy.exc import IntegrityError

from CICalculator import create_app, db
from CICalculator.models import  Handle, Paymentplan, Model
from CICalculator.resources import PaymentplanCollection

@pytest.fixture
def client():
    print("")
    
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

def _populate_db():
    for x in range(2):
        item = Handle(
        handle="asd{}".format(x),
        name="lol{}".format(x)
        )
        db.session.add(item)
        db.session.commit()
        
    for x in range(4):
        item = Paymentplan(
        price= 1000.0,
        provider="dummyprovider{}".format(x),
        months=6,
        payers=1,
        )
        db.session.add(item)
        db.session.commit()
        
    handle = Handle.query.first()                           # Ottaa ensimmäisen handlen
    paymentplan = Paymentplan.query.first()                 # Ottaa ensimmäisen paymentin
    handle.paymentplans.append(paymentplan)                 # lisää ensimmäisen handlen paymentplaneihin ensimmäisen planin
    paymentplan.open = False                                # muuttaa ensimmäisen planin maksetuksi
    paymentplan2 = Paymentplan.query.get(2)                 # ottaa toisen handlen
    handle.paymentplans.append(paymentplan2)                # laittaa ensimmäiseen handleen uuden planin
    db.session.commit()

    for x in range(4):
        model = Model(
        manufacturer="dummytoyota-{}".format(x),
        model="dummycorolla-{}".format(x),
        year="200{}".format(x)
        )
        db.session.add(model)
        db.session.commit()
        
    handle = Handle.query.first()                           # Ottaa ensimmäisen handlen
    model = Model.query.first()                             # Ottaa ensimmäisen modelin
    paymentplan = Paymentplan.query.first()                 # Ottaa ensimmäisen paymentplanin
    handle.models.append(model)
    model.paymentplans.append(paymentplan)
    db.session.commit()
    
    
def _get_handle_json():
    return {"handle": "lisähandle", "type": "lisätype", "name": "lisäname"}
    
def _get_model_json():
    return {"manufacturer": "Volkswagen", "model": "jetta", "year": 2016}
    
def _get_paymentplan_json():
    return {"price":500, "months": 5, "payers": 2, "provider": "Jussin Auto", "interestrate": 0.05, "open": True}
    
    
class TestPaymentplanCollection(object):

    RESOURCE_URL = "/api/asd0/plans"
    
    def test_get(self, client):
        plans = Paymentplan.query.all()
        print(len(plans))
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 201
        body = json.loads(resp.data)
        assert len(body) == 2
        
        
    def test_post(self, client):
        valid = _get_paymentplan_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        plans = Paymentplan.query.all()
        assert len(plans) == 5
        plan = Paymentplan.query.get(5)
        assert plan.provider == "Jussin Auto"
        assert plan.owner_name == "asd0"
        
class TestOpenPaymentplanCollection(object):

    RESOURCE_URL = "/api/asd0/plans/open"
    
    def test_get(self, client):
        """ Tests that get requests return open paymentplans """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 201
        body = json.loads(resp.data)
        for x in body:
            assert open

class TestModelCollection(object):
    
    RESOURCE_URL = "/api/asd0/models"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 201
        body = json.loads(resp.data)
        
    def test_post(self, client):
        valid = _get_model_json()
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        len = Model.query.count()
        assert len == 5
        
class TestModelItem(object):
    
    RESOURCE_URL = "/api/asd0/models/dummytoyota-0/dummycorolla-0/2000"    
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 201
        body = json.loads(resp.data)
        
        
    def test_put(self, client):
        valid = _get_model_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 200

    def test_delete(self, client):
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 200
        len = Model.query.count()
        assert len == 3
        
    def test_post(self, client):
        valid = {"id": 3}
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        
class TestPaymentplanItem(object):

    RESOURCE_URL = "/api/asd0/plans/1000.0/dummyprovider0/6/1/"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 201
        body = json.loads(resp.data)
        print(body)
        
def test_unique_models(client):
    model = Model(
    manufacturer="dummytoyota-0",
    model="dummycorolla-0",
    year="2000"
    )
    db.session.add(model)
    with pytest.raises(IntegrityError):
        db.session.commit()
        
def test_append_to_handle(client):
    handle = Handle.query.first()
    paymentplan = Paymentplan.query.first()
    model = Model.query.first()
    
    handle.paymentplans.append(paymentplan)
    handle.models.append(model)
    db.session.commit()
    
def test_append_to_paymentplan(client):
    handle = Handle.query.first()
    paymentplan = Paymentplan.query.first()
    model = Model.query.first()

    #paymentplan.model.append(model)                Ei toimi!
    #paymentplan.handle.append(handle)
    
def test_append_to_model(client):
    paymentplan = Paymentplan.query.get(2)
    model = Model.query.first()

    model.paymentplans.append(paymentplan)
    db.session.commit()
    
    assert len(model.paymentplans) == 2
        
def test_paymentplan_model_one_to_one(client):
    payment = Paymentplan.query.first()
    model = Model.query.get(2)
    model.paymentplans.append(payment)
    db.session.commit()
        
        
        
        
 








 