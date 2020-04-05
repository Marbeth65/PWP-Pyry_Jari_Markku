from CICalculator import db
import random
    
class Handle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), nullable=False, unique=True)              # Esim. Pyrynhandle
    name = db.Column(db.String(64), nullable=False)                             # Henkilön tai yrityksen nimi, jolle tämä handle on tehty. Esim. Pyryn Kilpa-Auto (kuvitteellinen autokauppa)
    type = db.Column(db.String(64))  

    paymentplans = db.relationship("Paymentplan", back_populates="handle")
    models = db.relationship("Model", back_populates="handle")
   
class Paymentplan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    provider = db.Column(db.String(64), nullable=False)
    interestrate = db.Column(db.Float)
    months = db.Column(db.Integer, nullable=False)
    payers = db.Column(db.Integer, nullable=False)
    open = db.Column(db.Boolean, default=True)                     
    owner_name = db.Column(db.String(64), db.ForeignKey("handle.handle"))
    model_name = db.Column(db.String(64), db.ForeignKey("model.model"))
    
    handle = db.relationship("Handle", back_populates="paymentplans")
    model = db.relationship("Model", back_populates="paymentplans")
    
class Model(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(64), nullable=False)
    model = db.Column(db.String(64), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    owner_name = db.Column(db.String(64), db.ForeignKey("handle.handle"))
    
    handle = db.relationship("Handle", back_populates="models")    
    paymentplans = db.relationship("Paymentplan", back_populates="model")
    
import click
from flask.cli import with_appcontext

@click.command("init-db")
@with_appcontext
def init_db_command():
    db.create_all()
    print("database created")
    
@click.command("populate-handle")
@with_appcontext
@click.argument("handle")
def populate_handle_command(handle):
    item = Handle(
    handle=handle,
    name="dummyname",
    type="dummytype"
    )
    db.session.add(item)
    db.session.commit()
    print("populated " + handle)
    
@click.command("populate-plans")
@with_appcontext
@click.argument("lkm", type=int)
def populate_plans_command(lkm):
    for x in range(lkm):
        item = Paymentplan(
        price = 1000.0,
        provider = "dummyprovider{}".format(x),
        interestrate = 0.0,
        months = 1,
        payers = 1,
        )
        db.session.add(item)
        db.session.commit()
        print("Luku on " + str(lkm) + " ja kierros on" + str(x))