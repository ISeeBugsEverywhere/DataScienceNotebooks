-- WITH AS konstrukcija 

-- WITH <name. AS 
-- 	(SELECT * FROM *)
-- SELECT * FROM <name>; 

-- WITH 
-- <t1> AS (SELECT * FROM *),
-- <t2> AS (SELECT * FROM *)
-- SELECT * FROM <t1> JOIN <t2> USING <col1>;


with T1 as 
(select actor_id, first_name from sakila.actor)  -- priskiriame T1 
select * from t1;


-- -----------------------------------------------------------------------------------------------
-- DVI VIENODOS LENTELES, SKIRTINGI BUDAI

with 
	T1 as  (select * from 'life-expectancy' where Year = 2019),
    T2 as (select substring(Name, 2, length(Name)) as Country, 
    'Constitutional form' from gov_forms)
select * from T1 inner join T2
on T1.Entity = T2.Country
where Code = 'LTU';


WITH 
    T1 AS (SELECT * FROM 'life-expectancy' WHERE Year = 2019),
    T2 AS (SELECT substring(Name, 2, length(Name)) AS Country, Constitutional_form FROM gov_forms)
SELECT * FROM T1
INNER JOIN T2 ON T1.Entity = T2.Country;


select *
from 
(select * from 'life-expectancy' where Year = 2019) as T1 
inner join 
(select * from gov_forms) as T2
using (Entity);


WITH 
    T1 AS (SELECT * FROM life-expectancy WHERE Year = 2019),
    T2 AS (SELECT substring(Name, 2, length(Name)) AS Country, Constitutional_form FROM gov_forms)
SELECT * FROM T1
INNER JOIN T2 ON T1.Entity = T2.Country;

-- -----------------------------------------------------------------------------------------------
-- ROW_NUMBER()


select *, row_number() over (order by 'Constitutional form') as rn 
from gov_forms;


select *, row_number() over (order by 'Life expectancy' desc) as rn 
from `life-expectancy`   -- sie du order by veikia atskirai (rikiavimas)
order by Entity asc;


WITH t1 AS (
    SELECT *, row_number() OVER (ORDER BY "Life expectancy" DESC) AS rn
    FROM `life-expectancy`
    WHERE Year = 2019
)
SELECT * FROM t1
WHERE Code = 'LTU';

select * from 
(select *, 
row_number() over(partition by name) as rn  -- partitiona pagal irasu kieki ir nurodome kuriame stulpelyje -- row number numeruoja 
from gov_forms) as T
where rn = 1;  -- --pvz kaip eliminuoti pasikartojancius irasus

with T1 as 
(select gamintojas, modelis, price,
row_number() over (partition by gamintojas, modelis order by cast(replace(price, ' ', '') as float) desc) as rn
from autopliuslt)
select * from T1 
where rn <4;

-- -----------------------------------------------------------------------------------------------
-- Kiek skirtingų profesijų/profesijų grupių  buvo apklausta 2014 ir 2018 metais? 
-- Pateikite skirtumą tarp jų kiekio 2014 ir 2018 metais,
--  jei toks yra. 



select * from
(
select count(*) as C18
from (SELECT profesija, 
row_number() OVER (PARTITION BY profesija ORDER BY profesija desc) AS rn
FROM DUS2018N
) as T
where rn =1;
)


select count(*) as C14
from (SELECT profesija, 
row_number() OVER (PARTITION BY profesija ORDER BY profesija desc) AS rn
FROM DUS2014N
) as B
where rn =1;


select * from
(select count(*) as C18
from (SELECT profesija, 
row_number() OVER (PARTITION BY profesija ORDER BY profesija desc) AS rn
FROM DUS2018N
) as T
where rn =1)
join
(select count(*) as C14
from (SELECT profesija, 
row_number() OVER (PARTITION BY profesija ORDER BY profesija desc) AS rn
FROM DUS2014N
) as B
where rn =1;


-- -----------------------------------------------------------------------------------------------
-- TEISINGAS SPRENDIMAS

select *, C18-C14 as Δ  from
(select count(*) as C14 from
(select count(*), profesija from DUS2014N group by profesija) as T1) as T2
join
(select count(*) as C18 from
(select count(*), profesija from DUS2018N group by profesija) as T1) as T3;


select count(distinct lytis) from DUS2014N; -- grazina unikalius irasus ir countas suskaiciuoja 


-- -----------------------------------------------------------------------------------------------
-- Suraskite 5-kis top telefonų gamintojus. Kiek vienetų kiekvieno gamintojo telefonų 
-- turėjo klientai?
-- jei gamintojas (brand) nenurodytas - atmeskite.
-- Lentele sa

select device_brand, count(*) as kiekis from sa 
where device_brand is not null AND device_brand <> ''
group by device_brand
order by kiekis desc
limit 5;

-- Kiek rinkos dalies užėmė šie 5-ki gamintojai? Pateikite tai procentais.
-- Jei gamintojas nenurodytas, priskirkite tą įrašą prie 'Other brands'.




-- SELECT A.Gamintojas, A.kiekis, (A.Kiekis * 100 ) / B.Rinka as Rinkos_dalis
-- FROM 
-- (
--     SELECT device_brand AS Gamintojas, COUNT(*) AS kiekis 
--     FROM sa 
--     WHERE device_brand IS NOT NULL OR device_brand <> '' as 'Other brands'
--     GROUP BY device_brand
--     ORDER BY kiekis DESC
--     LIMIT 6
-- ) AS A
-- Join
-- (
--     SELECT COUNT(*) AS Rinka
--     FROM sa
-- ) AS B;



SELECT A.Gamintojas, A.kiekis, (A.Kiekis * 100 ) / B.Rinka as Rinkos_dalis, A.rn
FROM 
(
    SELECT device_brand AS Gamintojas, COUNT(*) AS kiekis,
    row_number() OVER (ORDER BY kiekis desc) AS rn
    FROM sa 
    GROUP BY device_brand
    ORDER BY kiekis DESC
    LIMIT 100
) AS A
Join
(
    SELECT COUNT(*) AS Rinka
    FROM sa
) AS B




SELECT device_brand, COUNT(*) AS C
FROM sa
WHERE device_brand != ''
GROUP BY device_brand
ORDER BY C DESC
LIMIT 10;



select *, C/(select count(*) from sa)*100 as '%' from
(select * from
(select device_brand as B, count(*) as C
from sa
where device_brand != ''
group by device_brand
order by C desc
limit 5) as T1
union all
select 'Others', count(*) as C
from sa
where device_brand not in
(select B from (select device_brand as B, count(*) as C
from sa
where device_brand != ''
group by device_brand
order by C desc
limit 5) as T2)) as T3;


-- rinkos dalis (KITAS SPRENDIMAS)

select count(*) as Kiekis, count(*)/(select count(*) from sa)*100 as `Rinkos dalis`,
case 
when device_brand in (select * from(select brand from
(select count(*) as kiekis, device_brand as brand  from sa where device_brand<>'' group by device_brand) as D
order by kiekis desc limit 5)as f) then device_brand
else 'Other'
end as Brand from sa
group by Brand
order by kiekis desc;

