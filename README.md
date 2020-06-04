# PWP-Pyry_Jari_Markku

Steps you need to take in order to run our API and tests.  

1. You have to install our project with "pip install ." command. This should install all of the necessary libraries.(Note! I am not sure if it downloads them. 
I had virtualenv with no libraries on use and it worked afterwards but I am not sure if it downloaded them or searched them from my other enviroments)

2. You have to initialize database with flask command "flask init-db".

3. Before you use our API or client, you will have to submit a handle to it. Our default handle name that 
client supports is called dummyhandle. As of now, there is no resources you can use to submit a handle to the database.
You would have to submit it manually. For testing purposes I have created a flask-click function that populates the database.
This function can be invoked with "flask testgen" -command. This creates 1 handle called dummyhandle, 2 models, 10 paymentplans that are appended
to one of the two models and 5 paymentplans that dont have model yet. 3 of the paymentplans are by default marked as closed.

// Client setup here

After that localhosts /main/ route will take you to the mainpage of our client. There you can modify and add various things to our database. localhosts there is also localhosts /gallery -route that allows you to submit images to be displayed in the site. In order to start adding images with the postImage function you have to first create album. You can do that with the generateAlbum function. This generates new album and stores its values to your localStorage. Then postImage-function automatically adds posted images to that album.  

// Running tests  
  
If you have downloaded our project with pip install command and you have installed python pytest-library and addon pytest-cov you should be able to run all the tests from root folder with terminal comman "pytest". This will run all the tests in "tests"-folder. If you want to see the coverage, you can use the "pytest --cov-report term-missing --cov=CICalculator"-command.
