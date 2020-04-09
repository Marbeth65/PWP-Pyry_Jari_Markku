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
        price=1000.0,
        provider="dummyprovider{}".format(x),
        months=6,
        payers=1,
        )
        db.session.add(item)
        db.session.commit()

    # ================================== Tässä laitetaan paymentplanit tuonne handleen =========================================
    
    handle = Handle.query.first()                           # Ottaa ensimmäisen handlen
    paymentplan = Paymentplan.query.first()                 # Ottaa ensimmäisen paymentin
    handle.paymentplans.append(paymentplan)                 # lisää ensimmäisen handlen paymentplaneihin ensimmäisen planin
    paymentplan.open = False                                # muuttaa ensimmäisen planin maksetuksi
    paymentplan2 = Paymentplan.query.get(2)                 # ottaa toisen handlen
    handle.paymentplans.append(paymentplan2)                # laittaa ensimmäiseen handleen uuden planin
    db.session.commit()

    # ==================================== tässä aletaan jo tehdä muita juttuja =================================================
    for x in range(4):
        model = Model(
        manufacturer="dummytoyota-{}".format(x),
        model="dummycorolla-{}".format(x),
        year="200{}".format(x)
        )
        db.session.add(model)
        db.session.commit()

    # ====================================== Täällä ehkä helpoin esimerkki. Handleen laitetaan uusi modeli =======================
    
    
    handle = Handle.query.first()                           # Ottaa ensimmäisen handlen
    model = Model.query.first()                             # Ottaa ensimmäisen modelin
    handle.models.append(model)                             # Tämä on se rivi, joka rekisteröi handlen
    db.session.commit()

# ===================================================================================================================================    
def _get_handle_json():
    return {"handle": "lisähandle", "type": "lisätype", "name": "lisäname"}
    
def _get_model_json():
    return {"manufacturer": "Volkswagen", "model": "jetta", "year": 2016}
    
    
class TestPaymentplanCollection(object):

    RESOURCE_URL = "/api/plans"
    
    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 201
        body = json.loads(resp.data)
        assert len(body) == 2
        
        
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
        

        
        
        
        
        
        
        
        
        
        
