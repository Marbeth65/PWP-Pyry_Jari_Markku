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

    __table_args__ = (db.UniqueConstraint("price", "provider", "months", name="paymentplan_unique"), )
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    provider = db.Column(db.String(64), nullable=False)
    interestrate = db.Column(db.Float)
    months = db.Column(db.Integer, nullable=False)
    payers = db.Column(db.Integer, nullable=False)
    open = db.Column(db.Boolean, default=True)    

    # Foreign keys
    
    owner_name = db.Column(db.String(64), db.ForeignKey("handle.handle"))   
    model_id = db.Column(db.String(64), db.ForeignKey("model.id"))
    
    handle = db.relationship("Handle", back_populates="paymentplans")
    model = db.relationship("Model", back_populates="paymentplans", uselist=False)
    
class Model(db.Model):
    
    __table_args__ = (db.UniqueConstraint("manufacturer", "model", "year", name="model_unique"), )

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
def init_db_command():                                  # pragma: no cover
    db.create_all()
    print("database created")
    
@click.command("populate-handle")                       # pragma: no cover
@with_appcontext
@click.argument("handle")
def populate_handle_command(handle):                    # pragma: no cover
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
def populate_plans_command(lkm):                        # pragma: no cover
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
        
@click.command("testgen")
@with_appcontext
def generate_dummy():
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
        price = (1000.0 + random.randrange(1000)),
        provider = "dummyprovider-{}".format(x),
        interestrate = 0.0 + (random.random() * 30),
        months = 1 + (random.randrange(6)),
        payers = 1 + (random.randrange(3))
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
        
    print("Generated dummy data")
    
    
    
    
    
    
    
    
    
    
    