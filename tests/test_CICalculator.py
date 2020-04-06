import pytest
import tempfile
import os

from CICalculator import create_app, db
from CICalculator.models import  Handle, Paymentplan

@pytest.fixture
def app():
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
    
    yield app
    
    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
    print("Lopetus")
    

def test_testeri(app):
    paymentplans = Paymentplan.query.count()
    handles = Handle.query.count()
    assert handles == 2
    assert paymentplans == 4
    
    
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
        provider="dummyprovider",
        months=6,
        payers=1,
        )
        db.session.add(item)
        db.session.commit()
    print("Populated")
    
