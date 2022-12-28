cc is Country Code. It's always ISO (hopefully).

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

## AthleteIsInCountry/2
*(id, cc)*

## EditionIsInCountry/2
*(year, cc)*

*(Different data types, not worth it to try and make one table. I prefer having year as int for numerical operations/comparisons.)*

## GotTotalMedals/5
*(cc, year, gold, silver, bronze)*

*Including a special value for year, "TOTAL" (or NULL), if possible*

*Tabellotto gigante, ma se voglio quest'informazione vorrò sempre tutti i tipi di medaglie, quindi questa è un'ottimizzazione a livello logico*

## HadIncomeClass/3
*(cc, year, class)*

## HadPopulation/3
*(cc, year, population)*

## HasCapitalLatitude/2
*(what, lat)*

*For countries primarily, also for athletes*

## IsInContinent/2
*(what, continent)*

*As above*

# TODO

* Add FollowedBy to both schemas if we use it
