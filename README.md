# Moderne Datenbanken - Vergleichsprojekt

Ein Performance-Vergleichsprojekt zwischen relationalen (MySQL) und NoSQL (MongoDB) Datenbanken mit automatisierter Datengenerierung und Abfragemessung.

## 📋 Übersicht

Dieses Projekt vergleicht die Leistung von MySQL und MongoDB anhand eines realistischen Datenschemas, das ein soziales Netzwerk mit Nutzern, Unternehmen, Standorten und Stellenangeboten simuliert.

## 🏗️ Projektstruktur

```
Moderne-Datenbanken-Projekt/
├── src/
│   ├── fake.py                  # Generierung von Testdaten
│   ├── main_mysql.py            # MySQL-Implementierung
│   ├── main_mogodb.py           # MongoDB-Implementierung
│   ├── mappings.json            # ID-Mappings zwischen Datenbanken
│   └── query_execution_times*.txt  # Messergebnisse
├── LICENSE
└── README.md
```

## 🗄️ Datenbankschema

### Entitäten

- **Nutzer**: Personen und Unternehmen mit Profilinformationen
- **Person**: Individuelle Nutzer mit persönlichen Daten
- **Unternehmen**: Unternehmensprofile mit Branche und Größe
- **Adresse**: Standortdaten (Straße, PLZ, Stadt, Land)
- **Standort**: Geschäftsstandorte von Unternehmen
- **Stellenangebot**: Job-Postings an verschiedenen Standorten
- **Kenntnisse**: Skills und Fähigkeiten der Nutzer
- **NutzerBeziehungen**: Verbindungen zwischen Nutzern

## 🚀 Features

### Datengenerierung
- Automatische Generierung realistischer Testdaten mit der Faker-Bibliothek
- Konfigurierbare Datenmengen (statische und skalierbare Datensätze)
- Blockweise Datengenerierung für große Datenmengen

### Datenbank-Implementierungen

#### MySQL (Relational)
- Normalisiertes Schema mit Fremdschlüsseln
- SQL-Abfragen mit JOINs
- Transaktionale Integrität

#### MongoDB (NoSQL)
- Eingebettete Dokumente und Referenzen
- Flexibles Schema
- Aggregation Pipeline
- ObjectId-Mapping für Referenzen

## 📊 Performance-Messung

Das Projekt misst und vergleicht die Ausführungszeiten für:
- INSERT-Operationen
- SELECT-Abfragen (einfach und komplex)
- JOIN/Aggregations-Operationen
- Suchoperationen

Ergebnisse werden in Textdateien gespeichert:
- `query_execution_times.txt` (MySQL)
- `mongodb_query_execution_times.txt` (MongoDB)

## 🛠️ Installation & Setup

### Voraussetzungen

- Python 3.x
- MySQL Server
- MongoDB Server
- Docker (optional)

### Python-Abhängigkeiten

```bash
pip install faker mysql-connector-python pymongo
```

### Datenbank-Konfiguration

#### MySQL
```python
# In main_mysql.py anpassen
connection = mysql.connector.connect(
    host='localhost',
    user='dein_username',
    password='dein_passwort',
    database='deine_datenbank'
)
```

#### MongoDB
```python
# In main_mogodb.py anpassen
client = MongoClient('mongodb://mongouser:mongopassword@localhost:27017/')
```

## 🎮 Verwendung

### 1. Testdaten generieren

```python
python src/fake.py
```

Passt den `output_dir` in [fake.py](src/fake.py) an eure lokale Umgebung an.

### 2. MySQL-Datenbank initialisieren

```python
python src/main_mysql.py
```

### 3. MongoDB-Datenbank initialisieren

```python
python src/main_mogodb.py
```

### 4. Ergebnisse analysieren

Die Ausführungszeiten werden automatisch in den entsprechenden Textdateien protokolliert.

## 📈 Datenmodell

### Relationales Modell (MySQL)
```
Nutzer (NutzerID, Info, Email, NutzerTyp, ...)
├── Person (NutzerID FK, Vorname, Nachname, AdresseID FK, ...)
├── Unternehmen (NutzerID FK, Name, Branche, ...)
├── Kenntnisse (NutzerID FK, Kenntnis)
└── NutzerBeziehungen (NutzerID1 FK, NutzerID2 FK, Beziehungsart)

Standort (StandortID, Standortname, AdresseID FK, NutzerID FK)
└── Stellenangebot (StellenID, StandortID FK, Beschreibung, NutzerID FK)

Adresse (AdresseID, Strasse, PLZ, Stadt, Land)
```

### Dokumentenmodell (MongoDB)
```javascript
// Eingebettetes Dokument mit Referenzen
{
  _id: ObjectId,
  NutzerTyp: "Person" | "Unternehmen",
  Info: { ... },
  // Eingebettete Daten
  Adresse: { Strasse, PLZ, Stadt, Land },
  Kenntnisse: [ ... ],
  // Referenzen
  Standorte: [ ObjectId, ... ],
  Beziehungen: [ ... ]
}
```

## 🔧 Konfiguration

### Testdaten-Parameter

In [fake.py](src/fake.py#L7):
- `base_num_records`: Basis-Anzahl der Datensätze
- `static_companies`: Anzahl statischer Unternehmen
- `static_persons`: Anzahl statischer Personen
- `block_num`: Multiplikator für Datenmenge

## 📝 Lizenz

Dieses Projekt steht unter der entsprechenden Lizenz (siehe LICENSE).

## 👥 Autoren

Hochschulprojekt - FH Dortmund  
Kurs: Moderne Datenbanken, Semester 6

## 🤝 Beitragen

Dieses ist ein akademisches Projekt. Für Verbesserungsvorschläge oder Fragen, bitte ein Issue erstellen.

## 📚 Weitere Informationen

### Verwendete Technologien

- **Python**: Hauptprogrammiersprache
- **Faker**: Generierung realistischer Testdaten
- **MySQL**: Relationale Datenbank
- **MongoDB**: NoSQL-Dokumentendatenbank
- **mysql-connector-python**: MySQL-Python-Connector
- **pymongo**: MongoDB-Python-Driver

### Benchmark-Szenarien

Das Projekt testet verschiedene Anwendungsfälle:
1. Massendatenimport
2. Einfache Selektionen
3. Komplexe Joins/Aggregationen
4. Suche über mehrere Felder
5. Beziehungsabfragen

---

**Hinweis**: Pfade in den Skripten müssen an die lokale Umgebung angepasst werden (z.B. `output_dir` in fake.py und Datenbankverbindungen in den Hauptdateien).
