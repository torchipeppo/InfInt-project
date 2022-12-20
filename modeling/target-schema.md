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

*For athlete IDs and country codes. And maybe also editions, they may have the name of the city they were in...*

## HasSex/2
*(id, sex)*

## HadAge/3
*(id, year, age)*

## ParticipatedWithResults/5
*(id, year, sport, event, medal)*

## IsInCountry/2
*(what, cc)*

*For athletes and editions*

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

*For countries primarily, and consequently for athletes and editions too*

## IsInContinent/2
*(what, continent)*

*As above*
