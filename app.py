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

# 1. Devolver la predicción de los nuevos datos enviados mediante argumentos en la llamada
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


# 2. Almacenar nuevos registros en la base de datos new_data_advertising.db
@app.route('/ingest_data', methods=['GET'])
def ingest_data():

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)
    sales = request.args.get('sales', None)

    if tv is None or radio is None or newspaper is None or sales is None:
        
        return "Missing args, the input values are needed to insert data"
    else:
        conn = sqlite3.connect("data/advertising.db")
        cur = conn.cursor()
        query = 'INSERT INTO sales (TV, radio, newspaper, sales) VALUES (' + tv + ', ' + radio + ', ' + newspaper + ', ' + sales +')'
        cur.execute(query)
        conn.commit()

        return "The data has been added to the database"


# 3. Reentrenar y guardar el modelo con los datos disponibles en la carpeta data
@app.route('/retrain', methods=['GET'])
def retrain():
    connection = sqlite3.connect("data/advertising.db")
    crsr = connection.cursor()
    query = 'SELECT * FROM sales'
    crsr.execute(query)
    ans = crsr.fetchall()
    names = [description[0] for description in crsr.description]
    
    df = pd.DataFrame(ans,columns=names)

    X = df.drop(columns=['sales'])
    y = df['sales']

    model = pickle.load(open('data/advertising_model','rb'))
    model.fit(X,y)
    pickle.dump(model, open('data/advertising_model_v1','wb'))

    return "New model retrained and saved as advertising_model_v1"

# 4 Comprobar función

@app.route('/print_db', methods=['GET'])
def print_db():

    connection = sqlite3.connect('data/advertising.db')
    cursor = connection.cursor()

    query = '''
    SELECT * FROM datos
    '''

    result = cursor.execute(query).fetchall()
    connection.commit()

    return jsonify(result)