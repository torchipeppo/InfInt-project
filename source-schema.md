# athlete_events-upto2016.csv

### athlete_event(id, name, sex, age, ~~weight, height, team,~~ noc, ~~games,~~ year, season, city, sport, event, medal)

*Null is "NA"*

*Drop team and others b/c it's not in 2020. Team detecting strat: same country, same games, same sport/event, same medal.*

*TODO Preprocess to eliminate all winter games*


# noc_regions.csv

*TODO marked for deletion, the Wikipedia table should be better*


# 2020_Olympics_Dataset.csv

### athlete_event_tokyo(~~rownum,~~ code, name, gender, age, noc, country, ~~discipline,~~ sport, event, ~~rank,~~ medal)

*Null is "NA"*

*In theory country is semi-irrelevant too, there's the Wikipedia table*


# Tokyo-Olympic-Medals...

*TODO semi-useless, can/should recompute it from the detailed data, and also include previous games in the count*


# world-banks-income-groups.csv

### income_group(entity, code, year, class)

*Null is "Not categorized"*

*based on GNI*

*entity is country name, semi-irrelevant since we have Wiki table*

*TODO preprocess so that no special characters in column names*


# population.csv

### population(seriesname, seriescode, countryname, countrycode, YR1960, YR1961, ..., YR2021)

*Null is ".."*

*TODO preprocess so that no special characters in column names*


# country-capitals.csv

### countryinfo(countryname, ~~capitalname,~~ caplat, caplon, countrycode, continentname)

*Null is "NULL"*

*TODO there's a couple broken lines b/c "D.C.", and change file name.*

*countryname may be semi-useless w/ wikitable*


# Summer_olympic_Medals.csv

### hosted(year, hostcountry, hostcity, ~~...~~)

*TODO GIGA PREPROCESSING to only leave hosting country. No 2020, but we can hardcode Japan. And change filename.*
