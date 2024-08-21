select lytis, GROUP_CONCAT(bdu_spalio)
from DUS2014N du14 group by lytis;

SELECT gamintojas, count(*) as n, GROUP_CONCAT(price) AS p
FROM autopliuslt 
GROUP BY gamintojas;

SELECT gamintojas, count(*) n, GROUP_CONCAT(cast(replace(price,' ','') as float)) kainos
FROM works.autopliuslt 
GROUP BY gamintojas
order by n desc limit 5;

-- Besikartojančių ID eliminavimas panaudojant ROW_NUMBER()
WITH T1 AS
(SELECT gamintojas, modelis, id, price, ROW_NUMBER() OVER (PARTITION BY id) AS rn FROM autopliuslt)
SELECT * FROM T1
WHERE rn = 1
ORDER BY id ASC;

SELECT * FROM
(SELECT gamintojas, modelis, id, price, ROW_NUMBER() OVER (PARTITION BY id) AS rn FROM autopliuslt)
as T1
WHERE rn=1;

SELECT gamintojas, count(*) n, 
	GROUP_CONCAT(cast(replace(price,' ','') as float)) kainos
FROM (
	SELECT gamintojas, modelis, id, price, 
		ROW_NUMBER() OVER (PARTITION BY id) AS rn FROM autopliuslt
) as T1
WHERE rn=1
GROUP BY gamintojas
order by n desc limit 5;

-- Vidutinė kaina:
SELECT avg(cast(replace(price,' ','') as float)) vidKaina
FROM (
	SELECT id, price, 
		ROW_NUMBER() OVER (PARTITION BY id) AS rn FROM works.autopliuslt
) as T1
WHERE rn=1;

-- Paprastasis vidurkis:
SELECT avg(cast(replace(price,' ','') as float)) vidKaina
FROM works.autopliuslt;

-- Vidurkis atmetus besikartojančius:
SELECT avg(cast(replace(price,' ','') as float)) vidKaina
FROM ( SELECT id, price, 
ROW_NUMBER() OVER (PARTITION BY id) AS rn FROM works.autopliuslt
) as T1 WHERE rn=1;

# suraskite visus gamintojus, kurių  modelių vidutinė kaina yra didesnė už vidutinę

select gamintojas, avg(cast(replace(price,' ','') as float)) vidKaina
from autopliuslt
group by gamintojas;

select * from 
(select gamintojas,	
	round(avg(cast(replace(price,' ','') as float))) gamintojoVidurkis,
	GROUP_CONCAT(cast(replace(price,' ','') as float)) kainos
from autopliuslt
group by gamintojas) as vidurkiai
where gamintojoVidurkis>(SELECT avg(cast(replace(price,' ','') as float)) bendrasisVidurkis
FROM works.autopliuslt);

# visų automobilių kainą.
# Iš jų atrinkite 5-kis brangiausius gamintojus, ir suraskite jų 
# parduodamų modelių vidutinį amžių.
# taip pat atvaizduokite su boxplot'ais šių 5-kių gamintojų parduodamų modelių kainų pasiskirstymą.

