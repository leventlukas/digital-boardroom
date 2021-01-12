from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import sql
import json
import requests
import os
from datetime import datetime
import random
import pandas as pd

app = Flask(__name__)

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

    return json.dumps(res)

# Simulation

@app.route('/simulation/einlagerung', methods=['POST'])
def ws_simuliere_einlagerung():
    # 1. Setze Status Lager auf Befüllen
    # 2. Erhöhe Komponenten (Karosserie, Batterie, Innenraum, Farbe, AutoFahren) Sleep each 5 sec
    # 3. Pflege ein in Lager_Komponente und setze Timestamp auf aktuell
    # 3. Setze Status auf Prozent von Kapazität
    pass


@app.route('/simulation/bestellung', methods=['POST'])
def ws_simuliere_bestellung():
    
    bestellung_count = 10 # TODO: Dynamically from JSON

    # create random config of cars to be produced
    typ_base_ls = ['Model X', 'Model S', 'Model 3']
    bat_base_ls_x = ['Maximale Reichweite', 'Performance']
    bat_base_ls_3 = ['Standard Plus', 'Maximale Reichweite', 'Performance']
    bat_base_ls_s = ['Maximale Reichweite', 'Performance', 'Plaid']
    inn_base_ls = ['schwarz', 'weiss']
    farbe_base_ls = ['Pearl White Multi-Coat', 'Solid Black', 'Midnight Silver Metallic', 'Deep Blue Metallic', 'Red Multi-Coat']
    autofahr_base_ls = ['yes', 'no']
    
    typ_best_ls, bat_best_ls, inn_best_ls, farbe_best_ls, eingang_best_ls, autofahr_best_ls, preis_best_ls = ([] for i in range(7))

    for auto in range(bestellung_count):
        typ_best_ls.append(random.choice(typ_base_ls))
        
        if typ_best_ls[auto] == 'Model X':
            bat_best_ls.append(random.choice(bat_base_ls_x))
            if bat_best_ls[auto] == 'Maximale Reichweite':
                preis_best_ls.append(90990)
            else:
                preis_best_ls.append(107990)

        
        if typ_best_ls[auto] == 'Model S':
            bat_best_ls.append(random.choice(bat_base_ls_s))
            if bat_best_ls[auto] == 'Maximale Reichweite':
                preis_best_ls.append(81990)
            elif bat_best_ls[auto] == 'Performance':
                preis_best_ls.append(98990)
            else:
                preis_best_ls.append(139990)

        if typ_best_ls[auto] == 'Model 3':
            bat_best_ls.append(random.choice(bat_base_ls_3))
            if bat_best_ls[auto] == 'Maximale Reichweite':
                preis_best_ls.append(42900)
            elif bat_best_ls[auto] == 'Performance':
                preis_best_ls.append(48490)
            else:
                preis_best_ls.append(42900)
        
        inn_best_ls.append(random.choice(inn_base_ls))
        if inn_best_ls[auto] == 'weiss':
            preis_best_ls[auto] = preis_best_ls[auto] + 1600

        farbe_best_ls.append(random.choice(farbe_base_ls))
        if farbe_best_ls[auto] == 'Red Multi-Coat':
            preis_best_ls[auto] = preis_best_ls[auto] + 2900
        elif farbe_best_ls[auto] != 'Pearl White Multi-Coat':
            preis_best_ls[auto] = preis_best_ls[auto] + 1600

        eingang_best_ls.append(datetime.now())
        
        autofahr_best_ls.append(random.choice(autofahr_base_ls))
        if autofahr_best_ls[auto] == 'yes':
            preis_best_ls[auto] = preis_best_ls[auto] + 7500

        

    df_bestellungen = pd.DataFrame({
        'Typ': typ_best_ls,
        'Batterie': bat_best_ls,
        'Innenraum': inn_best_ls,
        'Farbe': farbe_best_ls,
        'Eingang': eingang_best_ls,
        'AutoFahren': autofahr_best_ls,
        'Preis': preis_best_ls
    })

    engine, connection = setup_connection()
    trans = connection.begin()

    df_bestellungen.to_sql("Bestellung", con=connection, if_exists="append", index=False)
    trans.commit()


    return df_bestellungen.to_json()

if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = '8404')