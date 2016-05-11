-- basic query for a date & limit
SELECT * FROM fares
where datescraped = '2016-02-01'
limit 10

-- inspect with AMTRAK markets
SELECT fares.*, ca.origin as amtrakorig, cd.origin as amtrakdest FROM fares
FULL OUTER JOIN ghcity ca ON fares.orig = ca.zip_code
FULL OUTER JOIN ghcity cd ON fares.dest = cd.zip_code
order by id
limit 10

-- inspect the cities key
select * from ghcity

/*Check number of rows per datescraped in database*/
select datescraped, count(webfare) from fares
group by datescraped
order by datescraped

/*Check number of rows per datescraped and date in database*/
select datescraped, date, count(webfare) from fares
group by datescraped, date
order by datescraped, date

/*Check number of rows in database*/
select count(*) from fares


/*Check origins and destinations by datescraped*/
select orig, dest, count(webfare) from fares
where datescraped = '4/21/2016'
group by orig, dest
order by orig, dest