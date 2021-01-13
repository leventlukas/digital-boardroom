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

@app.route('/simulation/lagereingang', methods=['POST'])
def sumuliere_algereingang():

    komponenten_count = 10

    typ_base_ls = ['Typ', 'Batterie', 'Innenraum', 'Farbe', 'AutoFahren']
    typ_aus_base_ls = ['Model X', 'Model S', 'Model 3']
    bat_aus_base_ls = ['Standard Plus', 'Maximale Reichweite', 'Performance', 'Plaid']
    inn_aus_base_ls = ['schwarz', 'weiss']
    farbe_aus_base_ls = ['Pearl White Multi-Coat', 'Solid Black', 'Midnight Silver Metallic', 'Deep Blue Metallic', 'Red Multi-Coat']
    autofahr_aus_base_ls = ['yes', 'no']

    typ_ls, ausf_ls, preis_ls, eingang_ls, lager_ls = ([] for i in range(5))

    for komponente in range(komponenten_count):
        komp_typ = random.choice(typ_base_ls)
        typ_ls.append(komp_typ)
        
        if komp_typ == 'Typ':
            ausf_ls.append(random.choice(typ_aus_base_ls))
            preis_ls.append(200)
        
        elif komp_typ == 'Batterie':
            ausf_ls.append(random.choice(bat_aus_base_ls))
            preis_ls.append(300)

        elif komp_typ == 'Innenraum':
            ausf_ls.append(random.choice(inn_aus_base_ls))
            preis_ls.append(150)

        elif komp_typ == 'Farbe':
            ausf_ls.append(random.choice(farbe_aus_base_ls))
            preis_ls.append(50)

        elif komp_typ == 'AutoFahren':
            ausf_ls.append(random.choice(autofahr_aus_base_ls))
            preis_ls.append(10)
        
        eingang_ls.append(datetime.now())
        lager_ls.append(1)
    typ_ls, ausf_ls, preis_ls, eingang_ls, lager_ls
    df_komp = pd.DataFrame({
        'Typ': typ_ls,
        'Ausführung': ausf_ls,
        'Preis': preis_ls,
        'Eingang': eingang_ls,
        'LagerID':lager_ls
    })

    engine, connection = setup_connection()
    trans = connection.begin()

    df_komp.to_sql("Komponente", con=connection, if_exists="append", index=False)
    trans.commit()

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

@app.route('/simulation/produktionsdurchlauf', methods=['POST'])
def ws_produktionsdurchlauf():
    
    engine, connection = setup_connection()
    zeitpunkt = datetime.now()
    
    # Prüfen ob Auto in Status 4 fertigstellen --> Fertigstellen und Kaskadieren (wenn nicht don't do anything)
    # Auto in Status 3 auf Status 

    # Alle letzten Maschinen einer Produktionsstraße
    # query_0 = 'SELECT * FROM ProduktionLine_Maschine WHERE Position = 4'
    
    # trans = connection.begin()
    # res = connection.execute(query).fetchall()
    
    # for maschine in res:
    #     maschinenID = maschine[0]
    #     prodlineID = maschine[1]

    maschinen = get_maschinenreihenfolge()

    for strasse in maschinen:
        print(strasse)
        for  i in range(len(strasse)):
            maschinen_id, auto_id, bearbeitungszeit = strasse[i]
            m_next_id, a_next_id, bzeit_next = strasse[i+1]

            engine, connection = setup_connection()
            trans = connection.begin()

            time = datetime.now()
            query_auto = f"SELECT * FROM Auto WHERE Auto_ID = {auto_id}"
            
            res_auto = connection.execute(query_auto).fetchall()

            zeit_in_maschine = time - res_auto[0][8]

            if zeit_in_maschine.difference.total_seconds() >= bearbeitungszeit:

                ausfürhung = dict(
                    typ = res_auto[0][1],
                    batterie = res_auto[0][2],
                    innenraum = res_auto[0][3],
                    farbe = res_auto[0][4],
                    autoFahren = res_auto[0][5],
                )
                wert = res_ausführung[0][7]
                
                if not maschinenID%4: #wenn letzte station

                    query_komp_id_Innenraum = f"SELECT KompID, Preis FROM Komponente WHERE Typ = Innenraum AND AUTO_ID = {auto_id}" #wenn in lager, dann verfügbar
                    preis_innenraum # TODO
                    query_komp_id_AutoFahren = f"SELECT KompID, Preis FROM Komponente WHERE Typ = AutoFahren AND AUTO_ID = {auto_id}"
                    preis_autoFahren # TODO
                
                    query_komponentenzuordnung = f"UPDATE Komponente SET Einbau = {time}, LagerID = NULL" #Einbau und aus Lager entfernen

                query_updateMaschine = f"UPDATE Maschine SET Auto_ID = NULL WHERE MaschinenID = {maschinen_id}"
                    
                mehrkosten_stufe = preis_innenraum + preis_autoFahren
                
                query_updateAuto = f"UPDATE Auto SET Status = 5, Wert = {wert+mehrkosten_stufe}, ProdTimestmp = {time}"
        
                

    
    # ausbuchen 



    pass

@app.route('/simulation/test', methods=['POST'])
def get_maschinenreihenfolge():
    engine, connection = setup_connection()
    maschine_ls = []

    query_1 = f"SELECT MaschinenID, Auto_ID, Bearbeitungszeit FROM  Maschine ORDER BY Position DESC"
    res = connection.execute(query_1).fetchall()
    maschine_ls.append(res)
    
    print(maschine_ls)
    return maschine_ls


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = '8404')