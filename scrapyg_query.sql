-- basic query for a date & limit
SELECT * FROM fares
where datescraped = '2016-02-01'
limit 10

-- inspect with AMTRAK markets
SELECT fares.*, ca.origin as amtrakorig, cd.origin as amtrakdest FROM fares
FULL OUTER JOIN ghcity ca ON fares.orig = ca.zip_code
FULL OUTER JOIN ghcity cd ON fares.dest = cd.zip_code
order by id

-- inspect the cities key
select * from ghcity

