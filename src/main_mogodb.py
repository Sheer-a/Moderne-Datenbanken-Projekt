import pymongo
import csv
from pymongo import MongoClient
import datetime
import time
from bson import ObjectId
import json
import os
from pymongo import MongoClient, errors
from pprint import pprint


# Globale Dictionaries
#Mapping von alten IDs (aus der CSV-Datei) zu neuen MongoDB ObjectIds
id_mapping_adressen = {}
id_mapping_nutzer = {}
id_mapping_standort = {}

client = MongoClient('mongodb://mongouser:mongopassword@localhost:27017/')
db = client['meinedatenbank']
file_path = "C:/Users/FHBBook/OneDrive - FH Dortmund/Informatik Studium/Semester 6/Moderne Datenbanken/Projekt/testdaten/"
data_files = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.startswith("dataset_block")]


def objectid_to_str(data):
    if isinstance(data, dict):
        return {k: objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [objectid_to_str(v) for v in data]
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

def str_to_objectid(data):
    if isinstance(data, dict):
        return {k: str_to_objectid(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [str_to_objectid(v) for v in data]
    elif isinstance(data, str):
        try:
            return ObjectId(data)
        except:
            return data
    else:
        return data

def save_dictionaries():
    data = {
        'id_mapping_adressen': objectid_to_str(id_mapping_adressen),
        'id_mapping_nutzer': objectid_to_str(id_mapping_nutzer),
        'id_mapping_standort': objectid_to_str(id_mapping_standort)
    }

    with open('mappings.json', 'w') as json_file:
        json.dump(data, json_file)

def load_dictionaries():
    global id_mapping_adressen, id_mapping_nutzer, id_mapping_standort

    try:
        with open('mappings.json', 'r') as json_file:
            data = json.load(json_file)

            id_mapping_adressen = str_to_objectid(data['id_mapping_adressen'])
            id_mapping_nutzer = str_to_objectid(data['id_mapping_nutzer'])
            id_mapping_standort = str_to_objectid(data['id_mapping_standort'])
            print("Dictionaries geladen")
    except FileNotFoundError:
        print("Mappings.json Datei nicht gefunden. Die Dictionaries sind leer.")
    except json.JSONDecodeError:
        print("Fehler beim Dekodieren der JSON-Datei. Die Dictionaries sind leer.")

def load_data(file_path):

    current_adress_id = 1  # Starte mit der ID 1 und inkrementiere für jede Adresse
    current_nutzer_id = 1  # Starte mit der ID 1 und inkrementiere für jeden Nutzer
    current_standort_id = 1 # Starte mit der ID 1 und inkrementiere für jeden Standort

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'Adresse':
                adresse = {
                    "Strasse": row[1],
                    "Hausnummer": row[2],
                    "PLZ": row[3],
                    "Stadt": row[4],
                    "Land": row[5]
                }
                result = db.adressen.insert_one(adresse)
                id_mapping_adressen[current_adress_id] = result.inserted_id
                current_adress_id += 1

            elif row[0] == 'Nutzer':
                nutzer = {
                    "Info": row[1],
                    "Profilbild": row[2],
                    "Email": row[3],
                    "NutzerTyp": row[4],
                    "Bannerbild": row[5]
                }
                result = db.nutzer.insert_one(nutzer)
                id_mapping_nutzer[current_nutzer_id] = result.inserted_id
                current_nutzer_id += 1

            elif row[0] == 'Person':
                person = {
                    "Nutzer_ID": id_mapping_nutzer[int(row[1])],  # Verknüpfung mit Nutzer-ID
                    "Vorname": row[2],
                    "Nachname": row[3],
                    "Geburtstag": datetime.datetime.strptime(row[4], '%Y-%m-%d'),
                    "Beruf": row[5],
                    "Beschreibung": row[6],
                    "Adresse_ID": id_mapping_adressen[int(row[7])]  # Verknüpfung mit Adress-ID
                }
                db.personen.insert_one(person)

            elif row[0] == 'Kenntnisse':
                nutzer_id = int(row[1])  # Nutzer-ID aus CSV
                kenntnis = row[2]  # Die spezifische Kenntnis

                # Füge die Kenntnis dem zugehörigen Personendokument hinzu, indem die Nutzer-ID verwendet wird
                # Wir nehmen an, dass das Personendokument bereits eine Referenz auf die Nutzer-ID enthält
                person_document = db.personen.find_one({"Nutzer_ID": id_mapping_nutzer[nutzer_id]})
                if person_document:
                    db.personen.update_one(
                        {"_id": person_document['_id']},
                        {"$push": {"kenntnisse": kenntnis}}
                    )

            elif row[0] == 'Unternehmen':
                unternehmen = {
                    "NutzerID": id_mapping_nutzer[int(row[1])],
                    "Name": row[2],
                    "Branche": row[3],
                    "Groesse": row[4],
                    "Gruendungsjahr": row[5],
                    "Standorte": [],
                    "Stellenangebote": []
                }
                db.unternehmen.insert_one(unternehmen)

            elif row[0] == 'Standort':
                standort = {
                    "Standortname": row[1],
                    "AdresseID": id_mapping_adressen[int(row[2])]
                }
                standort_id = current_standort_id
                id_mapping_standort[standort_id] = standort
                current_standort_id += 1
                # Füge Standort zum entsprechenden Unternehmen hinzu
                db.unternehmen.update_one(
                    {"NutzerID": id_mapping_nutzer[int(row[3])]},
                    {"$push": {"Standorte": standort}}
                )
            elif row[0] == 'Stellenangebot':
                stellenangebot = {
                    "StandortID": id_mapping_standort[int(row[1])],  # Referenz zum Standort-Objekt
                    "Beschreibung": row[2],
                    "Titel": row[3]
                }
                # Füge Stellenangebot zum entsprechenden Unternehmen hinzu
                db.unternehmen.update_one(
                    {"NutzerID": id_mapping_nutzer[int(row[4])]},
                    {"$push": {"Stellenangebote": stellenangebot}}
                )
            elif row[0] == 'NutzerBeziehungen':
                nutzerbeziehung = {
                    "NutzerID1": id_mapping_nutzer[int(row[1])],  # Verknüpfung mit Nutzer-ID1
                    "NutzerID2": id_mapping_nutzer[int(row[2])],  # Verknüpfung mit Nutzer-ID2
                    "Beziehungsart": row[3]  # Art der Beziehung
                }
                db.nutzerbeziehungen.insert_one(nutzerbeziehung)
        # Speichern der Dictionaries in einer JSON-Datei
        save_dictionaries()



def clear_data():
    client.drop_database('meinedatenbank')
    print("Datenbank wurde gelöscht.")


def get_execution_time(db, collection_name, pipeline):
    db.nutzerbeziehungen.aggregate(pipeline)
    try:
        # Startzeit erfassen
        start_time = time.time()
        cursor = db[collection_name].aggregate(pipeline)

        # Cursor vollständig durchlaufen, um sicherzustellen, dass die Aggregation abgeschlossen ist
        for _ in cursor:
            pass

        # Endzeit erfassen
        end_time = time.time()

        # Ausführungszeit berechnen
        execution_time = end_time - start_time

        return execution_time
    except Exception as e:
        raise Exception(f"Error executing the aggregation: {e}")

#Es gibt zwei Methoden execute_query1
#Die erste wird für performance vergleich genutzt und gibt die tatsächlichen Objektreferenzen der Kontakte zweiten Grades
# Die zweite ist für Demonstrationszwecke und gibt die reverse_gemappte ID aus

def execute_query1(nutzer_object_id):
    pipeline = [
        # Finde alle direkten Kontakte des Nutzers
        {
            "$match": {"NutzerID1": nutzer_object_id}
        },
        # Verbinde die Beziehungen, um die Kontakte zweiten Grades zu finden
        {
            "$lookup": {
                "from": "nutzerbeziehungen",
                "localField": "NutzerID2",
                "foreignField": "NutzerID1",
                "as": "second_degree_contacts"
            }
        },
        {
            "$unwind": "$second_degree_contacts"
        },
        # Schließe direkte Kontakte und den Nutzer selbst aus
        {
            "$match": {
                "second_degree_contacts.NutzerID2": {"$ne": nutzer_object_id}
            }
        },
        # Überprüfe, ob es eine direkte Rückverbindung zum ursprünglichen Nutzer gibt
        {
            "$lookup": {
                "from": "nutzerbeziehungen",
                "localField": "second_degree_contacts.NutzerID2",
                "foreignField": "NutzerID2",
                "as": "check_back_reference"
            }
        },
        {
            "$match": {
                "check_back_reference.NutzerID1": {"$ne": nutzer_object_id}
            }
        },
        # Projiziere die Kontakte zweiten Grades
        {
            "$project": {
                "_id": 0,
                "KontaktZweitenGrades": "$second_degree_contacts.NutzerID2"
            }
        },
        # Gruppiere die Ergebnisse, um Duplikate zu entfernen
        {
            "$group": {
                "_id": "$KontaktZweitenGrades"
            }
        }
    ]

    #results = list(db.nutzerbeziehungen.aggregate(pipeline))
    #id_mapping_nutzer_reverse = {v: k for k, v in id_mapping_nutzer.items()}  # Umgekehrtes Mapping-Dictionary

    #for result in results:
       # original_id = id_mapping_nutzer_reverse.get(result['_id'], "ID nicht gefunden")
       # print(f"Kontakt zweiten Grades: {original_id}")

    execution_time_ms = get_execution_time(db, "nutzerbeziehungen", pipeline)
    return execution_time_ms


def execute_query2(gesuchte_kenntnis):
    # Aggregationspipeline
    pipeline = [
        {
            "$match": {
                "kenntnisse": gesuchte_kenntnis  # Nutzt die Variable für den Filter
            }
        },
        {
            "$project": {
                "Nutzer_ID": 1,
                "Vorname": 1,
                "Nachname": 1,
                "Kenntnisse": {
                    "$filter": {
                        "input": "$kenntnisse",
                        "as": "kenntnis",
                        "cond": {"$eq": ["$$kenntnis", gesuchte_kenntnis]}  # Nutzt die Variable für den spezifischen Filter
                    }
                }
            }
        }
    ]

    # Ausführen der Pipeline
    #results = list(db.personen.aggregate(pipeline))

    # Ergebnisse ausgeben
    #for result in results:
        #print(result)

    execution_time_ms = get_execution_time(db, "personen", pipeline)
    return execution_time_ms




def execute_query3(unternehmensname):
    # Aggregationspipeline
    pipeline = [
        {
            "$match": {
                "Name": unternehmensname  # Filtert die Dokumente nach dem Unternehmensnamen
            }
        },
        {
            "$unwind": {
                "path": "$Stellenangebote",
                "preserveNullAndEmptyArrays": True  # Stellen sicher, dass Unternehmen ohne Stellenangebote in der Zählung als 0 erscheinen
            }
        },
        {
            "$group": {
                "_id": "$Name",
                "Anzahl_der_Stellenangebote": {"$sum": 1}  # Summiert die Anzahl der Stellenangebote
            }
        }
    ]

    # Ausführen der Pipeline
    #results = list(db.unternehmen.aggregate(pipeline))

    # Ergebnisse ausgeben
    #if results:
        #for result in results:
           # print(f"Unternehmen: {result['_id']}, Anzahl der offenen Stellenangebote: {result['Anzahl_der_Stellenangebote']}")
    #else:
        #print("Keine Stellenangebote gefunden oder Unternehmen existiert nicht.")

    execution_time_ms = get_execution_time(db, "personen", pipeline)
    return execution_time_ms


def get_user_info(nutzer_object_id):
    if isinstance(nutzer_object_id, str):
        nutzer_object_id = ObjectId(nutzer_object_id)

    user_info = db.nutzer.find_one({"_id": nutzer_object_id})
    if user_info:
        print("Nutzerinformationen:", user_info)
    else:
        print("Nutzer nicht gefunden")



def get_direct_relationships(nutzer_object_id):

    pipeline = [
        # Finde alle direkten Beziehungen des Nutzers
        {
            "$match": {"NutzerID1": nutzer_object_id}
        },
        # Verbinde die Beziehungen mit den Nutzern
        {
            "$lookup": {
                "from": "nutzer",
                "localField": "NutzerID2",
                "foreignField": "_id",
                "as": "direct_contacts"
            }
        },
        {
            "$unwind": "$direct_contacts"
        },
        # Projiziere die Nutzerdaten
        {
            "$project": {
                "_id": 0,
                "NutzerID1": 1,
                "NutzerID2": 1,
                "Beziehungsart": 1,
                "DirectContact": "$direct_contacts"
            }
        }
    ]

    results = list(db.nutzerbeziehungen.aggregate(pipeline))
    if results:
        for result in results:
            print("Direkter Kontakt:", result["DirectContact"])
    else:
        print("Keine direkten Kontakte gefunden")

    results = list(db.nutzerbeziehungen.aggregate(pipeline))
    for result in results:
        print("Direkter Kontakt:", result["DirectContact"])

def check_nutzerbeziehungen():
    relationships = db.nutzerbeziehungen.find()
    for relationship in relationships:
        print(relationship)

def main():

    # Statische Variablen für Unternehmensnamen und Kenntnisse
    unternehmensname = "Tech Solutions"
    kenntnis = "TopTeamfähigkeit"
    nutzer_object_id = 0
    arrayQuery1 = [0] * 10
    arrayQuery2 = [0] * 10
    arrayQuery3 = [0] * 10




    try:
        for index, file_path in enumerate(data_files):
            print(f"Processing file: {file_path}")

            # Schritt 1: Alle Tabellen droppen
            clear_data()

            # Schritt 2: Daten einspielen
            load_data(file_path)

            # Schritt 3: Laden der Dictionaries aus der JSON-Datei
            load_dictionaries()
            nutzer_object_id = id_mapping_nutzer['1']  # Die ObjectId des Nutzers
            # Schritt 4: Anfragen ausführen und Zeit messen

            for i in range(10):
                arrayQuery1[i] = execute_query1(nutzer_object_id)


            for i in range(10):
                arrayQuery2[i] = execute_query2(kenntnis)



            for i in range(10):
                arrayQuery3[i] = execute_query3(unternehmensname)

            # Durchschnittszeiten berechnen
            avg_time_query1 = sum(arrayQuery1) / len(arrayQuery1)
            avg_time_query2 = sum(arrayQuery2) / len(arrayQuery2)
            avg_time_query3 = sum(arrayQuery3) / len(arrayQuery3)

            # Ergebnisse in eine Datei schreiben
            output_filename = f'mongodb_query_execution_times_{index}.txt'
            with open(output_filename, 'w') as file:
                file.write('Query1 Ausführungszeiten:\n')
                for time in arrayQuery1:
                    file.write(f'{time}\n')
                file.write(f'Durchschnittszeit Query1: {avg_time_query1}\n\n')

                file.write('Query2 Ausführungszeiten:\n')
                for time in arrayQuery2:
                    file.write(f'{time}\n')
                file.write(f'Durchschnittszeit Query2: {avg_time_query2}\n\n')

                file.write('Query3 Ausführungszeiten:\n')
                for time in arrayQuery3:
                    file.write(f'{time}\n')
                file.write(f'Durchschnittszeit Query3: {avg_time_query3}\n\n')

            print(f"Results written to {output_filename}")

    except errors.PyMongoError as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("MongoDB connection is closed")


if __name__ == '__main__':
    main()
