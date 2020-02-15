The purpose of this document is to make inspection of my code easier.

Both the model for the database and the functions that are used to deal with the database are on the app.py file. The app is designed
so that when you run it as a program from cmd it will create the database. How ever in the folder there is already a populated database
by the name of paymentdatabase.db.

The application allows you to POST payment plans to it (example in the end of this document). These paymentplans are added to the database.

The "handle" value is used later to browse payment plans. If you send a GET-request with name of the handle it will return a json array
with all the paymentplans for that handle as objects.

Our current database has four different handles you can try out: "testhandle1" (3), "pyrynhandle" (2), "jarinhandle" (1) and "uusihandle"(1).
The number after each handle represents the amount of paymentplans with that name, for example GET-request with "testhandle1" returns 3
plans.

POST-requests with approppriate json object go to "/payments/add/" route
GET-requests go to "/plans/<handle>" where handle is the name of the paymentplan

Versions:
  Flask            1.1.1 (tried and working)
  Flask-SQLAlchemy 2.4.1 (tried and working)
  SQLAlchemy       1.3.12 (tried and working)

Example of postable json object:

{
	"handle": "uusihandle",
	"carprice": 2200.0,
	"downpayment": 2140.0,
	"no_of_payers": 1525,
	"paymentmonths": 6,
	"interestrate": 3.5,
	"totalprice": 21115.0,
	"monthlypayment": 115156.5,
	"payerpayment": 14112.7
}


PS. Sorry that this file looks like a mess. For some reason this file lost my carefully planned editing. You can try to read this in edit mode to have it in  a more pleasing form.
