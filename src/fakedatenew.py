from faker import Faker
import random

fake = Faker()

# Dateipfad, in dem die Ergebnisse gespeichert werden
output_file_path = "C:/Users/FHBBook/OneDrive - FH Dortmund/Informatik Studium/Semester 6/Moderne Datenbanken/Projekt/testdaten/dataset.txt"

skills_list = [fake.word() for _ in range(50)]  # Erstellen von 50 einzigartigen Kenntnissen



# Bestimmen der Anzahl der Unternehmen
num_companies = random.randint(100, 200)
company_ids = set(random.sample(range(1, 601), num_companies))
person_ids = [id for id in range(1, 601) if id not in company_ids]

# Datei öffnen zum Schreiben
with open(output_file_path, 'w') as file:
    # Adressen
    for _ in range(800):
        # Entfernen von Kommas aus den Adressdaten, um Probleme beim CSV-Import zu vermeiden
        street = fake.street_address().replace(',', ' ')
        file.write(f"Adresse,{street},{fake.building_number()},{fake.postcode()},{fake.city()},{fake.country()}\n")
    # Schreibe zuerst alle Nutzer
    for user_id in range(1, 601):
        email = fake.unique.email()  # Verwende unique generator für Emails
        if user_id in company_ids:
            typ = 'Unternehmen'
        else:
            typ = 'Person'
        file.write(f"Nutzer,{fake.sentence()},{fake.domain_name()}/profile.jpg,{email},{typ},{fake.domain_name()}/banner.jpg\n")

    # Nachdem alle Nutzer geschrieben sind, fahre fort mit Personen und Unternehmen
    for user_id in range(1, 601):
        if user_id in company_ids:
            company = fake.company().replace(',', '')
            bs = fake.bs().replace(',', '')
            file.write(f"Unternehmen,{user_id},{company},{bs},{random.choice(['klein', 'mittel', 'groß'])},{random.randint(1900, 2021)}\n")
        else:
            first_name = fake.first_name().replace(',', '')
            last_name = fake.last_name().replace(',', '')
            job = fake.job().replace(',', '')
            bio = fake.text(max_nb_chars=50).replace(',', '')
            file.write(f"Person,{user_id},{first_name},{last_name},{fake.date_of_birth()},'{job}','{bio}',{random.randint(1, 800)}\n")
            # Zuweisung von Kenntnissen
            person_skills = set()
            num_skills = random.randint(3, 7)
            while len(person_skills) < num_skills:
                skill = random.choice(skills_list)
                if skill not in person_skills:
                    person_skills.add(skill)
                    file.write(f"Kenntnisse,{user_id},{skill}\n")

    # Standorte
    for _ in range(400):
        # Einfache Zusammenstellung der Standortnamen
        file.write(f"Standort,{fake.city()} {fake.street_suffix()}, {random.randint(1, 800)}, {random.randint(1, 600)}\n")

    # Stellenangebote
    for _ in range(200):
        title = fake.job().replace(',', '')  # Jobbezeichnung ohne Kommas
        desc = fake.sentence().replace(',', '')  # Beschreibung ohne Kommas
        company_id = random.choice(list(company_ids))  # Wähle eine zufällige Unternehmens-ID
        file.write(f"Stellenangebot,{random.randint(1, 400)},{desc},{title},{company_id}\n")


    # NutzerBeziehungen
    #for _ in range(2000):
     #   relationship = fake.word().replace(',', '')  # Beziehungstyp ohne Kommas
    #    file.write(f"NutzerBeziehungen,{random.randint(1, 600)},{random.randint(1, 600)},{relationship}\n")

    # NutzerBeziehungen
    user_relationships = set()
    while len(user_relationships) < 2000:
        id1, id2 = random.randint(1, 600), random.randint(1, 600)
        if id1 != id2:
            relationship = (id1, id2)
            if relationship not in user_relationships and (id2, id1) not in user_relationships:
                user_relationships.add(relationship)
                file.write(f"NutzerBeziehungen,{id1},{id2},{fake.word().replace(',', '')}\n")
