from faker import Faker
import random
import os

fake = Faker()

output_dir = "C:/Users/FHBBook/OneDrive - FH Dortmund/Informatik Studium/Semester 6/Moderne Datenbanken/Projekt/testdaten/"

def generate_data_block(block_num, base_num_records):
    # Anzahl der statischen Datensätze
    static_companies = 10
    static_persons = 10
    static_users = static_companies + static_persons
    static_addresses = 30
    static_standorte = 10
    static_stellenangebote = 20
    static_relationships = 20
    static_skills = 10

    skills_list = [fake.word() for _ in range(50)]
    num_records = base_num_records * block_num
    num_companies = random.randint(100, 200) * block_num
    company_ids = set(random.sample(range(1 + static_users, num_records + 1 + static_users), num_companies))
    person_ids = [id for id in range(1 + static_users, num_records + 1+static_users) if id not in company_ids]
    user_id = static_users

    output_file_path = os.path.join(output_dir, f"dataset_block_{block_num}.txt")



    with open(output_file_path, 'w') as file:

        file.write(f"Adresse,Maple Street,45,12345,Springfield,USA\n")
        file.write(f"Adresse,Oak Avenue,78,67890,Shelbyville,USA\n")
        file.write(f"Adresse,Pine Lane,123,10101,Capital City,USA\n")
        file.write(f"Adresse,Elm Boulevard,56,20202,Ogdenville,USA\n")
        file.write(f"Adresse,Birch Road,89,30303,North Haverbrook,USA\n")
        file.write(f"Adresse,Ash Street,12,40404,Brockway,USA\n")
        file.write(f"Adresse,Cedar Drive,34,50505,Monroe,USA\n")
        file.write(f"Adresse,Willow Court,67,60606,Westfield,USA\n")
        file.write(f"Adresse,Chestnut Avenue,90,70707,Eastwood,USA\n")
        file.write(f"Adresse,Maple Lane,23,80808,South Park,USA\n")
        file.write(f"Adresse,Poplar Street,56,90909,Northfield,USA\n")
        file.write(f"Adresse,Fir Avenue,78,10101,Springwood,USA\n")
        file.write(f"Adresse,Redwood Road,34,11111,Eastvale,USA\n")
        file.write(f"Adresse,Hemlock Boulevard,12,12121,Westport,USA\n")
        file.write(f"Adresse,Spruce Street,45,13131,Midvale,USA\n")
        file.write(f"Adresse,Sequoia Avenue,67,14141,Bridgeport,USA\n")
        file.write(f"Adresse,Maple Court,89,15151,Fairview,USA\n")
        file.write(f"Adresse,Oak Drive,12,16161,Lakewood,USA\n")
        file.write(f"Adresse,Pine Street,34,17171,Clearwater,USA\n")
        file.write(f"Adresse,Elm Lane,56,18181,Riverside,USA\n")
        file.write(f"Adresse,Birch Boulevard,78,19191,Greenwood,USA\n")
        file.write(f"Adresse,Ash Road,90,20202,Ironwood,USA\n")
        file.write(f"Adresse,Cedar Street,23,21212,Briarwood,USA\n")
        file.write(f"Adresse,Willow Avenue,45,22222,Mapleton,USA\n")
        file.write(f"Adresse,Chestnut Drive,67,23232,Brookfield,USA\n")
        file.write(f"Adresse,Maple Road,89,24242,Ridgewood,USA\n")
        file.write(f"Adresse,Poplar Boulevard,12,25252,Willowbrook,USA\n")
        file.write(f"Adresse,Fir Lane,34,26262,Creekside,USA\n")
        file.write(f"Adresse,Redwood Avenue,56,27272,Meadowbrook,USA\n")
        file.write(f"Adresse,Hemlock Road,78,28282,Sunnyvale,USA\n")

        file.write(f"Nutzer,Investigation manage project allow.,johnson-wells.com/profile.jpg,tonyadams@example.org,Person,wright.com/banner.jpg\n")
        file.write(f"Nutzer,Feeling organization measure fast.,miller.com/profile.jpg,larrybrown@example.net,Person,robinson.com/banner.jpg\n")
        file.write(f"Nutzer,Modernize thought consider produce.,smith-brown.org/profile.jpg,karenmorgan@example.net,Person,young.com/banner.jpg\n")
        file.write(f"Nutzer,Project everything away material much.,harris.com/profile.jpg,brianlee@example.org,Person,king.com/banner.jpg\n")
        file.write(f"Nutzer,Window prevent part style.,moore-wilson.com/profile.jpg,brandonwhite@example.com,Person,scott.com/banner.jpg\n")
        file.write(f"Nutzer,Maintain air free case open.,taylor-anderson.net/profile.jpg,carolchavez@example.net,Person,martin.com/banner.jpg\n")
        file.write(f"Nutzer,Kitchen treat among history.,thomas-jackson.org/profile.jpg,douglasthomas@example.org,Person,garcia.com/banner.jpg\n")
        file.write(f"Nutzer,Thousand operation remember.,lewis-lopez.com/profile.jpg,stevenbrown@example.com,Person,rodriguez.com/banner.jpg\n")
        file.write(f"Nutzer,Interesting early magazine trip.,walker.com/profile.jpg,donaldharris@example.net,Person,martinez.com/banner.jpg\n")
        file.write(f"Nutzer,Performance campaign line.,allen-thompson.org/profile.jpg,angeladavis@example.com,Person,hall.com/banner.jpg\n")
        file.write(f"Nutzer,Prepare player such kind.,young-king.com/profile.jpg,sarahmartinez@example.org,Person,lopez.com/banner.jpg\n")
        file.write(f"Nutzer,Development edge entire.,hernandez.com/profile.jpg,davidwright@example.net,Person,green.com/banner.jpg\n")
        file.write(f"Nutzer,Certain race follow process.,lee.com/profile.jpg,jenniferallen@example.org,Person,robinson.com/banner.jpg\n")
        file.write(f"Nutzer,Exist discuss former project.,clark-mitchell.org/profile.jpg,matthewhernandez@example.net,Person,walker.com/banner.jpg\n")
        file.write(f"Nutzer,Wide create force space.,rodriguez-white.com/profile.jpg,maryjohnson@example.org,Person,hall.com/banner.jpg\n")
        file.write(f"Nutzer,Figure nothing body news.,lewis.com/profile.jpg,paulmartinez@example.com,Person,allen.com/banner.jpg\n")
        file.write(f"Nutzer,Traditional professional notice institution.,hernandez.net/profile.jpg,lindawright@example.org,Person,king.com/banner.jpg\n")
        file.write(f"Nutzer,Theory hold politics health.,martin-walker.org/profile.jpg,robertyoung@example.net,Person,jones.com/banner.jpg\n")
        file.write(f"Nutzer,Meet science away age.,rodriguez-anderson.com/profile.jpg,susanmartin@example.org,Person,lee.com/banner.jpg\n")
        file.write(f"Nutzer,Try social order common.,robinson-allen.com/profile.jpg,davidgarcia@example.net,Person,harris.com/banner.jpg\n")

        file.write(f"Person,1,John,Doe,1985-05-15,Software Engineer,Bachelor,1\n")
        file.write(f"Person,2,Jane,Smith,1990-07-22,Data Scientist,Master,2\n")
        file.write(f"Person,3,Emily,Jones,1978-03-30,Project Manager,PhD,3\n")
        file.write(f"Person,4,Michael,Brown,1982-11-02,Graphic Designer,High School,4\n")
        file.write(f"Person,5,Ashley,Davis,1992-12-11,Accountant,Bachelor,5\n")
        file.write(f"Person,6,Joshua,Wilson,1988-09-19,Marketing Specialist,Master,6\n")
        file.write(f"Person,7,Megan,Moore,1995-01-25,Sales Manager,PhD,7\n")
        file.write(f"Person,8,Andrew,Taylor,1981-06-05,HR Manager,High School,8\n")
        file.write(f"Person,9,Olivia,Anderson,1976-04-13,Product Manager,Bachelor,9\n")
        file.write(f"Person,10,Daniel,Thomas,1987-08-21,Research Scientist,Master,10\n")

        file.write(f"Unternehmen,11,Tech Solutions,IT,mittel,2001\n")
        file.write(f"Unternehmen,12,Green Energy,Erneuerbare Energien,groß,1998\n")
        file.write(f"Unternehmen,13,Urban Builders,Bau,klein,2005\n")
        file.write(f"Unternehmen,14,Fresh Foods,Lebensmittel,mittel,2010\n")
        file.write(f"Unternehmen,15,Health Care Services,Gesundheit,groß,1992\n")
        file.write(f"Unternehmen,16,Finance Experts,Finanzen,mittel,2003\n")
        file.write(f"Unternehmen,17,Auto World,Automobil,klein,1999\n")
        file.write(f"Unternehmen,18,Global Travel,Reisen,groß,2015\n")
        file.write(f"Unternehmen,19,Media House,Medien,mittel,2000\n")
        file.write(f"Unternehmen,20,Creative Agency,Marketing,klein,2012\n")

        file.write(f"Kenntnisse,1,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,2,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,3,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,4,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,5,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,6,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,7,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,8,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,9,TopTeamfähigkeit\n")
        file.write(f"Kenntnisse,10,TopTeamfähigkeit\n")

        # Standorte für Nutzer-ID 11 bis 20
        file.write(f"Standort,Alpha Office,11,11\n")
        file.write(f"Standort,Beta Office,12,11\n")
        file.write(f"Standort,Gamma Office,13,12\n")
        file.write(f"Standort,Delta Office,14,12\n")
        file.write(f"Standort,Epsilon Office,15,13\n")
        file.write(f"Standort,Zeta Office,16,13\n")
        file.write(f"Standort,Eta Office,17,14\n")
        file.write(f"Standort,Theta Office,18,14\n")
        file.write(f"Standort,Iota Office,19,15\n")
        file.write(f"Standort,Kappa Office,20,15\n")
        file.write(f"Standort,Lambda Office,21,16\n")
        file.write(f"Standort,Mu Office,22,16\n")
        file.write(f"Standort,Nu Office,23,17\n")
        file.write(f"Standort,Xi Office,24,17\n")
        file.write(f"Standort,Omicron Office,25,18\n")
        file.write(f"Standort,Pi Office,26,18\n")
        file.write(f"Standort,Rho Office,27,19\n")
        file.write(f"Standort,Sigma Office,28,19\n")
        file.write(f"Standort,Tau Office,29,20\n")
        file.write(f"Standort,Upsilon Office,30,20\n")

        # Nutzerbeziehungen für Personen
        file.write(f"NutzerBeziehungen,1,2,Freund\n")
        file.write(f"NutzerBeziehungen,1,3,Freund\n")
        file.write(f"NutzerBeziehungen,1,4,Freund\n")
        file.write(f"NutzerBeziehungen,2,5,Freund\n")
        file.write(f"NutzerBeziehungen,2,6,Freund\n")
        file.write(f"NutzerBeziehungen,3,7,Freund\n")
        file.write(f"NutzerBeziehungen,3,8,Freund\n")
        file.write(f"NutzerBeziehungen,4,9,Freund\n")
        file.write(f"NutzerBeziehungen,4,10,Freund\n")

        # Nutzerbeziehungen für Unternehmen
        file.write(f"NutzerBeziehungen,11,12,Partner\n")
        file.write(f"NutzerBeziehungen,11,13,Partner\n")
        file.write(f"NutzerBeziehungen,11,14,Partner\n")
        file.write(f"NutzerBeziehungen,12,15,Partner\n")
        file.write(f"NutzerBeziehungen,12,16,Partner\n")
        file.write(f"NutzerBeziehungen,13,17,Partner\n")
        file.write(f"NutzerBeziehungen,13,18,Partner\n")
        file.write(f"NutzerBeziehungen,14,19,Partner\n")
        file.write(f"NutzerBeziehungen,14,20,Partner\n")

        # Stellenangebote für Nutzer-ID 11 bis 20
        file.write(f"Stellenangebot,1,Erfahrung im Software-Engineering erforderlich,Software Engineer,11\n")
        file.write(f"Stellenangebot,2,Erfahrung im Projektmanagement erforderlich,Project Manager,11\n")
        file.write(f"Stellenangebot,3,Erfahrung im Marketing erforderlich,Marketing Specialist,12\n")
        file.write(f"Stellenangebot,4,Erfahrung in der Datenanalyse erforderlich,Data Analyst,12\n")
        file.write(f"Stellenangebot,5,Erfahrung im Bauwesen erforderlich,Bauingenieur,13\n")
        file.write(f"Stellenangebot,6,Erfahrung im Architekturdesign erforderlich,Architekt,13\n")
        file.write(f"Stellenangebot,7,Erfahrung im Vertrieb erforderlich,Sales Manager,14\n")
        file.write(f"Stellenangebot,8,Erfahrung in der Lebensmittelproduktion erforderlich,Lebensmitteltechnologe,14\n")
        file.write(f"Stellenangebot,9,Erfahrung im Gesundheitswesen erforderlich,Krankenpfleger,15\n")
        file.write(f"Stellenangebot,10,Erfahrung in der medizinischen Forschung erforderlich,Forscher,15\n")
        file.write(f"Stellenangebot,11,Erfahrung in der Finanzanalyse erforderlich,Finanzanalyst,16\n")
        file.write(f"Stellenangebot,12,Erfahrung in der Buchhaltung erforderlich,Buchhalter,16\n")
        file.write(f"Stellenangebot,13,Erfahrung im Automobilverkauf erforderlich,Verkaufsberater,17\n")
        file.write(f"Stellenangebot,14,Erfahrung in der Fahrzeugwartung erforderlich,Mechaniker,17\n")
        file.write(f"Stellenangebot,15,Erfahrung in der Reiseplanung erforderlich,Reiseberater,18\n")
        file.write(f"Stellenangebot,16,Erfahrung im Kundendienst erforderlich,Kundendienstmitarbeiter,18\n")
        file.write(f"Stellenangebot,17,Erfahrung in der Medienproduktion erforderlich,Medienproduzent,19\n")
        file.write(f"Stellenangebot,18,Erfahrung in der Redaktion erforderlich,Redakteur,19\n")
        file.write(f"Stellenangebot,19,Erfahrung im Marketing erforderlich,Marketing Manager,20\n")
        file.write(f"Stellenangebot,20,Erfahrung in der Werbegestaltung erforderlich,Werbedesigner,20\n")




        # Adressen
        for _ in range(800 * block_num + static_users):
            street = fake.street_address().replace(',', ' ')
            file.write(f"Adresse,{street},{fake.building_number()},{fake.postcode()},{fake.city()},{fake.country()}\n")

        # Nutzer
        for user_id in range(1 + static_users, num_records + 1 + static_users):
            email = fake.unique.email()
            typ = 'Unternehmen' if user_id in company_ids else 'Person'
            file.write(f"Nutzer,{fake.sentence()},{fake.domain_name()}/profile.jpg,{email},{typ},{fake.domain_name()}/banner.jpg\n")
            user_id += 1

        # Personen und Unternehmen
        for user_id in range(1 + static_users, num_records + 1 + static_users):
            if user_id in company_ids:
                company = fake.company().replace(',', '')
                bs = fake.bs().replace(',', '')
                file.write(f"Unternehmen,{user_id},{company},{bs},{random.choice(['klein', 'mittel', 'groß'])},{random.randint(1900, 2021)}\n")
            else:
                first_name = fake.first_name().replace(',', '')
                last_name = fake.last_name().replace(',', '')
                job = fake.job().replace(',', '')
                bio = fake.text(max_nb_chars=50).replace(',', '')
                file.write(f"Person,{user_id},{first_name},{last_name},{fake.date_of_birth()},{job},{bio},{random.randint(1 + static_users, 800 * block_num + static_users)}\n")
                # Kenntnisse
                person_skills = set()
                num_skills = random.randint(3, 7)
                while len(person_skills) < num_skills:
                    skill = random.choice(skills_list)
                    if skill not in person_skills:
                        person_skills.add(skill)
                        file.write(f"Kenntnisse,{user_id},{skill}\n")

        # Standorte
        for _ in range(400 * block_num + static_users):
            file.write(f"Standort,{fake.city()} {fake.street_suffix()},{random.randint(1 + static_users, 800 * block_num + static_users)},{random.randint(1 + static_users, num_records + static_users)}\n")

        # Stellenangebote
        for _ in range(200 * block_num + static_users):
            title = fake.job().replace(',', '')
            desc = fake.sentence().replace(',', '')
            company_id = random.choice(list(company_ids))
            file.write(f"Stellenangebot,{random.randint(1 + static_users, 400 * block_num + static_users)},{desc},{title},{company_id}\n")

        # NutzerBeziehungen
        user_relationships = set()
        while len(user_relationships) < 2000 * block_num:
            id1, id2 = random.randint(1 + static_users, user_id), random.randint(1 + static_users, user_id)
            if id1 != id2:
                relationship = (id1, id2)
                if relationship not in user_relationships and (id2, id1) not in user_relationships:
                    user_relationships.add(relationship)
                    file.write(f"NutzerBeziehungen,{id1},{id2},{fake.word().replace(',', '')}\n")

    print(f"Anzahl Users: {user_id}")

# Beispiel: Erzeuge Blöcke mit zunehmender Anzahl von Datensätzen
base_num_records = 6732 // 6  # Anzahl der Datensätze in einem Block
for block_num in range(1, 6):  # Erzeuge 5 Blöcke
    generate_data_block(block_num, base_num_records)
