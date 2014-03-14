SELECT bbs.counts.countrynum, bbs.counts.statenum, bbs.counts.route, bbs.routes.lati, bbs.routes.loni, bbs.counts.year, bbs.species.aou, bbs.species.genus, bbs.species.species
FROM bbs.counts
JOIN bbs.species ON bbs.counts.aou = bbs.species.aou
JOIN bbs.weather ON bbs.counts.countrynum = bbs.weather.countrynum AND bbs.counts.statenum = bbs.weather.statenum AND bbs.counts.route = bbs.weather.route AND bbs.counts.rpid = bbs.weather.rpid AND bbs.counts.year = bbs.weather.year
JOIN bbs.routes ON bbs.counts.countrynum = bbs.routes.countrynum AND bbs.counts.statenum = bbs.routes.statenum AND bbs.counts.route = bbs.routes.route
WHERE bbs.weather.runtype = 1
LIMIT 100

SELECT statenum * 1000 + route, lati, loni, stratum, bcr
FROM routes
