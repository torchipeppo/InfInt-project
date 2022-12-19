cc is Country Code. It's always ISO (hopefully).

# VERSIONE TABULARE

<!--
## Athlete/9
*(id, name, sex, age, cc, year, sport, event, medal)*
-->

## AthleteInfo/4
*(id, name, sex, cc)*

## AthleteEvent/6
*(id, year, age, sport, event, medal)*

## CountryMedals/5
*(cc, year, gold, silver, bronze)*

*Including a special value for year, "TOTAL" (or NULL)*

## GameHostedIn/2
*(year, cc)*

## CountryIncome/3
*(cc, year, class)*

## CountryPopulation/3
*(cc, year, population)*

## IsAtLatitude/2
*(what, lat)*

*Conceptually, "what" can be an athlete id, a country code or an Olympic Games edition (represented by its year) without need for separate predicates, I think. The implementation might need us to do separate tables (or one for the countries and handle the rest with joins), however.*

## IsInContinent/2
*(what, continent)*

*As above*





# VERSIONE OBJECT-ORIENTED

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

## IsAtLatitude/2
*(what, lat)*

*For countries primarily, and consequently for athletes and editions too*

## IsInContinent/2
*(what, continent)*

*As above*
