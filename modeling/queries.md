### Atleti che hanno giocato per almeno tre nazioni, mostrando anche tre di quelle nazioni

&exist; year1, year2, year3 . AthleteWasFromCountry(id, year1, cc1) &and; AthleteWasFromCountry(id, year2, cc2) &and; AthleteWasFromCountry(id, year3, cc3) &and; &not; (cc1 = cc2) &and; &not; (cc1 = cc3) &and; &not; (cc2 = cc3)

``` SQL
SELECT DISTINCT aic1.id, aic1.cc AS cc1, aic2.cc AS cc2, aic3.cc AS cc3, hn.name
FROM
    AthleteWasFromCountry AS aic1
        JOIN AthleteWasFromCountry AS aic2 ON aic1.id = aic2.id
        JOIN AthleteWasFromCountry AS aic3 ON aic1.id = aic3.id
        JOIN HasName AS hn                 ON aic1.id = hn.what
WHERE
    aic1.cc != aic2.cc AND aic1.cc != aic3.cc AND aic2.cc != aic3.cc
    -- Aggiungo queste condizioni solo per standardizzare l'ordine
    -- e quindi far uscire ogni atleta solo una volta
    AND aic1.year < aic2.year AND aic2.year < aic3.year;
```

### Atleti tali che, giocando al di fuori della propria nazione, si sono piazzati sul podio meglio di un atleta che giocava in casa, anch'esso sul podio nello stesso evento.

(&exist; id_home_guy, year, sport, event, medal_p, medal_h, other_cc, home_cc . ParticipatedWithResults(id_protagonist_guy, year, sport, event, medal_p) &and; ParticipatedWithResults(id_home_guy, year, sport, event, medal_h) &and; EditionIsInCountry(year, home_cc) &and; AthleteWasFromCountry(id_home_guy, year, home_cc) &and; AthleteWasFromCountry(id_protagonist_guy, year, other_cc) &and; &not; (other_cc = home_cc) &and; medal_p = "Gold" &and; medal_h = "Silver") &or; (&exist; ... &and; medal_p = "Gold" &and; medal_h = "Bronze") &or; (&exist; ... &and; medal_p = "Silver" &and; medal_h = "Bronze") *(Unione di query congiuntive)* *(N.B.: Richiediamo anche al padrone di casa di aver vinto una medaglia per limitarci a rivali comunque "competenti", credo che avere un atleta in casa fuori dal podio sia praticamente scontato per tutto. Quindi, evitiamo un numero eccessivo di risultati.)*

``` SQL
SELECT DISTINCT protag.id, hn.name
FROM
    ParticipatedWithResults AS protag
        JOIN ParticipatedWithResults AS home    ON protag.year = home.year AND protag.sport = home.sport AND protag.event = home.event
        JOIN HasName AS hn                      ON protag.id = hn.what
        JOIN EditionIsInCountry AS eic          ON home.year = eic.year
        JOIN AthleteWasFromCountry AS aic_p     ON protag.id = aic_p.id AND protag.year = aic_p.year
        JOIN AthleteWasFromCountry AS aic_h     ON home.id = aic_h.id AND home.year = aic_h.year
WHERE
    aic_h.cc = eic.cc AND
    aic_p.cc != eic.cc AND
    (
        (protag.medal = 'Gold' AND home.medal = 'Silver') OR
        (protag.medal = 'Gold' AND home.medal = 'Bronze') OR
        (protag.medal = 'Silver' AND home.medal = 'Bronze')
    );
```

*(N.B.: l'implementazione SQL raggruppa la disgiunzione in maniera più concisa, ma la query è comunque equivalente.)*

### Atleti che vincono una medaglia nello stesso sport in due continenti diversi. I due continenti devono essere diversi dal proprio, e l'atleta deve aver giocato per la stessa nazione entrambe le volte.

FOL: &exist; year1, year2, sport, e1, e2, medal1, medal2, cc1, cc2, cont1, cont2, home_cont, home_cc . ParticipatedWithResults(id, year1, sport, e1, medal1) &and; ParticipatedWithResults(id, year2, sport, e2, medal2) &and; &not; (medal1 = "None") &and; &not; (medal2 = "None") &and; EditionIsInCountry(year1, cc1) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc1, cont1) &and; IsInContinent(cc2, cont2) &and; &not; (cont1 = cont2) &and; AthleteWasFromCountry(id, year1, home_cc) &and; AthleteWasFromCountry(id, year2, home_cc) &and; IsInContinent(home_cc, home_cont) &and; &not; (cont1 = home_cont) &and; &not; (cont2 = home_cont)

``` SQL
SELECT DISTINCT hn.name, aic1.cc, cic1.continent AS continent1, cic2.continent AS continent2
FROM
    ParticipatedWithResults AS p1
        JOIN ParticipatedWithResults AS p2    ON p1.id = p2.id AND p1.sport = p2.sport
        JOIN HasName AS hn                    ON p1.id = hn.what
        JOIN EditionIsInCountry AS eic1       ON p1.year = eic1.year
        JOIN IsInContinent AS cic1            ON eic1.cc = cic1.cc
        JOIN EditionIsInCountry AS eic2       ON p2.year = eic2.year
        JOIN IsInContinent AS cic2            ON eic2.cc = cic2.cc
        JOIN AthleteWasFromCountry AS aic1    ON p1.id = aic1.id AND p1.year = aic1.year
        JOIN AthleteWasFromCountry AS aic2    ON p2.id = aic2.id AND p2.year = aic2.year
        JOIN IsInContinent as home_ic         ON aic1.cc = home_ic.cc
WHERE
    aic1.cc = aic2.cc AND
    p1.medal != 'None' AND
    p2.medal != 'None' AND
    cic1.continent != cic2.continent AND
    cic1.continent != home_ic.continent AND
    cic2.continent != home_ic.continent AND
    -- the following condition is just to standardize the order of the continents
    cic1.continent < cic2.continent;
```

### data un'edizione, esaminare la distribuzione delle (fasce di) PIL presenti nelle nazioni con più di X medaglie vinte in quell'edizione (forse affiancarla con tale distrubizione senza il vincolo in classifica)

&exist; gold, silver, bronze . GotTotalMedals(cc, year, gold, silver, bronze) &and; &not; (gold = 0) &and; &not; (gold = 1) &and; ... &and; &not; (gold = X) &and; HadIncomeClass(cc, year, class) &and; HadPopulation(cc, year, population)

*(Ta-daa! Non c'è bisogno della tabella gt! Ciò non toglie che magari in fase di implementazione usi l'operatore di confronto di SQL.)*

``` SQL
SELECT DISTINCT ic.cc, ic.class, hp.population
FROM GotTotalMedals AS tm
    JOIN HadIncomeClass AS ic ON tm.cc = ic.cc AND tm.year = ic.year
    JOIN HadPopulation AS hp ON tm.cc = hp.cc AND tm.year = hp.year
WHERE
    tm.gold != 0 AND tm.gold != 1
    AND tm.year = 2012
ORDER BY ic.class;
```
*Parametri: tipo 2 o 3 come soglia medaglie (possiamo anche mettere le disuguaglianze esplicitamente se è così bassa), anno accaso*

E l'altra faccia della medaglia:

(&exist; gold, silver, bronze . GotTotalMedals(cc, year, gold, silver, bronze) &and; HadIncomeClass(cc, year, class) &and; HadPopulation(cc, year, population) &and; gold = 0) &or; (&exist; ... &and; gold = 1) &or; (&exist; ... &and; gold = X)

``` SQL
SELECT DISTINCT ic.cc, ic.class, hp.population
FROM GotTotalMedals AS tm
    JOIN HadIncomeClass AS ic ON tm.cc = ic.cc AND tm.year = ic.year
    JOIN HadPopulation AS hp ON tm.cc = hp.cc AND tm.year = hp.year
WHERE
    (tm.gold = 0 OR tm.gold = 1)
    AND tm.year = 2012
ORDER BY ic.class;
```

Al solo scopo di contare meglio, si può fare un'altra query SQL espansa con COUNT e GROUP BY.

``` SQL
SELECT ic.class, COUNT(DISTINCT ic.cc)
FROM GotTotalMedals AS tm
    JOIN HadIncomeClass AS ic ON tm.cc = ic.cc AND tm.year = ic.year
WHERE
    tm.gold > 2
    AND tm.year = 2012
GROUP BY ic.class
ORDER BY ic.class;
```

### Trovare le coppie di edizioni consecutive che si sono svolte nello stesso continente

*(Non è una query sugli atleti, stavolta è più sulle edizioni e sulla geografia. La vorrei perché sugli atleti ne ho già parecchie. Può fare da quinta query, oppure sostituirsi a una sugli atleti.)*

&exist; continent . FollowedBy(year1, year2) &and; EditionIsInCountry(year1, cc1) &and; IsInContinent(cc1, continent) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc2, continent)

``` SQL
SELECT eic1.year AS year1, eic1.cc AS cc1, eic2.year AS year2, eic2.cc AS cc2
FROM FollowedBy AS fb
    JOIN EditionIsInCountry AS eic1   ON fb.prev=eic1.year
    JOIN IsInContinent AS cic1        ON eic1.cc=cic1.cc
    JOIN EditionIsInCountry AS eic2   ON fb.next=eic2.year
    JOIN IsInContinent AS cic2        ON eic2.cc=cic2.cc
WHERE cic1.continent=cic2.continent;
```
