# TODO
mettere predicati /1 nelle query. *(oppure toglierli dallo schema globale, se ci fanno schifo)*

### atleti con carriera interessante (tipo, vince per la prima volta dopo N tentativi di fila, oppure vince bronzo->argento->oro in tre edizioni consecutive, ...)

*   &exist; year1, year2, year3, sport, event, finalmedal . ParticipatedWithResults(id, year1, sport, event, "None") &and; ParticipatedWithResults(id, year2, sport, event, "None") ParticipatedWithResults(id, year3, sport, event, finalmedal) &and; FollowedBy(year1, year2) &and; FollowedBy(year2, year3) &and; finalmedal &ne; "None" *(N=3, estendibile ad altri N)*

    ``` SQL
    SELECT DISTINCT p12.id, hn.name
    FROM
        (
            SELECT p1.id, p1.year AS year1, p2.year AS year2, p1.sport, p1.event
            FROM
                ParticipatedWithResults AS p1
                    JOIN ParticipatedWithResults AS p2
                    ON p1.id = p2.id AND p1.sport = p2.sport AND p1.event = p2.event,
                FollowedBy as f12
            WHERE
                p1.medal = 'None' AND
                p2.medal = 'None' AND
                f12.prev = p1.year AND
                f12.next = p2.year
        ) AS p12
            JOIN ParticipatedWithResults AS p3
            ON p12.id = p3.id AND p12.sport = p3.sport AND p12.event = p3.event
            JOIN HasName AS hn ON p12.id = hn.what,
        FollowedBy AS f23
    WHERE
        f23.prev = p12.year2 AND
        f23.next = p3.year AND
        p3.medal != 'None';
    ```

*   &exist; year1, year2, year3, sport, event . ParticipatedWithResults(id, year1, sport, event, Bronze) &and; ParticipatedWithResults(id, year2, sport, event, Silver) ParticipatedWithResults(id, year3, sport, event, Gold) &and; FollowedBy(year1, year2) &and; FollowedBy(year2, year3)

    ``` SQL
    SELECT DISTINCT p12.id, hn.name
    FROM
        (
            SELECT p1.id, p1.year AS year1, p2.year AS year2, p1.sport, p1.event
            FROM
                ParticipatedWithResults AS p1
                    JOIN ParticipatedWithResults AS p2
                    ON p1.id = p2.id AND p1.sport = p2.sport AND p1.event = p2.event,
                FollowedBy as f12
            WHERE
                p1.medal = 'Bronze' AND
                p2.medal = 'Silver' AND
                f12.prev = p1.year AND
                f12.next = p2.year
        ) AS p12
            JOIN ParticipatedWithResults AS p3
            ON p12.id = p3.id AND p12.sport = p3.sport AND p12.event = p3.event
            JOIN HasName AS hn ON p12.id = hn.what,
        FollowedBy AS f23
    WHERE
        f23.prev = p12.year2 AND
        f23.next = p3.year AND
        p3.medal = 'Gold';
    ```

### atleti con carriera interessante X geografia (tipo, vince una medaglia nello stesso sport in due continenti diversi, o batte il padrone di casa, o vince a una latitudine molto diversa dalla propria, ...)

*   &exist; year1, year2, sport, e1, e2, medal1, medal2, cc1, cc2, cont1, cont2 . ParticipatedWithResults(id, year1, sport, e1, medal1) &and; ParticipatedWithResults(id, year2, sport, e2, medal2) &and; medal1 &ne; "None" &and; medal2 &ne; "None" &and; EditionIsInCountry(year1, cc1) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc1, cont1) &and; IsInContinent(cc2, cont2) &and; cont1 &ne; cont2 *(Potremmo pensare di farci dare pure i continenti...?)*

    ``` SQL
    SELECT DISTINCT p1.id, hn.name
    FROM
        ParticipatedWithResults AS p1
            JOIN ParticipatedWithResults AS p2  ON p1.id = p2.id AND p1.sport = p2.sport
            JOIN HasName AS hn                  ON p1.id = hn.what
            JOIN EditionIsInCountry AS eic1     ON p1.year = eic1.year
            JOIN IsInContinent AS cic1          ON eic1.cc = cic1.what
            JOIN EditionIsInCountry AS eic2     ON p2.year = eic2.year
            JOIN IsInContinent AS cic2          ON eic2.cc = cic2.what
    WHERE
        p1.medal != 'None' AND p2.medal != 'None' AND cic1.continent != cic2.continent;
    ```

*   (&exist; id_home_guy, year, sport, event, medal_p, medal_h, other_cc, home_cc . ParticipatedWithResults(id_protagonist_guy, year, sport, event, medal_p) &and; ParticipatedWithResults(id_home_guy, year, sport, event, medal_h) &and; EditionIsInCountry(year, home_cc) &and; AthleteIsInCountry(id_home_guy, home_cc) &and; AthleteIsInCountry(id_protagonist_guy, other_cc) &and; other_cc &ne; home_cc &and; ~~medal_p &ne; "None" &and; medal_h &ne; "None"~~ &and; medal_p = "Gold" &and; medal_h = "Silver") &or; (&exist; ... &and; medal_p = "Gold" &and; medal_h = "Bronze") &or; (&exist; ... &and; medal_p = "Silver" &and; medal_h = "Bronze") *(Unione di query congiuntive)* *(N.B.: Richiediamo anche al padrone di casa di aver vinto una medaglia per evitare un numero eccessivo di risultati, la descrizione della query andrà sistemata di conseguenza se scegliamo questa)*

    ``` SQL
    SELECT DISTINCT protag.id, hn.name
    FROM
        ParticipatedWithResults AS protag
            JOIN ParticipatedWithResults AS home  ON protag.year = home.year AND protag.sport = home.sport AND protag.event = home.event
            JOIN HasName AS hn                  ON protag.id = hn.what
            JOIN EditionIsInCountry AS eic      ON home.year = eic.year
            JOIN AthleteIsInCountry AS aic_p    ON protag.id = aic_p.id
            JOIN AthleteIsInCountry AS aic_h    ON home.id = aic_h.id
    WHERE
        aic_h.cc = eic.cc AND
        aic_p.cc != eic.cc AND
        (
            (protag.medal = 'Gold' AND home.medal = 'Silver') OR
            (protag.medal = 'Gold' AND home.medal = 'Bronze') OR
            (protag.medal = 'Silver' AND home.medal = 'Bronze')
        );
    ```

&exist; ??? . ParticipatedWithResults(id, year, s, e, medal) &and; medal &ne; "None" &and; HasCapitalLatitude(id, caplat_a) &and; EditionIsInCountry(year, cc) &and; HasCapitalLatitude(cc, caplat_c) &and; MoltoDiverse??(caplat_a, caplat_c)

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

### Le nazioni con almeno N atleti che hanno partecipato a giochi fuori dal proprio continente ~~(lo stesso atleta conta più volte se ha partecipato ad altrettante edizioni extracontinentali)~~. Affiancare alla fascia di GNI che la nazione aveva in uno qualunque degli anni considerati (la stessa nazione potrebbe comparire più volte se più fasce sono applicabili, ma tanto le fasce sono solo quattro, quindi mi preoccupo poco).

&exist; home_cont, id1, id2, id3, year1, year2, year3, s1, s2, s3, e1, e2, e3, m1, m2, m3, cc1, cc2, cc3, cont1, cont2, cont3 . IsInContinent(home_cc, home_cont) &and; AthleteIsInCountry(id1, home_cc) &and; ParticipatedWithResults(id1, year1, s1, e1, m1) &and; EditionIsInCountry(year1, cc1) &and; IsInContinent(cc1, cont1) &and; cont1 &ne; home_cont &and; AthleteIsInCountry(id2, home_cc) &and; ParticipatedWithResults(id2, year2, s2, e2, m2) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc2, cont2) &and; cont2 &ne; home_cont &and; AthleteIsInCountry(id3, home_cc) &and; ParticipatedWithResults(id3, year3, s3, e3, m3) &and; EditionIsInCountry(year3, cc3) &and; IsInContinent(cc3, cont3) &and; cont3 &ne; home_cont &and; id1 &ne; id2 &and; id1 &ne; id3 &and; id2 &ne; id3 &and; HadIncomeClass(home_cc, year1, class) *(N=3, estendibile ad altri N)*

``` SQL
DROP VIEW IF EXISTS Temp;

CREATE TEMP VIEW Temp AS
SELECT *
FROM PlayedInContinent
WHERE year=2012;

SELECT DISTINCT hicl.cc, hicl.class
FROM
    IsInContinent as home_iic
        -- first
        JOIN Temp AS pic1 ON pic1.home_cc = home_iic.what
        -- second
        JOIN Temp AS pic2 ON pic2.home_cc = home_iic.what
        -- third
        JOIN Temp AS pic3 ON pic3.home_cc = home_iic.what
        -- class
        JOIN HadIncomeClass AS hicl ON hicl.cc = home_iic.what AND hicl.year = pic1.year
WHERE
    pic1.continent != home_iic.continent AND
    pic2.continent != home_iic.continent AND
    pic3.continent != home_iic.continent AND
    pic2.id != pic3.id AND
    pic1.id != pic3.id AND
    pic1.id != pic2.id;
```

Sta query non s'ha da fare. Anche limitandoci a un singolo anno, impiega comunque circa un minuto. Senza la limitazione, impiega un tempo non determinato E si pappa tutto lo spazio su disco come cache. Nessuno dei due casi è adatto all'esecuzione rapida in fase di presentazione/demo. E limitare a un anno snatura un po' la query.

### Atleti che hanno giocato per almeno tre nazioni, mostrando anche tre di quelle nazioni

&exist; &empty; . AthleteIsInCountry(id, cc1) &and; AthleteIsInCountry(id, cc2) &and; AthleteIsInCountry(id, cc3) &and; cc1 &ne; cc2 &and; cc1 &ne; cc3 &and; cc2 &ne; cc3

``` SQL
SELECT DISTINCT aic1.id, aic1.cc, aic2.cc, aic3.cc, hn.name
FROM
    AthleteIsInCountry AS aic1
        JOIN AthleteIsInCountry AS aic2 ON aic1.id = aic2.id
        JOIN AthleteIsInCountry AS aic3 ON aic1.id = aic3.id
        JOIN HasName AS hn              ON aic1.id = hn.what
WHERE
    aic1.cc != aic2.cc AND aic1.cc != aic3.cc AND aic2.cc != aic3.cc
    -- Aggiungo queste condizioni solo per standardizzare l'ordine
    -- e quindi far uscire ogni atleta solo una volta
    AND aic1.cc < aic2.cc AND aic2.cc < aic3.cc;
```

# Sostituzione!

Questa sostituisce UNA delle query sotto "carriera interessante X geografia"

### Atleti che vincono una medaglia nello stesso sport in due continenti diversi. I due continenti devono essere diversi dal proprio, e l'atleta deve aver giocato per la stessa nazione entrambe le volte.

**TODO** Ancora non è possibile sapere se l'atleta ha giocato per la stessa nazione entrambe le volte. Questa però è la seconda volta che vorrei avere quest'informazione (l'altra è per la query dei tre paesi, per ordinarli), quindi magari posso mettere mano allo schema globale...

FOL: &exist; year1, year2, sport, e1, e2, medal1, medal2, cc1, cc2, cont1, cont2, home_cont, home_cc . ParticipatedWithResults(id, year1, sport, e1, medal1) &and; ParticipatedWithResults(id, year2, sport, e2, medal2) &and; medal1 &ne; "None" &and; medal2 &ne; "None" &and; EditionIsInCountry(year1, cc1) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc1, cont1) &and; IsInContinent(cc2, cont2) &and; cont1 &ne; cont2 &and; IsInContinent(id, home_cont) &and; cont1 &ne; home_cont &and; cont2 &ne; home_cont &and; AthleteIsInCountry(id, home_cc) &and; TODO(vedi_sopra)

``` SQL
DROP VIEW IF EXISTS QueryResult1;

CREATE TEMP VIEW QueryResult1 AS
SELECT DISTINCT p1.id, aic.cc, hn.name, p1.year as anyyear
FROM
    ParticipatedWithResults AS p1
        JOIN ParticipatedWithResults AS p2  ON p1.id = p2.id AND p1.sport = p2.sport
        JOIN HasName AS hn                  ON p1.id = hn.what
        JOIN EditionIsInCountry AS eic1     ON p1.year = eic1.year
        JOIN IsInContinent AS cic1          ON eic1.cc = cic1.what
        JOIN EditionIsInCountry AS eic2     ON p2.year = eic2.year
        JOIN IsInContinent AS cic2          ON eic2.cc = cic2.what
        JOIN AthleteIsInCountry AS aic      ON p1.id = aic.id
        JOIN IsInContinent as home_ic       ON p1.id = home_ic.what
WHERE
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
