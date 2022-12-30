# athlete_events-upto2016.csv

### athlete_event(id, name, sex, age, ~~height, weight, team,~~ noc, year, ~~season,~~ city, sport, event, medal)

*Null is "NA"*

*Dropped team and others b/c it's not in 2020. Team detecting strat: same country, same games, same sport/event, same medal.*

*Preprocessed to eliminate all winter games*

*N.B.: Dataset is bugged!! Non-ascii characters are mysteriously absent from names. For example, see poor no. 108383, whose actual surname is Šekarić. It came like this. Nothing to be done about it.*


# Summer_olympic_Medals.csv

### country_medals(year, countryname, countrycode, gold, silver, bronze)

*Already-counted data since FOL can't count*

*Disclaimer: here appear some teams/regions that don't correspond to countries with ISO codes or former countries. They won't be integrated at all. It would be useless anyway since they don't have socio-economic or geographic data.*


# world-banks-income-groups.csv

### income_group(entity, code, year, class)

*Null is "Not categorized"*

*based on GNI*

*entity is country name, semi-irrelevant since we have Wiki table*

*Fixed Kosovo code: OWID_KOS -> XKX to match the population dataset*


# population.csv

### population(countrycode, YR1960, YR1961, ..., YR2021)

*Null is ".."*

*preprocessed so that no special characters in column names*


# country-data.csv

### countrydata(isocode, caplat, caplon, continent)

*Preprocessing: fixed a couple "Washington, D.C.", removed useless columns, replaced country codes with ISO Alpha-3 (was only occurrence of Alpha-2, decided to simplify). Added Kosovo by hand.*


# hosting-countries.csv

### hosted(year, hostcountry, hostcity)

*done GIGA PREPROCESSING to only leave hosting country. And changed filename. And fixed country names to match Wiki table.*


# country-codes.csv

### countrycodes(Country, IOC, FIFA, ISO)

*Null is "null"*

*Will be main source for country names too*

*Preprocessing: fused two HTML into one CSV (tried fusing into one HTML and read it as XML, but exec time went from ~30 sec to ~5 min, so CSV was chosen for performance reasons). Set Kosovo ISO code to XKX (its temporary code, used in the population dataset)*

*Historical countries may be useless. Economic data is only from 1960 anyway.*
