from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import sql
import json
import requests
import os
from datetime import *

app = Flask(__name__)

# app.config['MYSQL_USER'] = os.getenv("DB_USER")
# app.config['MYSQL_PASSWORD'] = os.getenv("DB_USER")

# app.config['MYSQL_USER'] = 
# app.config['MYSQL_PASSWORD'] = 
# app.config['MYSQL_HOST'] = 
# app.config['MYSQL_DB'] = 
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# mysql = MySQL(app)

def setup_connection():
    try:
        user = "janlevent"
        pwd = "DigitalBoardroom2021"
        db_url = 'realtime-bi.tk'
        db_name = 'realtimebi' 
        connection_string = 'mysql+pymysql://' + user + ':' + pwd + '@' + db_url + ':3306/' + db_name
        engine = sqlalchemy.create_engine(connection_string, echo=False)
        connection = engine.connect()

    except Exception:
        raise
    
    return engine, connection

# Test

@app.route('/ping', methods=['POST'])
def ws_ping():
    print(request.json)
    return ("pong")

@app.route('/test', methods=['POST'])
def ws_test():
    print("test")
    query = 'SELECT * FROM realtimebi.Bestellung'

    engine, connection = setup_connection()
    trans = connection.begin()
    res = connection.execute(query).fetchall()
    
    print(res)

    return jsonify(res)

# Simulation

@app.route('/simulation/einlagerung', methods=['POST'])
def ws_simuliere_einlagerung():
    # 1. Setze Status Lager auf Befüllen
    # 2. Erhöhe Komponenten (Karosserie, Batterie, Innenraum, Farbe, AutoFahren) Sleep each 5 sec
    # 3. Setze Status auf Prozent von Kapazität


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = '8404')