from flask import Flask, jsonify, request
import sqlalchemy
from sqlalchemy import sql, text
import json
import requests
import os
from datetime import datetime
import random
import pandas as pd
import sys
import os

app = Flask(__name__)

def setup_connection():
    try:
        user = os.environ["DB_USER"]
        pwd = os.environ["DB_PWD"]
        db_url = os.environ["DB_URL"]
        db_name = os.environ["DB_NAME"] 
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

@app.route('/simulation/lagereingang', methods=['POST'])
def simuliere_lagereingang(komponenten_count = None):
    
    if not komponenten_count:
        komponenten_count = 50

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
        'Ausfuehrung': ausf_ls,
        'Preis': preis_ls,
        'Eingang': eingang_ls,
        'LagerID':lager_ls
    })

    engine, connection = setup_connection()
    trans = connection.begin()

    df_komp.to_sql("Komponente", con=connection, if_exists="append", index=False)
    trans.commit()

    return "success"

@app.route('/simulation/bestellung', methods=['POST'])
def simuliere_bestellung():
    
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
def produktionsdurchlauf():
    
    maschinen = get_maschinenreihenfolge()
    time = datetime.utcnow()
    timestr = str(time)
    time_db_format = timestr[:-6] + '0'

    engine, connection = setup_connection()
    trans = connection.begin()
    
    m_id_ls, tstmp_ls, nutzung_ls, dauer_ls, auslastung_ls, status_ls, prod_ls = [], [], [], [], [], [], []

    try:

        for strasse in maschinen:
            for  i in range(len(strasse)):
                maschinen_id, auto_id, bearbeitungszeit, position, status, prod = strasse[i]

                if auto_id: #wenn es eine auto_id gibt arbeitet Maschine noch --> evtl ausbuchen
                    nutzung = True
                    query_auto = f"SELECT * FROM Auto WHERE Auto_ID = {auto_id}"
                    res_auto = connection.execute(query_auto).fetchall()
                    zeit_in_maschine = time - res_auto[0][8]
                    print(zeit_in_maschine.total_seconds(), bearbeitungszeit)
                    if zeit_in_maschine.total_seconds() >= bearbeitungszeit: # pruefen ob Maschine fertig ist
                        print(f"-------------Maschine {maschinen_id} ist fertig")
                        ausfuerhung = dict(
                            typ = res_auto[0][1],
                            batterie = res_auto[0][2],
                            innenraum = res_auto[0][3],
                            farbe = res_auto[0][4],
                            autoFahren = res_auto[0][5],
                        )
                        wert = res_auto[0][7]

                        komp_id = None
                        mehrkosten_stufe = None
                        
                        if i == 0: #wenn letzte station

                            query_komp_Innenraum = f"SELECT KompID, Preis FROM Komponente WHERE Typ = 'Innenraum' AND AUTO_ID = {auto_id}" #wenn in lager, dann verfuegbar
                            res_innenraum = connection.execute(query_komp_Innenraum).fetchall()
                            
                            query_komp_AutoFahren = f"SELECT KompID, Preis FROM Komponente WHERE Typ = 'AutoFahren' AND AUTO_ID = {auto_id}"
                            res_autoFahren = connection.execute(query_komp_AutoFahren).fetchall()
                            if res_autoFahren and res_innenraum: # safety --> sollte nie False sein, da komp bei planung zugeordnet werden
                                kompid_innenraum, preis_innenraum = res_innenraum[0]
                                kompid_autoFahren, preis_autoFahren = res_autoFahren[0]

                                komp_id = kompid_autoFahren
                                mehrkosten_stufe = preis_innenraum + preis_autoFahren
                                query_komponentenzuordnung = f"UPDATE Komponente SET Einbau = '{time_db_format}', LagerID = NULL WHERE KompID = '{kompid_innenraum}'" #Einbau und aus Lager entfernen innenraum
                                connection.execute(query_komponentenzuordnung)
                                query_updateAuto = f"UPDATE Auto SET Status = 5, Wert = '{wert+mehrkosten_stufe}', ProdTimestmp = '{time_db_format}' WHERE AUTO_ID = '{auto_id}'" #set status to lagernd only for maschine 4

                                query_autoEinlagern = f"INSERT INTO Lager_Auto VALUES ('{auto_id}', '1', '{time_db_format}')"
                                connection.execute(query_autoEinlagern)

                        elif i == 1: #wenn station batterieeinbau
                            query_komp_id_Batterie = f"SELECT KompID, Preis FROM Komponente WHERE Typ = 'Batterie' AND AUTO_ID = '{auto_id}'"
                            res_bat = connection.execute(query_komp_id_Batterie).fetchall()
                            komp_id, mehrkosten_stufe = res_bat[0]
                            
                            query_updateAuto = f"UPDATE Auto SET Wert = {wert+mehrkosten_stufe}"
                            
                        elif i == 2:
                            query_komp_id_Farbe = f"SELECT KompID, Preis FROM Komponente WHERE Typ = 'Farbe' AND AUTO_ID = '{auto_id}'"
                            res_farbe = connection.execute(query_komp_id_Farbe).fetchall()
                            komp_id, mehrkosten_stufe = res_farbe[0]

                            query_updateAuto = f"UPDATE Auto SET Wert = {wert+mehrkosten_stufe}"

                        elif i == 3:
                            query_komp_id_typ = f"SELECT KompID, Preis FROM Komponente WHERE Typ = 'Typ' AND AUTO_ID = '{auto_id}'"
                            res_typ = connection.execute(query_komp_id_typ).fetchall()
                            komp_id, mehrkosten_stufe = res_typ[0]

                            query_updateAuto = f"UPDATE Auto SET Wert = {wert+mehrkosten_stufe}"
                        
                        query_komponentenzuordnung = f"UPDATE Komponente SET Einbau = '{time_db_format}', LagerID = NULL WHERE KompID = '{komp_id}'"
                        connection.execute(query_komponentenzuordnung)


                        query_updateMaschine = f"UPDATE Maschine SET Auto_ID = NULL WHERE MaschinenID = '{maschinen_id}'"
                        connection.execute(query_updateMaschine)

                        connection.execute(query_updateAuto)

                    else:
                        print(f"-------------Maschine {maschinen_id} arbeitet")

                else: #wenn keine auto_id --> Maschine wartet
                    print(f"-------------Maschine {maschinen_id} wartet")
                    produktionsstrasse_id =  maschinen.index(strasse)+1 
                    auto_id_pipe = None
                    nutzung = False
                    
                    if i == 3: # wenn erste maschine wartet id 3 --> position 4
                        query_next_auto = f"SELECT Auto_ID FROM Auto WHERE Status = 0 ORDER BY ProdTimestmp LIMIT 1"
                        res_next_auto = connection.execute(query_next_auto).fetchall()
                        if res_next_auto: # wenn es autos in der Pipeline gibt
                            auto_id_pipe = res_next_auto[0][0]
                            print("auto_id_pipe: "+ str(auto_id_pipe))
                            query_updateAuto = f"UPDATE Auto SET Status = '{position}', ProdTimestmp = '{time_db_format}', Produktionsstrasse  = '{produktionsstrasse_id}', BeginnProdTime = '{time_db_format}' WHERE Auto_ID = '{auto_id_pipe}'"
                            connection.execute(query_updateAuto)
                            query_updateMaschine = f"UPDATE Maschine SET Auto_ID = '{auto_id_pipe}' WHERE MaschinenID = '{maschinen_id}'"
                            connection.execute(query_updateMaschine)
                        else:
                            print("-------------Kein geplantes auto in der Pipeline")
                    else: 
                        _, a_next_id, _, _, _, _ = strasse[i+1]
                        if not a_next_id: #pruefen ob Maschine in der position vorher schon fertig ist
                            
                            query_auto = f"SELECT * FROM Auto WHERE Produktionsstrasse = '{produktionsstrasse_id}' AND Status = '{position-1}'" #TODO pruefen ob i = maschinen_id -1 fuer prodstrasse 1
                            res_auto = connection.execute(query_auto).fetchall()
                            if res_auto: #prüfen ob ein auto in dieser produktionsstufe ist (nur start und ende)
                                auto_id_pipe = res_auto[0][0]
                                query_updateAuto = f"UPDATE Auto SET Status = '{position}', ProdTimestmp = '{time_db_format}' WHERE Auto_ID = '{auto_id_pipe}'"
                                connection.execute(query_updateAuto)
                                query_updateMaschine = f"UPDATE Maschine SET Auto_ID = '{auto_id_pipe}' WHERE MaschinenID = '{maschinen_id}'"
                                connection.execute(query_updateMaschine)        

                query_letzte_nutzung = f"SELECT * FROM Auslastung_Maschine WHERE MaschinenID = '{maschinen_id}' ORDER BY Timestmp DESC LIMIT 10"
                res_letzte_nutzung = connection.execute(query_letzte_nutzung).fetchall()
                            
                if res_letzte_nutzung: #only not ramp up
                    dauer = time - res_letzte_nutzung[0][2]
                    dauer = dauer.total_seconds()
                    laufzeit = dauer
                    for t in res_letzte_nutzung:
                        laufzeit = laufzeit + t[3]
                    nutzungszeit = 0
                    if nutzung:
                        nutzungszeit = dauer
                    for t in res_letzte_nutzung:
                        if t[1]:
                            nutzungszeit = nutzungszeit + t[3]
                    
                    auslastung = nutzungszeit/laufzeit

                else:
                    dauer, laufzeit, auslastung = 0, 0 ,0
                    nutzung = False
                    
                status_ls.append(status)
                prod_ls.append(prod)
                m_id_ls.append(maschinen_id)
                tstmp_ls.append(time_db_format)
                nutzung_ls.append(nutzung)
                dauer_ls.append(dauer)
                auslastung_ls.append(auslastung)     

            # TESTED AB HIER -----------------------------
            #decide on next car and assign komponents
            query_bestellung = f"SELECT * FROM Bestellung WHERE Auto_ID IS NULL ORDER BY Eingang"
            res_bestellung = connection.execute(query_bestellung).fetchall()

            if res_bestellung: # wenn es nicht bearbeitete bestellungen gibt
                best_id_ls = [b[0] for b in res_bestellung]
                best_typ_ls = [b[1] for b in res_bestellung]
                best_bat_ls = [b[2] for b in res_bestellung]
                best_inn_ls = [b[3] for b in res_bestellung]
                best_farbe_ls = [b[4] for b in res_bestellung]
                best_autoFahren_ls = [b[6] for b in res_bestellung]
                
                komp_ls = []
                bestellung_id = None 
                for i in range(len(best_id_ls)):
                    #check availability of needed components
                    query_typ_check = f"SELECT KompID FROM Komponente WHERE Auto_ID IS NULL AND Typ = 'Typ' AND Ausfuehrung = '{best_typ_ls[i]}' ORDER BY Eingang"
                    typ_id = connection.execute(query_typ_check).fetchall()
                    if typ_id:
                        komp_ls.append(typ_id[0][0])
                        query_batt_check = f"SELECT KompID FROM Komponente WHERE Auto_ID IS NULL AND Typ = 'Batterie' AND Ausfuehrung = '{best_bat_ls[i]}' ORDER BY Eingang"
                        batt_id = connection.execute(query_batt_check).fetchall()
                        if batt_id:
                            komp_ls.append(batt_id[0][0])
                            query_inn_check = f"SELECT KompID FROM Komponente WHERE Auto_ID IS NULL AND Typ = 'Innenraum' AND Ausfuehrung = '{best_inn_ls[i]}' ORDER BY Eingang"
                            inn_id = connection.execute(query_inn_check).fetchall()
                            if inn_id:
                                komp_ls.append(inn_id[0][0])
                                query_farbe_check = f"SELECT KompID FROM Komponente WHERE Auto_ID IS NULL AND Typ = 'Farbe' AND Ausfuehrung = '{best_farbe_ls[i]}' ORDER BY Eingang"
                                farbe_id = connection.execute(query_farbe_check).fetchall()
                                if farbe_id:
                                    komp_ls.append(farbe_id[0][0])
                                    query_autoFahren_check = f"SELECT KompID FROM Komponente WHERE Auto_ID IS NULL AND Typ = 'AutoFahren' AND Ausfuehrung = '{best_autoFahren_ls[i]}' ORDER BY Eingang"
                                    autoFahren_id = connection.execute(query_autoFahren_check).fetchall()
                                    if autoFahren_id:
                                        komp_ls.append(autoFahren_id[0][0])
                                        bestellung_id = best_id_ls[i]
                                        index = i
                                        break
                                    else:
                                        komp_ls = []
                                        continue
                                else:
                                    komp_ls = []
                                    continue
                            else:
                                komp_ls = []
                                continue
                        else:
                            komp_ls = []
                            continue    
                    else:
                        komp_ls = []
                        continue
                
                if komp_ls:
                    print("-------------Plaung Neues Auto")               
                    query_create_car = f"INSERT INTO Auto (Typ, Batterie, Innenraum, Farbe, AutoFahren, Status, Wert, ProdTimestmp) VALUES ('{best_typ_ls[index]}', '{best_bat_ls[index]}', '{best_inn_ls[index]}', '{best_farbe_ls[index]}', '{best_autoFahren_ls[index]}', 0, 0, '{time_db_format}')"

                    connection.execute(query_create_car)

                    auto_id_new_query = f"SELECT Auto_ID FROM Auto WHERE ProdTimestmp = '{time_db_format}' ORDER BY Auto_ID DESC"
                    auto_id_new_query = text(auto_id_new_query)
                    auto_id_new = connection.execute(auto_id_new_query).fetchall()[0][0]
                    
                    print(f"auto_id: {auto_id_new}")
                    query_assign_komponents = f"UPDATE Komponente SET Auto_ID = '{auto_id_new}' WHERE KompID = '{komp_ls[0]}' OR KompID = '{komp_ls[1]}' OR KompID = '{komp_ls[2]}' OR KompID = '{komp_ls[3]}' OR KompID = '{komp_ls[4]}'"
                    connection.execute(query_assign_komponents)

                    query_updateBestellung = f"UPDATE Bestellung SET Auto_ID = '{auto_id_new}' WHERE BESTELLUNG_ID = '{bestellung_id}'"
                    connection.execute(query_updateBestellung)

                else:
                    print("-------------Lagerbestand nicht ausreichend")
                    query_best_unbearbeitet = f"SELECT COUNT(Bestellung_ID) FROM Bestellung WHERE Auto_ID IS NULL"
                    res_best_unbearbeitet = connection.execute(query_best_unbearbeitet).fetchall()[0][0]
                    
                    if res_best_unbearbeitet >= 0: # HC erst ab 20 unbearbeiteten Bestellungen nachbestellen
                        print(f"-------------Lagerbestand auffüllen (unbearbeitete Bestellungen: {res_best_unbearbeitet})")
                        simuliere_lagereingang(20)                     

        print("-------------Statusupdate Produktionshalle")  
        df_auslastung = pd.DataFrame({
            'MaschinenID': m_id_ls,
            'Timestmp': tstmp_ls,
            'Nutzung': nutzung_ls,
            'Dauer': dauer_ls,
            'Auslastung': auslastung_ls
        })

        df_prodVerlauf = pd.DataFrame({
            'MaschinenID': m_id_ls,
            'Timestmp': tstmp_ls,
            'Produktivität': prod_ls
        })

        df_statusVerlauf = pd.DataFrame({
            'MaschinenID': m_id_ls,
            'Timestmp': tstmp_ls,
            'Status': status_ls
        })

        df_auslastung.to_sql("Auslastung_Maschine", con=connection, if_exists="append", index=False)
        df_prodVerlauf.to_sql("ProduktivitätVerlauf_Maschine", con=connection, if_exists="append", index=False)
        df_statusVerlauf.to_sql("StatusVerlauf_Maschine", con=connection, if_exists="append", index=False)   
        
        query_lb_unf = "SELECT COUNT(KompID) FROM Komponente WHERE Einbau IS Null" # Lagerbestand rohstoffe
        query_lb_rst = "SELECT COUNT(Auto_ID) FROM Auto WHERE Status = 1 OR Status = 2 OR Status = 3 OR Status = 4" #lagerbestand unfertige erzeugnisse
        query_lb_fert = "SELECT COUNT(Auto_ID) FROM Auto WHERE Status = 5" #lagerbestand fertige erzeugnisse
        lb_unf = connection.execute(query_lb_unf).fetchall()[0][0]
        lb_rst = connection.execute(query_lb_rst).fetchall()[0][0]
        lb_fert = connection.execute(query_lb_fert).fetchall()[0][0]
        lagerbestand_ges = int(lb_unf) + int(lb_rst) + int(lb_fert)

        if lb_fert > 30: #HC Bestellungen versenden ab 30 bestellungen
            print(f"-------------Versandt Bestellungen (Fert Erzeugnisse: {lb_fert})")
            query_getLager = f"SELECT Auto_ID FROM Lager_Auto"
            lager = connection.execute(query_getLager).fetchall()
            for auto in lager:
                a_id = auto[0]
                query_updateBestellausgang = f"UPDATE Bestellung SET Ausgang = '{time_db_format}' WHERE Auto_ID = '{a_id}'"
                connection.execute(query_updateBestellausgang)
                query_updateAutoVersandt = f"UPDATE Auto SET Status = '6' WHERE Auto_ID = {a_id}"
                connection.execute(query_updateAutoVersandt)
            query_updateLager ="DELETE FROM Lager_Auto"
            connection.execute(query_updateLager)

            
            lagerbestand_ges = lagerbestand_ges = int(lb_unf) + int(lb_rst)

        lager_status = lagerbestand_ges/10000 #Kapazität aktuell HC 10000

        query_update_lagerstatus = f"UPDATE Lager SET Status = '{lager_status}' WHERE LagerID = '1'"
        connection.execute(query_update_lagerstatus)
        
        trans.commit()  

    except:
        trans.rollback()
        raise
    finally:
        #trans.rollback()
        connection.close()
        engine.dispose()

    return "success"

@app.route('/test/createandreturncar', methods=['POST'])
def createandreturncar():
    engine, connection = setup_connection()
    trans = connection.begin()

    time = datetime.utcnow()

    timestr = str(time)
    time_db_format = timestr[:-6] + '0'
    print(timestr)
    print(time_db_format)
    
    query_create_car = f"INSERT INTO Auto (Typ, Batterie, Innenraum, Farbe, AutoFahren, Status, Wert, ProdTimestmp) VALUES ('Model X', 'Maximale Reichweite', 'weiss', 'Red Multi-Coat', 'yes', 0, 0, '{time_db_format}')"
    query_create_car = text(query_create_car)
    connection.execute(query_create_car)

    auto_id_new_query = f"SELECT Auto_ID FROM Auto WHERE ProdTimestmp = '{time_db_format}'"
    auto_id_new_query = text(auto_id_new_query)
    print(auto_id_new_query)
    auto_id_new = connection.execute(auto_id_new_query).fetchall()
    print(auto_id_new)
    
    trans.rollback()
    return "success"

@app.route('/test/auslastung', methods=['POST'])
def testauslastung():
    engine, connection = setup_connection()
    trans = connection.begin()
    nutzung_base = [True, False]

    maschinen = get_maschinenreihenfolge()
    time = datetime.utcnow()
    timestr = str(time)
    time_db_format = timestr[:-6] + '0'
    
    m_id_ls, tstmp_ls, nutzung_ls, dauer_ls, auslastung_ls, status_ls, prod_ls = [], [], [], [], [], [], []

    for strasse in maschinen:
            print(strasse)
            for  i in range(len(strasse)):
                nutzung = random.choice(nutzung_base)
                print(i, strasse[i])
                maschinen_id, auto_id, bearbeitungszeit, position, status, prod = strasse[i]

                query_letzte_nutzung = f"SELECT * FROM Auslastung_Maschine WHERE MaschinenID = '{maschinen_id}' ORDER BY Timestmp DESC LIMIT 10"
                res_letzte_nutzung = connection.execute(query_letzte_nutzung).fetchall()
                        
                if res_letzte_nutzung: #only not ramp up
                    print(res_letzte_nutzung)
                    print(res_letzte_nutzung[0])
                    print(res_letzte_nutzung[0][2])
                    dauer = time - res_letzte_nutzung[0][2]
                    dauer = dauer.total_seconds()
                    laufzeit = dauer
                    for t in res_letzte_nutzung:
                        laufzeit = laufzeit + t[3]
                    nutzungszeit = 0
                    if nutzung:
                        nutzungszeit = dauer
                    for t in res_letzte_nutzung:
                        if t[1]:
                            nutzungszeit = nutzungszeit + t[3]
                    
                    auslastung = nutzungszeit/laufzeit

                else:
                    dauer, laufzeit, auslastung = 0, 0 ,0
                    nutzung = False
                    
                status_ls.append(status)
                prod_ls.append(prod)
                m_id_ls.append(maschinen_id)
                tstmp_ls.append(time_db_format)
                nutzung_ls.append(nutzung)
                dauer_ls.append(dauer)
                auslastung_ls.append(auslastung)                    

    df_auslastung = pd.DataFrame({
        'MaschinenID': m_id_ls,
        'Timestmp': tstmp_ls,
        'Nutzung': nutzung_ls,
        'Dauer': dauer_ls,
        'Auslastung': auslastung_ls
    })

    df_prodVerlauf = pd.DataFrame({
        'MaschinenID': m_id_ls,
        'Timestmp': tstmp_ls,
        'Produktivität': prod_ls
    })

    df_statusVerlauf = pd.DataFrame({
        'MaschinenID': m_id_ls,
        'Timestmp': tstmp_ls,
        'Status': prod_ls
    })

    print(df_auslastung)

    df_auslastung.to_sql("Auslastung_Maschine", con=connection, if_exists="append", index=False)
    df_prodVerlauf.to_sql("ProduktivitätVerlauf_Maschine", con=connection, if_exists="append", index=False)
    df_statusVerlauf.to_sql("StatusVerlauf_Maschine", con=connection, if_exists="append", index=False)
    
    trans.commit()
    
    return "success"

@app.route('/simulation/test', methods=['POST'])
def get_maschinenreihenfolge():
    engine, connection = setup_connection()
    maschine_ls = []

    query_1 = f"SELECT MaschinenID, Auto_ID, Bearbeitungszeit, Position, Status, Produktivitaet FROM  Maschine ORDER BY Position DESC"
    
    res = connection.execute(query_1).fetchall()

    converted_ls = []
    for item in res:

        a, b, c, d, e, f = item[0], item[1], item[2], item[3], item[4], item[5]
        umrechungsfkt = f * 0.01

        if e == "Kaputt":
            c = 9999999999999
        else:
            c = c * pow(umrechungsfkt, -1)
        
        zw = a, b, c, d, e, f
        converted_ls.append(zw)
    
    maschine_ls.append(converted_ls)

    return maschine_ls


if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0', port = '8404')