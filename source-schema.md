# athlete_events-upto2016.csv

### athlete_event(id, name, sex, age, ~~height, weight, team,~~ noc, year, season, city, sport, event, medal)

*Null is "NA"*

*Dropped team and others b/c it's not in 2020. Team detecting strat: same country, same games, same sport/event, same medal.*

*Preprocessed to eliminate all winter games*


# noc_regions.csv

*TODO marked for deletion, the Wikipedia table should be better*

*But check if there are some nations that appear only there first*


# 2020_Olympics_Dataset.csv

### athlete_event_tokyo(~~rownum,~~ code, name, gender, age, noc, country, ~~discipline,~~ sport, event, ~~rank,~~ medal)

*Null is "NA"*

*In theory country is semi-irrelevant too, there's the Wikipedia table*


# Tokyo-Olympic-Medals...

*TODO semi-useless, can/should recompute it from the detailed data, and also include previous games in the count*

*Or maybe we want to take some already-counted data, since FOL can't count?*


# world-banks-income-groups.csv

### income_group(entity, code, year, class)

*Null is "Not categorized"*

*based on GNI*

*entity is country name, semi-irrelevant since we have Wiki table*


# population.csv

### population(countrycode, YR1960, YR1961, ..., YR2021)

*Null is ".."*

*preprocessed so that no special characters in column names*


# country-data.csv

### countrydata(isocode, caplat, caplon, countrycode, continent)

*Preprocessing: fixed a couple "Washington, D.C.", removed useless columns, replaced country codes with ISO Alpha-3 (was only occurrence of Alpha-2, decided to simplify)*


# hosting-countries.csv

### hosted(year, hostcountry, hostcity)

*done GIGA PREPROCESSING to only leave hosting country. And changed filename.*


# country-codes.csv

### countrycodes(Country, IOC, FIFA, ISO)

*Null is "null"*

*Will be main source for country names too*

*Preprocessing: turned into CSV (was HTML)*

*Historical countries may be useless. Economic data is only from 1960 anyway.*
