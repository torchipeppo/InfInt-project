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

### ...

&exist; ??? . ParticipatedWithResults(id, year, s, e, medal) &and; medal &ne; "None" &and; HasCapitalLatitude(id, caplat_a) &and; EditionIsInCountry(year, cc) &and; HasCapitalLatitude(cc, caplat_c) &and; MoltoDiverse??(caplat_a, caplat_c)

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