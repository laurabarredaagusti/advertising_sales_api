from flask import Flask, request, jsonify
import os
import pickle
import pandas as pd
import sqlite3


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido la API de Laura Barreda del modelo predictivo de ventas"

# 1. Crea un endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/predict', methods=['GET'])
def predict():
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[tv,radio,newspaper]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + '€'


# 2. Crea un endpoint para almacenar nuevos registros en la base de datos que deberá estar previamente creada
@app.route('/ingest_data', methods=['PUT'])
def ingest_data():
    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    sales = request.args.get('sales', None)

    connection = sqlite3.connect("books.db")
    crsr = connection.cursor()
    query = 'INSERT INTO sales (TV, radio, newspaper, sales) VALUES (' + tv + ', ' + radio + ', ' + newspaper + ', ' + sales +')'
    crsr.execute(query)