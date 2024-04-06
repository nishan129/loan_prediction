from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from src.loan.pipeline.predication import Prediction

app = Flask(__name__)


@app.route('/', methods=["GET"])
def homePage():
    return render_template("index.html")

@app.route('/train', methods=["GET"])
def training():
    os.system("python main.py")
    return "Training Successful!"


@app.route('/predict', methods=["POST","GET"])
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            Income	 =int(request.form["income"])
            Age =int(request.form["age"])
            Experience =int(request.form["experience"])
            Married =str(request.form["married"])
            House_Ownership	 =str(request.form["house"])
            Car_Ownership =str(request.form["car"])
            Profession =str(request.form["profesion"])
            CITY =str(request.form["city"])
            STATE =str(request.form["state"])
            CURRENT_JOB_YRS =int(request.form["jobyear"])
            CURRENT_HOUSE_YRS =int(request.form["houseyer"])
       
         
            data = [Income,Age,Experience,Married,House_Ownership,Car_Ownership,Profession,CITY,STATE,CURRENT_JOB_YRS,CURRENT_HOUSE_YRS]
            #print(data)
            data = np.array(data).reshape(1,-1)
            #print(data)
            
            
            obj = Prediction()
            pred = obj.predict(data)
            predict = ""
            if pred == 0:
                predict = "Your Loan is Not Aprove 😢 But Your Phone is Hacked 😂😂😂 "
            else:
                predict = "Your Loan is Not Aprove 😢 But Your Phone is not Hacked Plss Try again"
                
                
            #print(predict)

            return render_template('result.html', prediction = str(predict))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    # else:
    #     return render_template('result.html')

if __name__ == "__main__":
    #app.run(host="0.0.0.0", port= 8080, debug=True)
    app.run(host="0.0.0.0", port= 8080)