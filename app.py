# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:55:37 2020

@author: uthaman.pk
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl','rb'))

@app.route('/')
def home():
    return render_template('Index.html')

@app.route('/predict', methods=['POST'])
def predict():
    #for rendering results on HTML GUI
    int_features = [int(x) for x in request.form.values()]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)
    
    output = round(prediction[0],2)
    
    return render_template('Index.html', prediction_text='Employee Salary with Experience {} years, Test Score {} and Interview Score {} should be $ {}'.format(int_features[0],int_features[1],int_features[2],output))

if __name__=='__main__':
    app.run()
