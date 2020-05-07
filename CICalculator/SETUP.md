This is a file that is supposed to help testing and using our API.

From external libraries you need Flask and SQLalchemy.

Our API name is CICalculator so in order to test it you will have to locate to the directory in which the API is located and change flask application name with cmd command "set_FLASK_APP=CICalculator". In order to run tests you are going to have pytest installed and you have to also install our application to your pip directory with the setup file by typing "pip install -e ."

Before running manual tests you should first initialize and populate database. Initializing database is done with "flask init-db"-command.
For populating the database you can use designed click-functions in the models.py-file. "flask testgen" -command will populate database with enough dummy data to test all parts of our application. Unlike the wiki says, I dont have populated database in my repo. Thats because the database I used got really messy after I tried out various parts of my program and just generating and populating a new database is so easy.

