import csv

tokyonames = set()
tokyocodes = dict()
with open("2020_Olympics_Dataset.csv", newline="", encoding = 'latin') as tokyocsv:
    # ['', 'Code', 'Name', 'Gender', 'Age', 'NOC', 'Country', 'Discipline', 'Sport', 'Event', 'Rank', 'Medal']
    tokyoreader = csv.reader(tokyocsv, delimiter=",", quotechar='"')
    for row in tokyoreader:
        name = row[2].lower()
        tokyonames.add(name)
        tokyocodes[name] = row[1]

restnames = set()
restids = dict()
with open("athlete_events-upto2016.csv", newline="", encoding="latin") as restcsv:
    # ['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
    restreader = csv.reader(restcsv, delimiter=",", quotechar='"')
    for row in restreader:
        name = row[1].lower()
        restnames.add(name)
        restids[name] = row[0]

commonnames = tokyonames.intersection(restnames)

eqcount = 0
diffcount = 0
for name in commonnames:
    if tokyocodes[name] != restids[name]:
        diffcount += 1
        print(f"ZAN ZAN ZAN {tokyocodes[name]} != {restids[name]}")
    else:
        eqcount+=1
print(f"{diffcount} - {eqcount}")  # 180 - 0

# Morale: codici INCOMPATIBILI
