### atleti con carriera interessante (tipo, vince per la prima volta dopo N tentativi di fila, oppure vince bronzo->argento->oro in tre edizioni consecutive, ...)

&exist; year1, year2, year3, sport, event, finalmedal . ParticipatedWithResults(id, year1, sport, event, "None") &and; ParticipatedWithResults(id, year2, sport, event, "None") ParticipatedWithResults(id, year3, sport, event, finalmedal) &and; FollowedBy(year1, year2) &and; FollowedBy(year2, year3) &and; finalmedal &ne; "None" *(N=3, estendibile ad altri N)*

&exist; year1, year2, year3, sport, event . ParticipatedWithResults(id, year1, sport, event, Bronze) &and; ParticipatedWithResults(id, year2, sport, event, Silver) ParticipatedWithResults(id, year3, sport, event, Gold) &and; FollowedBy(year1, year2) &and; FollowedBy(year2, year3)

### atleti con carriera interessante X geografia (tipo, vince una medaglia nello stesso sport in due continenti diversi, o batte il padrone di casa, o vince a una latitudine molto diversa dalla propria, ...)

&exist; year1, year2, sport, e1, e2, medal1, medal2, cc1, cc2, cont1, cont2 . ParticipatedWithResults(id, year1, sport, e1, medal1) &and; ParticipatedWithResults(id, year2, sport, e2, medal2) &and; medal1 &ne; "None" &and; medal2 &ne; "None" &and; EditionIsInCountry(year1, cc1) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc1, cont1) &and; IsInContinent(cc2, cont2) &and; cont1 &ne; cont2 *(Potremmo pensare di farci dare pure i continenti...?)*

(&exist; id_home_guy, year, sport, event, medal_p, medal_h, other_cc, home_cc . ParticipatedWithResults(id_protagonist_guy, year, sport, event, medal_p) &and; ParticipatedWithResults(id_home_guy, year, sport, event, medal_h) &and; EditionIsInCountry(year, home_cc) &and; AthleteIsInCountry(id_home_guy, home_cc) &and; AthleteIsInCountry(id_protagonist_guy, other_cc) &and; other_cc &ne; home_cc &and; ~~medal_p &ne; "None" &and; medal_h &ne; "None"~~ &and; medal_p = "Gold" &and; medal_h = "Silver") &or; (&exist; ... &and; medal_p = "Gold" &and; medal_h = "Bronze") &or; (&exist; ... &and; medal_p = "Silver" &and; medal_h = "Bronze") *(Unione di query congiuntive)* *(N.B.: Richiediamo anche al padrone di casa di aver vinto una medaglia per evitare un numero eccessivo di risultati, la descrizione della query andrà sistemata di conseguenza se scegliamo questa)*

&exist; ??? . ParticipatedWithResults(id, year, s, e, medal) &and; medal &ne; "None" &and; HasCapitalLatitude(id, caplat_a) &and; EditionIsInCountry(year, cc) &and; HasCapitalLatitude(cc, caplat_c) &and; MoltoDiverse??(caplat_a, caplat_c)

### data un'edizione, esaminare la distribuzione delle (fasce di) PIL presenti nelle nazioni con più di X medaglie vinte in quell'edizione (forse affiancarla con tale distrubizione senza il vincolo in classifica)

&exist; gold, silver, bronze . GotTotalMedals(cc, year, gold, silver, bronze) &and; gold &ne; 0 &and; gold &ne; 1 &and; ... &and; gold &ne; X &and; HadIncomeClass(cc, year, class)

*(Ta-daa! Non c'è bisogno della tabella gt! Ciò non toglie che magari in fase di implementazione usi l'operatore di confronto di SQL.)*

Al solo scopo di contare meglio, si può fare un'altra query SQL espansa con COUNT e GROUP BY.

### Le nazioni con almeno N atleti che hanno partecipato a giochi fuori dal proprio continente ~~(lo stesso atleta conta più volte se ha partecipato ad altrettante edizioni extracontinentali)~~. Affiancare alla fascia di GNI che la nazione aveva in uno qualunque degli anni considerati (la stessa nazione potrebbe comparire più volte se più fasce sono applicabili, ma tanto le fasce sono solo quattro, quindi mi preoccupo poco).

&exist; home_cont, id1, id2, id3, year1, year2, year3, s1, s2, s3, e1, e2, e3, m1, m2, m3, cc1, cc2, cc3, cont1, cont2, cont3 . IsInContinent(home_cc, home_cont) &and; AthleteIsInCountry(id1, home_cc) &and; ParticipatedWithResults(id1, year1, s1, e1, m1) &and; EditionIsInCountry(year1, cc1) &and; IsInContinent(cc1, cont1) &and; cont1 &ne; home_cont &and; AthleteIsInCountry(id2, home_cc) &and; ParticipatedWithResults(id2, year2, s2, e2, m2) &and; EditionIsInCountry(year2, cc2) &and; IsInContinent(cc2, cont2) &and; cont2 &ne; home_cont &and; AthleteIsInCountry(id3, home_cc) &and; ParticipatedWithResults(id3, year3, s3, e3, m3) &and; EditionIsInCountry(year3, cc3) &and; IsInContinent(cc3, cont3) &and; cont3 &ne; home_cont &and; id1 &ne; id2 &and; id1 &ne; id3 &and; id2 &ne; id3 &and; HadIncomeClass(home_cc, year1, class) *(N=3, estendibile ad altri N)*
