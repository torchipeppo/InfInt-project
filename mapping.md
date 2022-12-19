<!-- &#8364; &#x20AC; &euro; -->
<!-- &exist; &forall; &xrarr; -->

<!--

BASTA. Non vale la pena di complicare tutto quanto, solo per aggiungere un atro csv al mischiotto.




# Assumptions

* The athlete IDs of the two athlete_event* tables are disjoint. Verified to be true with my specific dataset.

# Definiamo formule frequenti

AthleteIdentifiesAtRio(tokyoid, otherid) : &exist; x1,x2,x3,x4,x5,x6,x7,y1,y2,y3,y4,y5,y6,y7,y8 . (
    
* athlete_event_tokyo(x1, tokyoid, tokyoname, tokyogender, tokyoage, tokyonoc, x2, x3, x4, x5, x6, x7) &and;

* athlete_event(otherid, othername, othergender, otherage, y1, y2, y3, othernoc, 2016, y4, y5, y6, y7, y8) &and;

* EquivalentNames(tokyoname, othername) &and;

* tokyogender = othergender &and;

* tokyonoc = othernoc &and;

* plus(otherage, 5, tokyoage)

)



AthleteIdentifiesAtLondon(tokyoid, otherid) : &exist; x1,x2,x3,x4,x5,x6,x7,y1,y2,y3,y4,y5,y6,y7,y8 . (
    
* athlete_event_tokyo(x1, tokyoid, tokyoname, tokyogender, tokyoage, tokyonoc, x2, x3, x4, x5, x6, x7) &and;

* athlete_event(otherid, othername, othergender, otherage, y1, y2, y3, othernoc, 2012, y4, y5, y6, y7, y8) &and;

* EquivalentNames(tokyoname, othername) &and;

* tokyogender = othergender &and;

* tokyonoc = othernoc &and;

* plus(otherage, 9, tokyoage)

)

*(Note: the two differ only in the year in athlete_event and the number in plus)*

-->






# MAPPING

&forall; id . (&exist; n,s,a,h,w,t,noc,y,se,c,sp,e,m . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &xrarr; Athlete(id))

&forall; isocode . (&exist; id,n,s,a,h,w,t,noc,y,se,c,sp,e,m,cn,cf . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(cn, noc, cf, isocode) &xrarr; Country(isocode))

&forall; year . (&exist; id,n,s,a,h,w,t,noc,year,se,c,sp,e,m . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &xrarr; Edition(year))

&forall; id, name . (&exist; s,a,h,w,t,noc,y,se,c,sp,e,m . athlete_event(id, name, s, a, h, w, t, noc, y, se, c, sp, e, m) &xrarr; HasName(id, name))

&forall; isocode, name . (&exist; id,n,s,a,h,w,t,noc,y,se,c,sp,e,m,cf . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(name, noc, cf, isocode) &xrarr; HasName(isocode, name))

&forall; year, city . (&exist; id,n,s,a,h,w,t,noc,year,se,c,sp,e,m,hc . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &and; hosted(year, hc, city) &xrarr; HasName(year, city))

&forall; id, sex . (&exist; n,a,h,w,t,noc,y,se,c,sp,e,m . athlete_event(id, n, sex, a, h, w, t, noc, y, se, c, sp, e, m) &xrarr; HasSex(id, sex))

&forall; id, year, age . (&exist; n,s,h,w,t,noc,se,c,sp,e,m . athlete_event(id, n, s, age, h, w, t, noc, year, se, c, sp, e, m) &xrarr; HadAge(id, year, age))

&forall; id, year, sport, event, medal . (&exist; n,s,a,h,w,t,noc,se,c . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sport, event, medal) &xrarr; ParticipatedWithResults(id, year, sport, event, medal))

&forall; id, isocode . (&exist; n,s,a,h,w,t,noc,y,se,c,sp,e,m,cn,cf . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(cn, noc, cf, isocode) &xrarr; IsInCountry(id, isocode))

&forall; year, isocode . (&exist; id,n,s,a,h,w,t,noc,se,c,sp,e,m,cname,city,ci,cf . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &and; hosted(year, cname, city) &and; countrycodes(cname, ci, cf, isocode) &xrarr; IsInCountry(year, isocode))

&forall; isocode, year, gold, silver, bronze . (&exist; hco, hci, cn, noc, cn2, cf . country_medals(year, hco, hci, cn, noc, gold, silver, bronze) &and; countrycodes(cn2, noc, cf, isocode) &xrarr; GotTotalMedals(isocode, year, gold, silver, bronze))

&forall; isocode, year, class . (&exist; cn . income_group(cn, isocode, year, class) &xrarr; HadIncomeClass(isocode, year, class))

&forall; isocode, pop . (&exist; y61, y62, ..., y99, y00, ..., y21 . population(isocode, pop, y61, ..., y21) &xrarr; HadPopulation(isocode, 1960, pop))

&forall; isocode, pop . (&exist; y60, y62, ..., y99, y00, ..., y21 . population(isocode, y60, pop, y62, ..., y21) &xrarr; HadPopulation(isocode, 1961, pop))

&forall; isocode, pop . (&exist; y60, y61, ..., y99, y00, ..., y20 . population(isocode, y60, ..., y20, pop) &xrarr; HadPopulation(isocode, 2021, pop))

&forall; isocode, caplat . (&exist; caplon, continent . countrydata(isocode, caplat, caplon, continent) &xrarr; HasCapitalLatitude(isocode, caplat))

&forall; id, caplat . (&exist; n,s,a,h,w,t,noc,y,se,c,sp,e,m,cn,cf,caplon,continent . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(cn, noc, cf, isocode) &and; countrydata(isocode, caplat, caplon, continent) &xrarr; HasCapitalLatitude(id, caplat))

&forall; year, caplat . (&exist; id,n,s,a,h,w,t,noc,se,c,sp,e,m,cname,city,ci,cf,caplon,continent . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &and; hosted(year, cname, city) &and; countrycodes(cname, ci, cf, isocode) &and; countrydata(isocode, caplat, caplon, continent) &xrarr; HasCapitalLatitude(year, caplat))

&forall; isocode, caplat . (&exist; caplat, caplon . countrydata(isocode, caplat, caplon, continent) &xrarr; IsInContinent(isocode, continent))

&forall; id, caplat . (&exist; n,s,a,h,w,t,noc,y,se,c,sp,e,m,cn,cf,caplat,caplon . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(cn, noc, cf, isocode) &and; countrydata(isocode, caplat, caplon, continent) &xrarr; IsInContinent(id, continent))

&forall; year, caplat . (&exist; id,n,s,a,h,w,t,noc,se,c,sp,e,m,cname,city,ci,cf,caplat,caplon . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &and; hosted(year, cname, city) &and; countrycodes(cname, ci, cf, isocode) &and; countrydata(isocode, caplat, caplon, continent) &xrarr; IsInContinent(year, continent))
