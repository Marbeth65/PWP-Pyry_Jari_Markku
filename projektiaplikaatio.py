from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc

'''
Tämä on flask-applikaatio, joka sekä ottaa vastaan että lähettää viestejä. Tuo add_product funktio ottaa vastaan application/json-tyyppistä dataa muodossa, josta esimerkkejä toisessa tiedostossa.
Testausta varten teidän pitää ensin suorittaa ohjelma kertaalleen, niin kansioonne ilmestyy tietokantana toimiva "maksudatabase.db"-tiedosto. Sen jälkeen teidän pitää asettaa tämän tiedoston nimi komennolla
set FLASK_APP=projektiaplikaatio (tuo windowsilla, saatatte joutua käyttämään erilaista komentoa eri käyttöjärjestelmällä).

Sitten voitte käynnistää serverin ja lähettää sille GET- ja POST-pyyntöjä vaikkapa tuolla kurssilla esitellyllä Talend API Tester -chromelaajennuksella, jonka käyttöön ohjeistusta löytyy kurssin lovelace-sivulta osiosta
"Testing Flask applications".
'''
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///maksudatabase.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    return "Indeksisivu"
    
@app.route("/products/add/", methods=["POST"])
def add_product():                                      # Tällä funktiolla tallennetaan databaseen maksusuunnitelma.
    handle = request.json["handle"]                     # Tämä on maksun nimi, jolla tunnistetaan maksut
    kokohinta = request.json["kokohinta"]               # Tämä on maksun kokonaishinta, josta tämä ohjelma laskee osamaksun raakaversion, ilman mitään korkoja yms.
    periodit = request.json["periodit"]                 # Tämä on maksujen lukumäärä, eli monellekko kuukaudelle maksu sijoittuu
    osahinta = kokohinta / periodit                     # Tässä on laskettu yhden kuukauden hinta hyvin yksinkertaisella periaatteella. Tämä vaan mallin vuoksi
    Suunnitelma = Maksusuunnitelma(
    handle=handle,
    kokohinta=kokohinta,
    periodit=periodit,
    osahinta=osahinta
    )
    db.session.add(Suunnitelma)                     
    db.session.commit()                                 # Tässä maksu lähetetään databaseen "maksudatabase.db".
    return "Handle on {handle}, kokonaishinta on {kokohinta:.2f}, periodeja on {periodit}, yksittäisen erän hinta on {osahinta:.2f}".format(handle=handle, kokohinta=kokohinta, periodit=periodit, osahinta=osahinta), 201
    
@app.route("/storage/", methods=["GET"])
def get_inventory():                                    # Tämä funktio lähettää takaisin maksut tietokannasta. Toistaiseksi se lähettää kaikki maksut kahvasta huolimatta, mutta sen voi muuttaa varsin helposti sitten lopulliseen
    lista = Maksusuunnitelma.query.all()                # versioon
    jsonifylista = []
    sanakirja = {}
    indeksi = 1
    for x in lista:
        alkio = Maksusuunnitelma.query.get(indeksi)
        jsonifylista.append({
        "handle": alkio.handle,
        "kokohinta": alkio.kokohinta,
        "periodut": alkio.periodit,
        "osahinta": alkio.osahinta
        })
        indeksi = indeksi + 1
    return jsonify(jsonifylista)
    
class Maksusuunnitelma(db.Model):                       # Tässä yhden maksun muotti
    id = db.Column(db.Integer, primary_key=True)
    handle = db.Column(db.String(50), unique=True, nullable=False)
    kokohinta = db.Column(db.Float, nullable=False)
    osahinta = db.Column(db.Float, nullable=False)
    periodit = db.Column(db.Integer, nullable=False)

if __name__ == "__main__":                              # Kun suoritatte ohjelman komentoriviltä, tämä vain luo tuon yllä olevan muotin.
    db.create_all()