import mysql.connector
from mysql.connector import Error
import time

setup_path = r"C:\Users\FHBBook\OneDrive - FH Dortmund\Informatik Studium\Semester 6\Moderne Datenbanken\Projekt\databases\mysql-init\setup.sql"

data_path = "C:/Users/FHBBook/OneDrive - FH Dortmund/Informatik Studium/Semester 6/Moderne Datenbanken/Projekt/testdaten/dataset.txt"


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


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_query_with_param(connection, query, params):
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        result = cursor.fetchall()
        for row in result:
            print(row)
    except Error as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()


def show_all_tables(connection):
    query = "SHOW TABLES"
    execute_query(connection, query)


def drop_all_tables(connection):
    cursor = connection.cursor()
    tables = ['NutzerBeziehungen', 'Kenntnisse', 'Stellenangebot', 'Standort', 'Unternehmen', 'Person', 'Adresse',
              'Nutzer']
    for table_name in tables:
        drop_table_query = f"DROP TABLE IF EXISTS {table_name}"
        try:
            cursor.execute(drop_table_query)
            print(f"Table {table_name} dropped successfully.")
        except Error as e:
            print(f"Failed to drop table {table_name}: {e}")
    connection.commit()


def create_triggers(connection):
    cursor = connection.cursor()
    triggers = [
        """
        CREATE TRIGGER CheckNutzerTypeBeforeInsert
        BEFORE INSERT ON Standort
        FOR EACH ROW
        BEGIN
            DECLARE v_nutzertyp VARCHAR(255);
            SELECT NutzerTyp INTO v_nutzertyp FROM Nutzer WHERE NutzerID = NEW.NutzerID;
            IF v_nutzertyp != 'Unternehmen' THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nur Unternehmen können Standorte haben';
            END IF;
        END;
        """,
        """
        CREATE TRIGGER CheckNutzerTypeBeforeUpdate
        BEFORE UPDATE ON Standort
        FOR EACH ROW
        BEGIN
            DECLARE v_nutzertyp VARCHAR(255);
            SELECT NutzerTyp INTO v_nutzertyp FROM Nutzer WHERE NutzerID = NEW.NutzerID;
            IF v_nutzertyp != 'Unternehmen' THEN
                SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Nur Unternehmen können Standorte haben';
            END IF;
        END;
        """
    ]
    for trigger in triggers:
        try:
            cursor.execute(trigger)
            print("Trigger created successfully")
        except Error as e:
            print(f"Failed to create trigger: {e}")
    connection.commit()


def execute_script_from_file(connection, file_path):
    cursor = connection.cursor()
    with open(file_path, 'r') as file:
        sql_script = file.read()
    commands = sql_script.split(';')
    for command in commands:
        if command.strip():
            try:
                cursor.execute(command)
            except Error as e:
                print(f"Failed to execute command: {command}\nError: {e}")
    connection.commit()
    print("Script executed successfully")


def insert_data_from_file(connection, file_path):
    queries = {
        'Nutzer': "INSERT INTO Nutzer (Info,Profilbild,Email, NutzerTyp,Bannerbild) VALUES (%s, %s, %s, %s, %s)",
        'Person': "INSERT INTO Person (NutzerID, Vorname, Nachname, Geburtsdatum, Beruf, Bildungsabschluss, AdresseID) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        'Unternehmen': "INSERT INTO Unternehmen (NutzerID, Name, Branche, Groesse, Gruendungsjahr) VALUES (%s, %s, %s, %s, %s)",
        'Adresse': "INSERT INTO Adresse (Strasse, Hausnummer, PLZ, Stadt, Land) VALUES (%s, %s, %s, %s, %s)",
        'Standort': "INSERT INTO Standort (Standortname, AdresseID, NutzerID) VALUES (%s, %s, %s)",
        'Stellenangebot': "INSERT INTO Stellenangebot (StandortID,Beschreibung,Titel, NutzerID) VALUES (%s, %s, %s, %s)",
        'Kenntnisse': "INSERT INTO Kenntnisse (NutzerID, Kenntnis) VALUES (%s, %s)",
        'NutzerBeziehungen': "INSERT INTO NutzerBeziehungen (NutzerID1, NutzerID2, Beziehungsart) VALUES (%s, %s, %s)"
    }

    with open(file_path, 'r') as file:
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
    except Error as e:
        print(f"The error '{e}' occurred: {e} \n query: '{query}' \n data: '{data}'")


def main():
    connection = create_connection(
        "localhost",  # Hostname, wenn Docker lokal läuft und Ports weitergeleitet sind
        "myuser",  # MYSQL_USER, wie im Docker Compose definiert
        "mypassword",  # MYSQL_PASSWORD, wie im Docker Compose definiert
        "mydatabase"  # MYSQL_DATABASE, wie im Docker Compose definiert
    )
    # Uncomment the method calls below as needed to perform the operations.
    #show_all_tables(connection)
    #drop_all_tables(connection)
    #execute_script_from_file(connection, setup_path)
    #insert_data_from_file(connection, data_path)

    #Anfrage 1 Anfrage mit rekursiver Beziehung: Ermitteln Sie alle Kontakte zweiten Grades eines Benutzers.

    query1 = '''
                SELECT DISTINCT nb2.NutzerID2 AS KontaktZweitenGrades
                FROM NutzerBeziehungen nb1
                JOIN NutzerBeziehungen nb2 ON nb1.NutzerID2 = nb2.NutzerID1
                LEFT JOIN NutzerBeziehungen nb3 ON nb2.NutzerID2 = nb3.NutzerID2 AND nb3.NutzerID1 = %s
                WHERE nb1.NutzerID1 = %s AND nb2.NutzerID2 != %s AND nb3.NutzerID2 IS NULL;
            '''

    user_id = 402
    start_time = time.time()
    execute_query_with_param(connection, query1, (user_id, user_id, user_id))
    end_time = time.time()
    print(f"Query Execution Time: {end_time - start_time:.4f} seconds")

    execute_query(connection, "SELECT * FROM Nutzer WHERE NutzerID = 402")



    #Anfrage 2 Anfrage mit mehrwertigem Attribut: Finden Sie alle Benutzer, die eine spezifische Fähigkeit besitzen (z.B. "Python").

    #Ermitteln welche Kenntnisse es gibt:
    prequery = '''      SELECT 
                        n.NutzerID, 
                        p.Vorname, 
                        p.Nachname, 
                        k.Kenntnis
                    FROM 
                        Nutzer n
                    JOIN 
                        Person p ON n.NutzerID = p.NutzerID
                    JOIN 
                        Kenntnisse k ON n.NutzerID = k.NutzerID
                    ORDER BY 
                        k.Kenntnis;'''
    #execute_query(connection, prequery)

    query2 = '''SELECT p.NutzerID, p.Vorname, p.Nachname, k.Kenntnis
                FROM Person p
                JOIN Kenntnisse k ON p.NutzerID = k.NutzerID
                WHERE k.Kenntnis = 'word';'''
    start_time = time.time()
    #execute_query(connection, query2)
    end_time = time.time()
    #print(f"Query Execution Time: {end_time - start_time:.4f} seconds")

    #Anfrage 3 Aggregation Funktion: Anzahl der offenen Stellenangebote eines bestimmten Unternehmen.

    prequery3 = '''SELECT JobID, Titel, Beschreibung, NutzerID, StandortID
                   FROM Stellenangebot ORDER BY NutzerID;
                '''



    #execute_query(connection, prequery3)
    #execute_query(connection, "Select * from Unternehmen where NutzerID = 560;")




    query3 = '''
            SELECT COUNT(*) AS AnzahlOffeneStellen
            FROM Stellenangebot
            JOIN Unternehmen ON Stellenangebot.NutzerID = Unternehmen.NutzerID
            WHERE Unternehmen.Name = %s;
            '''


    unternehmensname = "Solomon-Beck"

    start_time = time.time()
    #execute_query_with_param(connection, query3, (unternehmensname,))
    end_time = time.time()
    #print(f"Query Execution Time: {end_time - start_time:.4f} seconds")

    connection.close()


if __name__ == "__main__":
    main()
