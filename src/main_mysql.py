import mysql.connector
import time
import os
from mysql.connector import Error

# Deine Methoden
def drop_all_tables(connection):
    cursor = connection.cursor()
    tables = ["NutzerBeziehungen", "Kenntnisse", "Stellenangebot", "Standort", "Person", "Unternehmen", "Adresse", "Nutzer"]
    for table in tables:
        try:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            connection.commit()
        except mysql.connector.Error as e:
            print(f"The error '{e}' occurred while dropping table {table}")

def execute_script_from_file(connection, setup_path):
    cursor = connection.cursor()
    with open(setup_path, 'r') as file:
        script = file.read()
    statements = script.split(';')
    try:
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred while executing the script")

def insert_data_from_file(connection, data_path):
    queries = {
        'Nutzer': "INSERT INTO Nutzer (Info, Profilbild, Email, NutzerTyp, Bannerbild) VALUES (%s, %s, %s, %s, %s)",
        'Person': "INSERT INTO Person (NutzerID, Vorname, Nachname, Geburtsdatum, Beruf, Bildungsabschluss, AdresseID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        'Unternehmen': "INSERT INTO Unternehmen (NutzerID, Name, Branche, Groesse, Gruendungsjahr) VALUES (%s, %s, %s, %s, %s)",
        'Adresse': "INSERT INTO Adresse (Strasse, Hausnummer, PLZ, Stadt, Land) VALUES (%s, %s, %s, %s, %s)",
        'Standort': "INSERT INTO Standort (Standortname, AdresseID, NutzerID) VALUES (%s, %s, %s)",
        'Stellenangebot': "INSERT INTO Stellenangebot (StandortID, Beschreibung, Titel, NutzerID) VALUES (%s, %s, %s, %s)",
        'Kenntnisse': "INSERT INTO Kenntnisse (NutzerID, Kenntnis) VALUES (%s, %s)",
        'NutzerBeziehungen': "INSERT INTO NutzerBeziehungen (NutzerID1, NutzerID2, Beziehungsart) VALUES (%s, %s, %s)"
    }

    with open(data_path, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            record_type = data[0]
            record_data = data[1:]
            query = queries.get(record_type)
            if query:
                execute_dataquery(connection, query, tuple(record_data))

def execute_dataquery(connection, query, data):
    cursor = connection.cursor()
    try:
        cursor.execute(query, data)
        connection.commit()
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred: {e} \n query: '{query}' \n data: '{data}'")

def execute_query_with_param(connection, query, params):
    cursor = connection.cursor()
    start_time = time.time()
    cursor.execute(query, params)
    end_time = time.time()
    result = cursor.fetchall()
    elapsed_time = end_time - start_time
    print(f"Query: {query}")
    print(f"Params: {params}")
    print(f"Result: {result}")
    print(f"Time: {elapsed_time:.4f} seconds")
    return elapsed_time

def execute_query(connection, query):
    cursor = connection.cursor()
    start_time = time.time()
    cursor.execute(query)
    result = cursor.fetchall()
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Query: {query}")
    print(f"Result: {result}")
    print(f"Time: {elapsed_time:.4f} seconds")
    return elapsed_time

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

def get_execution_time():
    return 0

def main():
    connection = create_connection(
        "localhost",  # Hostname, wenn Docker lokal läuft und Ports weitergeleitet sind
        "myuser",  # MYSQL_USER, wie im Docker Compose definiert
        "mypassword",  # MYSQL_PASSWORD, wie im Docker Compose definiert
        "mydatabase"  # MYSQL_DATABASE, wie im Docker Compose definiert
    )

    setup_path = r"C:\Users\FHBBook\OneDrive - FH Dortmund\Informatik Studium\Semester 6\Moderne Datenbanken\Projekt\databases\mysql-init\setup.sql"
    data_dir = "C:/Users/FHBBook/OneDrive - FH Dortmund/Informatik Studium/Semester 6/Moderne Datenbanken/Projekt/testdaten/"
    data_files = [os.path.join(data_dir, f) for f in os.listdir(data_dir) if f.startswith("dataset_block")]

    query1 = "SELECT DISTINCT nb2.NutzerID2 AS KontaktZweitenGrades FROM NutzerBeziehungen nb1 JOIN NutzerBeziehungen nb2 ON nb1.NutzerID2 = nb2.NutzerID1 LEFT JOIN NutzerBeziehungen nb3 ON nb2.NutzerID2 = nb3.NutzerID2 AND nb3.NutzerID1 = %s WHERE nb1.NutzerID1 = %s AND nb2.NutzerID2 != %s AND nb3.NutzerID2 IS NULL;"
    query2 = "SELECT p.NutzerID, p.Vorname, p.Nachname, k.Kenntnis FROM Person p JOIN Kenntnisse k ON p.NutzerID = k.NutzerID WHERE k.Kenntnis = %s;"
    query3 = "SELECT COUNT(*) AS AnzahlOffeneStellen FROM Stellenangebot JOIN Unternehmen ON Stellenangebot.NutzerID = Unternehmen.NutzerID WHERE Unternehmen.Name = %s;"

    # Statische Variablen für Unternehmensnamen und Kenntnisse
    unternehmensname = "Tech Solutions"
    kenntnis = "TopTeamfähigkeit"
    user_id = 1

    try:
        for index, data_path in enumerate(data_files):
            print(f"Processing file: {data_path}")

            # Schritt 1: Alle Tabellen droppen
            drop_all_tables(connection)

            # Schritt 2: Schema einspielen
            execute_script_from_file(connection, setup_path)

            # Schritt 3: Daten einspielen
            insert_data_from_file(connection, data_path)

            # Schritt 4: Anfragen ausführen und Zeit messen

            print("Executing query 1...")
            query1_time = execute_query_with_param(connection, query1, (user_id, user_id, user_id))

            print("Executing query 2...")
            query2_time = execute_query_with_param(connection, query2, (kenntnis,))

            print("Executing query 3...")
            query3_time = execute_query_with_param(connection, query3, (unternehmensname,))

            print(f"Results for {data_path}:")
            print(f"Query 1 time: {query1_time:.4f} seconds")
            print(f"Query 2 time: {query2_time:.4f} seconds")
            print(f"Query 3 time: {query3_time:.4f} seconds")

    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    main()
