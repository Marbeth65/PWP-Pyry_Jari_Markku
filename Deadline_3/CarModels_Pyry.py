'''
Minun ehdottamani rakenne on kolmiportainen, Handlet sisältävät paymentplaneja, jotka sisältävät automalleja (carModel).
Handlen tarkoitus on vain eritellä maksuja. Esim. jokin yritys tai yksityishenkilö voi tehdä itselleen handlen, jonne voi sitten tallentaa
maksusuunnitelmia.

Maksusuunnitelmat ovat varmaan ika itsestäänselviä. Tässä variaatiossa olen kuitenkin laittanut maksusuunnitelmaan vain ns. syötettävät arvot,
muut arvot voi sitten clientti laskea niistä. Olen myös jättänyt downpaymentin pois, mutta sen voi lisätä, jos tarvitsee.

Car modelista olen laittanut valmistajan, mallin ja vuoden. Tarkoitus on, että yhdessä maksusopimuksessa voi olla vain yksi automalli. 

HUOM! KYSEISIÄ MALLEJA EI OLE TESTATTU, NE OVAT VAAN SUUNNITTELUUN. SAATTAA OLLA VIRHEITÄ.


'''








class Handle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(64), nullable=False, unique=True)              # Esim. Pyrynhandle
    name = db.Column(db.String(64), nullable=False)                             # Henkilön tai yrityksen nimi, jolle tämä handle on tehty. Esim. Pyryn Kilpa-Auto (kuvitteellinen autokauppa)
    type = db.Column(db.String(64))                                             # Vapaasti määriteltävä yritystyyppi tai yksityishenkilö. Esim. Car Store.
    
    paymentplans = db.relationship("Paymentplan", back_populates="handle")      # Tämän handlen paymentplanit


class Paymentplan(db.Model):                                                    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    interestrate = db.Column(db.Float)
    months = db.Column(db.Integer, nullable=False)
    payers = db.Column(db.Integer, nullable=False)
    open = db.Column(db.Boolean, default=True)                                  # Onko maksu maksettu, defaulttina se on "auki".
    
    handle = db.relationship("Handle", back_populates="paymentplans")           # Tämän planin handle
    carmodel = db.relationship("CarModel", back_populates="plans")               # Tämän planin malli
    


    
class CarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)                                
    manufacturer = db.Column(db.String(64), nullable=False)                     # Esim. Toyota
    model = db.Column(db.String(64), nullable=False)                            # Esim. Corolla Touring Sports 2.0 Hybrid
    year = db.Column(db.Integer)                                                # Esim. 2020
    
    plans = db.relationship("Paymentplan", back_populates="carmodel")           # tämän mallin planit