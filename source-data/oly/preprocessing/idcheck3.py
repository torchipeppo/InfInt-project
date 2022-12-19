import csv

tokyocodes = set()
with open("2020_Olympics_Dataset.csv", newline="", encoding = 'latin') as tokyocsv:
    # ['', 'Code', 'Name', 'Gender', 'Age', 'NOC', 'Country', 'Discipline', 'Sport', 'Event', 'Rank', 'Medal']
    tokyoreader = csv.reader(tokyocsv, delimiter=",", quotechar='"')
    for row in tokyoreader:
        tokyocodes.add(row[1])

restids = set()
with open("athlete_events-upto2016.csv", newline="", encoding="latin") as restcsv:
    # ['ID', 'Name', 'Sex', 'Age', 'Height', 'Weight', 'Team', 'NOC', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal']
    restreader = csv.reader(restcsv, delimiter=",", quotechar='"')
    for row in restreader:
        restids.add(row[0])

commons = tokyocodes.intersection(restids)

print(len(commons))  # 0

# Morale: In questi dataset, gli ID sono distinti,
# quindi non devo preoccuparmi di unicizzare gli id degli atleti di Tokyo
# che non hanno corispondenza nell'altro dataset.
