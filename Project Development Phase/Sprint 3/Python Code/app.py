#Import necessary libraries
from flask import Flask, render_template, request,url_for

import numpy as np
import os
import requests
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
import pandas as pd
from PIL import Image


model = load_model(r"Uploads\Vegetable .h5")
model1 = load_model(r"Uploads\fruitdata.h5")
print(model)

print("Model Loaded Successfully")

# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/")
def home():
        return render_template('home.html')

@app.route("/predict2", methods=['GET', 'POST'])
def predict2():
        return render_template('predict2.html')


# render index.html page
@app.route("/predict1", methods=['GET', 'POST'])
def predict1():
        return render_template('predict1.html')
    
 
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image1'] # fet input
        filename = secure_filename(file.filename)
        basepath = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(basepath,r'static\upload',filename)
        img_path = os.path.join(r'static\upload',filename)
        file.save(file_path)
        print(filename)
        Prediction_image,output=leaves(Plant_image=file_path)
        return render_template('predict1.html',pred_output=Prediction_image,Disease=output,value=img_path,flag=True)
        

def leaves(Plant_image):
        img=image.load_img(Plant_image,target_size=(128,128))
        x=image.img_to_array(img)
        x=np.expand_dims(x,axis=0)
        plant = request.form.get('Plant')
        print(plant)
        if(plant == "vegetable"):
            prediction=np.argmax(model.predict(x),axis=1)
            print(prediction)
            index=['Pepper,_bell___Bacterial_spot','Pepper,_bell___healthy','Potato___Early_blight','Potato___Late_blight','Potato___healthy','Tomato___Bacterial_spot','Tomato___Late_blight','Tomato___Leaf_Mold','Tomato___Septoria_leaf_spot']
            print(index[prediction[0]])
            df=pd.read_excel(r'Uploads\precautions - veg.xlsx')
            print(df.iloc[prediction[0]]['caution'])

        else:
            prediction=np.argmax(model1.predict(x),axis=1)
            index=['Apple___Black_rot','Apple___healthy','Corn_(maize)___Northern_Leaf_Blight','Corn_(maize)___healthy','Peach___Bacterial_spot','Peach___healthy']
            print(index[prediction[0]])
            df=pd.read_excel(r'Uploads\precautions - fruits.xlsx')
            print(df.iloc[prediction[0]]['caution'])
        
        return df.iloc[prediction[0]]['caution'],index[prediction[0]]


if __name__ == "__main__":
    app.run(threaded=False,debug=True) 
    
    
