HOW TO USE:
--------------------------------------------------------------
Please ensure you install all required dependencies prior to using this program.
--------------------------------------------------------------
The "assets" folder for running main.py. main.py is a python file that trains the ML model with photos in the train folder. It will then iterate through the validate folder which contains a bunch of randomized test images to test itself which will provide an accuracy score as well as a confusion matrix graph. 

To use the program, upload different categories of images as different folder under the "train" folder. These images will be used to train the model into understanding the features of each category. The folder should already have empty folders that serve as an example of what this process may look like when its finished. Under each of these category folders, you may upload anything that is similar to the category. For example, the "dog" folder should contain pictures of dogs. 

The validate folder should contain category folders that contain identical names as the folders you created under assets/train. However, these folders should examples that are different from the ones chosen in  assets/train, allowing the model to test itself. 

The "assets1" folder is used for running server.py, which is the backend flask server used to connect the front end functionality with. You'll notice that the assets1 folder also contains a train and validate folder. In the train folder, follow the same process described for the "assets" folder. However, leave the validate folder empty as the files the user will upload in the frontend will be uploaded into assets1/validate/user for the program to use. 

To initiate the react app, you will need to cd into the client folder by using the command `cd client` in your terminal. Once you are in the client, run the command `npm start`. (Ensure you have all the dependencies requried installed in the node modules folder)

To initiate the flask server, you will need to create a virtual environment file (venv) file inside the backend folder. To do this, run the command `python -m venv venv`. Once the virtual environment has been created, you will need to activate it by running `./venv/Scripts/activate`. Once the virtual environment has been activated, ensure you have the dependencies for the ML program installed into the venv folder. Once this is completed, run `python server.py` to start the flask server.

Once the react and flask server are running, test the program out! In the react app, navigate to the test page and upload a file. When you click upload, an alert will pop up to tell you if the upload is successful. You can check assets1/validate/user to ensure the file was properly uploaded. Once the file is uploaded, click the ANALYZE button to see your result. The app will take some time to run but will eventually update the diagnosis label into its predicted result. When you are finished, delete the uploaded file in assets1/validate/user to run the program again. 

Happy diagnosing with OcnoAlert!
--------------------------------------------------------------
