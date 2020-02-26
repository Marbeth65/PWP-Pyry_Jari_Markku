import os
import pytest
import tempfile
from sqlalchemy.exc import IntegrityError

import app
from app import Paymentplan
@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()                                # fd viittaa sanaan FILE DESCRIPTOR!!!!!!!!!!!!!!
    app.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.app.config["TESTING"] = True
    
    with app.app.app_context():
        app.db.create_all()
        
    yield app.db
    
    app.db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)

def test_create_sensor(client):
    ''' 
    Tests that Paymentplan model works
    '''
    plan = app.Paymentplan(
    handle="lolhandle",
    carprice=114.2,
    downpayment=20.2,
    no_of_payers=2,
    paymentmonths=12,
    interestrate=14.0,
    totalprice=43.0,
    monthlypayment=141.0,
    payerpayment=142.1
    )
    
    client.session.add(plan)
    client.session.commit()
    handle = Paymentplan.query.first()
    assert Paymentplan.query.count() == 1
    assert handle.handle == "lolhandle"
    
def test_nullable(client):
    '''
    tests that handle cannot be set to null
    '''
    plan = app.Paymentplan(
    handle=None,
    carprice=114.2,
    downpayment=20.2,
    no_of_payers=2,
    paymentmonths=12,
    interestrate=14.0,
    totalprice=43.0,
    monthlypayment=141.0,
    payerpayment=142.1
    )
    client.session.add(plan)
    with pytest.raises(IntegrityError):
        client.session.commit()

    

    