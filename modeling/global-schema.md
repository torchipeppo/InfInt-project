cc is Country Code. It's always ISO.

*(medals, events and continents are not first-class citizens, so they don't have any /1 predicates)*

## Athlete/1
*(id)*

## Country/1
*(cc)*

## Edition/1
*(year)*

*Editions of the Games are simply identified by their year*

## HasName/2
*(what, name)*

*For athlete IDs and country codes. (Not editions, years are int and not varchar. It's not worth it.)*

## HasSex/2
*(id, sex)*

## HadAge/3
*(id, year, age)*

## ParticipatedWithResults/5
*(id, year, sport, event, medal)*

## AthleteWasFromCountry/3
*(id, year, cc)*

## EditionIsInCountry/2
*(year, cc)*

## GotTotalMedals/5
*(cc, year, gold, silver, bronze)*

*Including a special value for year, "TOTAL" (or NULL), if possible*

*Tabellotto gigante, ma se voglio quest'informazione vorrò sempre tutti i tipi di medaglie, quindi questa è un'ottimizzazione a livello logico*

## HadIncomeClass/3
*(cc, year, class)*

## HadPopulation/3
*(cc, year, population)*

## IsInContinent/2
*(cc, continent)*

## FollowedBy/2
*(prev, next)*

# Soffitta

## PlayedInContinent/3
*(id, year, continent)*

*Added because I want the system to compute the big final query "countries with X athletes that played in a continent other than the country's". This predicate is here solely for the purpose of making that query actually computable without sucking up all my disk space as cache. It should be legit, designing the system based on the task I want it to perform.*

## HasCapitalLatitude/2
*(cc, lat)*

*Never found a good use for this.*
