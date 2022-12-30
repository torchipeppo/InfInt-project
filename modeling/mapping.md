&forall; id . (&exist; n,s,a,h,w,t,noc,y,se,c,sp,e,m . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &xrarr; Athlete(id))

&forall; isocode . (&exist; id,n,s,a,h,w,t,noc,y,se,c,sp,e,m,cn,cf . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(cn, noc, cf, isocode) &xrarr; Country(isocode))

&forall; year . (&exist; id,n,s,a,h,w,t,noc,year,se,c,sp,e,m . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &xrarr; Edition(year))

&forall; id, name . (&exist; s,a,h,w,t,noc,y,se,c,sp,e,m . athlete_event(id, name, s, a, h, w, t, noc, y, se, c, sp, e, m) &xrarr; HasName(id, name))

&forall; isocode, name . (&exist; id,n,s,a,h,w,t,noc,y,se,c,sp,e,m,cf . athlete_event(id, n, s, a, h, w, t, noc, y, se, c, sp, e, m) &and; countrycodes(name, noc, cf, isocode) &xrarr; HasName(isocode, name))

&forall; id, sex . (&exist; n,a,h,w,t,noc,y,se,c,sp,e,m . athlete_event(id, n, sex, a, h, w, t, noc, y, se, c, sp, e, m) &xrarr; HasSex(id, sex))

&forall; id, year, age . (&exist; n,s,h,w,t,noc,se,c,sp,e,m . athlete_event(id, n, s, age, h, w, t, noc, year, se, c, sp, e, m) &xrarr; HadAge(id, year, age))

&forall; id, year, sport, event, medal . (&exist; n,s,a,h,w,t,noc,se,c . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sport, event, medal) &xrarr; ParticipatedWithResults(id, year, sport, event, medal))

&forall; id, year, isocode . (&exist; n,s,a,h,w,t,noc,se,c,sp,e,m,cn,cf . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, e, m) &and; countrycodes(cn, noc, cf, isocode) &xrarr; AthleteWasFromCountry(id, year isocode))

&forall; year, isocode . (&exist; cname,city,ci,cf . hosted(year, cname, city) &and; countrycodes(cname, ci, cf, isocode) &xrarr; EditionIsInCountry(year, isocode))

&forall; isocode, year, gold, silver, bronze . (&exist; cn, noc, cn2, cf . country_medals(year, cn, noc, gold, silver, bronze) &and; countrycodes(cn2, noc, cf, isocode) &xrarr; GotTotalMedals(isocode, year, gold, silver, bronze))

&forall; isocode, year, class . (&exist; cn . income_group(cn, isocode, year, class) &xrarr; HadIncomeClass(isocode, year, class))

&forall; isocode, pop . (&exist; y61, y62, ..., y99, y00, ..., y21 . population(isocode, pop, y61, ..., y21) &xrarr; HadPopulation(isocode, 1960, pop))

&forall; isocode, pop . (&exist; y60, y62, ..., y99, y00, ..., y21 . population(isocode, y60, pop, y62, ..., y21) &xrarr; HadPopulation(isocode, 1961, pop))

&forall; isocode, pop . (&exist; y60, y61, ..., y99, y00, ..., y20 . population(isocode, y60, ..., y20, pop) &xrarr; HadPopulation(isocode, 2021, pop))

&forall; isocode, caplat . (&exist; caplon, continent . countrydata(isocode, caplat, caplon, continent) &xrarr; HasCapitalLatitude(isocode, caplat))

&forall; isocode, continent . (&exist; caplat, caplon . countrydata(isocode, caplat, caplon, continent) &xrarr; IsInContinent(isocode, continent))

# Soffitta

&forall; id, year, continent . (&exist; n,s,a,h,w,t,noc,se,c,sp,ev,m,cname,city,ci,cf,isocode,caplat,caplon . athlete_event(id, n, s, a, h, w, t, noc, year, se, c, sp, ev, m) &and; hosted(year, cname, city) &and; countrycodes(cname, ci, cf, isocode) &and; countrydata(isocode, caplat, caplon, continent) &xrarr; PlayedInContinent(id, year, continent))
