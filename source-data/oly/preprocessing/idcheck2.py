import csv

tokyostuff = set()
with open("2020_Olympics_Dataset.csv", newline="", encoding = 'latin') as tokyocsv:
    # ['', 'Code', 'Name', 'Gender', 'Age', 'NOC', 'Country', 'Discipline', 'Sport', 'Event', 'Rank', 'Medal']
    tokyoreader = csv.reader(tokyocsv, delimiter=",", quotechar='"')
    for row in tokyoreader:
        name = frozenset(row[2].lower().split())
        gender = row[3][0]
        age = row[4]
        noc = row[5]
        tokyostuff.add((name, gender, age, noc))

reststuff = set()
with open("athlete_events-upto2016.csv", newline="", encoding="latin") as restcsv:
    # ['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
    restreader = csv.reader(restcsv, delimiter=",", quotechar='"')
    for row in restreader:
        name = frozenset(row[1].lower().split())
        sex = row[2][0]
        age = row[3]
        try:
            age = str(int(row[3])+5)
        except ValueError:
            pass
        noc = row[7]
        reststuff.add((name, sex, age, noc))

commonstuff = tokyostuff.intersection(reststuff)

print(commonstuff)
print(len(commonstuff))

# MORALE: con la giusta condizione (implementabile in JS)
# posso identificare un buon numero di atleti.
# (ma devo limitarmi a quelli di Rio prima di aggiungere +5)
# (e magari prendo anche quelli dei giochi 2012 aggiungendo +9)
