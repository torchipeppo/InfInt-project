### Atleti che hanno giocato per almeno tre nazioni, mostrando anche tre di quelle nazioni

&exist; year1, year2, year3 . AthleteWasInCountry(id, year1, cc1) &and; AthleteWasInCountry(id, year2, cc2) &and; AthleteWasInCountry(id, year3, cc3) &and; cc1 &ne; cc2 &and; cc1 &ne; cc3 &and; cc2 &ne; cc3

``` SQL
SELECT DISTINCT aic1.id, aic1.cc AS cc1, aic2.cc AS cc2, aic3.cc AS cc3, hn.name
FROM
    AthleteWasInCountry AS aic1
        JOIN AthleteWasInCountry AS aic2 ON aic1.id = aic2.id
        JOIN AthleteWasInCountry AS aic3 ON aic1.id = aic3.id
        JOIN HasName AS hn               ON aic1.id = hn.what
WHERE
    aic1.cc != aic2.cc AND aic1.cc != aic3.cc AND aic2.cc != aic3.cc
    -- Aggiungo queste condizioni solo per standardizzare l'ordine
    -- e quindi far uscire ogni atleta solo una volta
    AND aic1.year < aic2.year AND aic2.year < aic3.year;
```

### Atleti tali che, giocando al di fuori della propria nazione, si sono piazzati sul podio meglio di un atleta che giocava in casa, anch'esso sul podio nello stesso evento.

(&exist; id_home_guy, year, sport, event, medal_p, medal_h, other_cc, home_cc . ParticipatedWithResults(id_protagonist_guy, year, sport, event, medal_p) &and; ParticipatedWithResults(id_home_guy, year, sport, event, medal_h) &and; EditionIsInCountry(year, home_cc) &and; AthleteWasInCountry(id_home_guy, year, home_cc) &and; AthleteWasInCountry(id_protagonist_guy, year, other_cc) &and; other_cc &ne; home_cc &and; medal_p = "Gold" &and; medal_h = "Silver") &or; (&exist; ... &and; medal_p = "Gold" &and; medal_h = "Bronze") &or; (&exist; ... &and; medal_p = "Silver" &and; medal_h = "Bronze") *(Unione di query congiuntive)* *(N.B.: Richiediamo anche al padrone di casa di aver vinto una medaglia per limitarci a rivali comunque "competenti", credo che avere un atleta in casa fuori dal podio sia praticamente scontato per tutto. Quindi, evitiamo un numero eccessivo di risultati.)*

``` SQL
SELECT DISTINCT protag.id, hn.name
FROM
    ParticipatedWithResults AS protag
        JOIN ParticipatedWithResults AS home  ON protag.year = home.year AND protag.sport = home.sport AND protag.event = home.event
        JOIN HasName AS hn                    ON protag.id = hn.what
        JOIN EditionIsInCountry AS eic        ON home.year = eic.year
        JOIN AthleteWasInCountry AS aic_p     ON protag.id = aic_p.id AND protag.year = aic_p.year
        JOIN AthleteWasInCountry AS aic_h     ON home.id = aic_h.id AND home.year = aic_h.year
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

FOL: &exist; year1, year2, sport, e1, e2, medal1, medal2, cc1, cc2, cont1, cont2, home_cont, home_cc . ParticipatedWithResults(id, year1, sport, e1, medal1) &and; ParticipatedWithResults(id, year2, sport, e2, medal2) &and; medal1 &ne; "None" &and; medal2 &ne; "None" &and; EditionIsInCountry(year1, cc1) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc1, cont1) &and; IsInContinent(cc2, cont2) &and; cont1 &ne; cont2 &and; AthleteWasInCountry(id, year1, home_cc) &and; AthleteWasInCountry(id, year2, home_cc) &and; IsInContinent(home_cc, home_cont) &and; cont1 &ne; home_cont &and; cont2 &ne; home_cont

``` SQL
DROP VIEW IF EXISTS QueryResult1;

CREATE TEMP VIEW QueryResult1 AS
SELECT DISTINCT p1.id, aic1.cc, hn.name, p1.year as anyyear
FROM
    ParticipatedWithResults AS p1
        JOIN ParticipatedWithResults AS p2  ON p1.id = p2.id AND p1.sport = p2.sport
        JOIN HasName AS hn                  ON p1.id = hn.what
        JOIN EditionIsInCountry AS eic1     ON p1.year = eic1.year
        JOIN IsInContinent AS cic1          ON eic1.cc = cic1.what
        JOIN EditionIsInCountry AS eic2     ON p2.year = eic2.year
        JOIN IsInContinent AS cic2          ON eic2.cc = cic2.what
        JOIN AthleteWasInCountry AS aic1    ON p1.id = aic1.id AND p1.year = aic1.year
        JOIN AthleteWasInCountry AS aic2    ON p2.id = aic2.id AND p2.year = aic2.year
        JOIN IsInContinent as home_ic       ON aic1.cc = home_ic.what
WHERE
    aic1.cc = aic2.cc AND
    p1.medal != 'None' AND
    p2.medal != 'None' AND
    cic1.continent != cic2.continent AND
    cic1.continent != home_ic.continent AND
    cic2.continent != home_ic.continent;

SELECT DISTINCT qr.id, qr.name
FROM QueryResult1 AS qr;
```

### FOLLOW-UP!! Get ogni nazione che ha un atleta come risultato della query precedente, insieme alla sua fascia di GNI

FOL: &exist; ... &and; HadIncomeClass(home_cc, year1, class)

``` SQL
-- Eseguire prima la query precedente per definire la view!

SELECT DISTINCT qr.cc, hicl.class
FROM QueryResult1 AS qr JOIN HadIncomeClass as hicl ON qr.cc = hicl.cc AND qr.anyyear = hicl.year
ORDER BY hicl.class;
```

### data un'edizione, esaminare la distribuzione delle (fasce di) PIL presenti nelle nazioni con più di X medaglie vinte in quell'edizione (forse affiancarla con tale distrubizione senza il vincolo in classifica)

&exist; gold, silver, bronze . GotTotalMedals(cc, year, gold, silver, bronze) &and; gold &ne; 0 &and; gold &ne; 1 &and; ... &and; gold &ne; X &and; HadIncomeClass(cc, year, class)

*(Ta-daa! Non c'è bisogno della tabella gt! Ciò non toglie che magari in fase di implementazione usi l'operatore di confronto di SQL.)*

``` SQL
SELECT DISTINCT ic.cc, ic.class
FROM GotTotalMedals AS tm
    JOIN HadIncomeClass AS ic ON tm.cc = ic.cc AND tm.year = ic.year
WHERE
    -- Rappresento la serie di disuguaglianze FOL in maniera più concisa,
    -- tanto le medaglie sono nel dominio degli interi positivi
    tm.gold > 2
    AND tm.year = 2012
ORDER BY ic.class;
```
*Parametri: tipo 2 o 3 come soglia medaglie (possiamo anche mettere le disuguaglianze esplicitamente se è così bassa), anno accaso*

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
