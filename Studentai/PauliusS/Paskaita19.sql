
select * from gov_forms;
select * from `life-expectancy`;




-- ar yra priklausomybė tarp šalių konstitucinės santvarkos ir vidutinės gyvenimo trukmės?

select length(Name) from works.gov_forms;
select length(substring(Entity, .3)) from `life-expectancy`;

select LE.year, GF.`Constitutional form`, round(avg(`Life expectancy`),0), group_concat(substring(Name,2)) from works.gov_forms as GF
left join `life-expectancy` as LE
on substring(Name,2) = LE.Entity    -- apsikarpome, nes stulpeliuose ne vienodi saliu pavadinimai (9 ir 11 simboliai).
-- where LE.Year = 2018
group by GF.`Constitutional form`, LE.Year;


-- suraskite tris valstybes, kurios yra su ilgiausia gyvenimo trukme, tris su mažiausia, ir palyginkite su Lietuva. (2019 metams)

(
  SELECT Name, `Life expectancy`
  FROM gov_forms AS GF
  LEFT JOIN `life-expectancy` AS LE
  ON SUBSTRING(Name, 2) = LE.Entity
  WHERE LE.`Life expectancy` IS NOT NULL and LE.Year = 2019
  GROUP BY Name
  ORDER BY AVG(`Life expectancy`) DESC
  LIMIT 3
)
UNION ALL
(
  SELECT Name, `Life expectancy`
  FROM gov_forms AS GF
  LEFT JOIN `life-expectancy` AS LE
  ON SUBSTRING(Name, 2) = LE.Entity
  WHERE LE.`Life expectancy` IS NOT NULL and LE.Year = 2019
  GROUP BY Name
  ORDER BY AVG(`Life expectancy`) ASC
  LIMIT 3
)
UNION ALL
(
  SELECT Name, `Life expectancy`
  FROM gov_forms AS GF
  LEFT JOIN `life-expectancy` AS LE
  ON SUBSTRING(Name, 2) = LE.Entity
  WHERE Name like '%Lith%' and LE.Year = 2019
  GROUP BY Name
);

-- DUS2014N ir DUS2018N,
-- suraskite 
-- kiek dalyvavo respondentų iš kiekvienos amžiaus grupės?alter
-- koks buvo vidutinis atlyginimas pagal amžiaus grupę?
-- (4 atskiros SQL užklausos)
-- Parodykite vienoje lentelėje ansktesnius duomenis ir pateikite
-- skirtumus tarp atlyginimų, dalyvių kiekių.



select 
case 
when amzius = '14-19' or amzius = '20-29' then '14-29'
else amzius 
end as naujas_amzius, count(amzius), avg(bdu_spalio)/3.456 from DUS2014N 
group by naujas_amzius;

select amzius, count(amzius), avg(bdu_spalio) from DUS2018N as B
group by amzius;



-- TEISINGAS SPRENDIMAS 
select *, C18-C14 as Δ,
A18-A14 as `Δ€`
from
(select case
when amzius = '14-19' then '14-29'
when amzius = '20-29' then '14-29'
else amzius
end as Amz,
count(*) as C14, round(avg(bdu_spalio)/3.4528) as A14
from DUS2014N
group by Amz) as T14
join
(select amzius as Amz, count(*) as C18, round(avg(bdu_spalio)) as A18
from DUS2018N
group by amzius) as T18
using (Amz);






select avg(bdu_spalio)/3.456 as vidutinis from DUS2014N;    -- vidutinis atlyginimas 

select lytis, count(*) from DUS2014N
where lytis = 'F' and bdu_spalio > (select avg(bdu_spalio)/3.456 as vidutinis from DUS2014N);




select lytis, count(lytis), avg(bdu_spalio)/3.456 from DUS2014N
group by lytis;

select lytis, bdu_spalio from DUS2018N
where lytis = 'F'
CASE 
when bdu_spalio > 684 then 'Daugiau'
else 'Maziau';





select actor_id as ID,
CASE
when actor_id MOD 2 = 0 then 'Lyginis'
else 'Nelyginis'
END AS Lyginumas
from actor
order by Lyginumas asc, ID desc;


-- Kiek respondenčių moterų uždirbo 2014 bei 2018 metais daugiau, nei vidutinį atlyginimą?
-- Kiek tai buvo daugiau/mažiau, lyginant su vyrų kiekiais, uždirbusiais daugiau, nei vidutinį 
-- atlyginimą, atitinkamais metais? (procentais, jei pavyksta)

select avg(bdu_spalio)/3.456 as vidutinis from DUS2014N;    -- vidutinis atlyginimas 2014 

select avg(bdu_spalio) as vidutinis from DUS2018N;   -- vidutinis atlyginimas 2018


select count(*) from DUS2014N
where lytis = 'F' and bdu_spalio/3.456 > (select avg(bdu_spalio)/3.456 as vidutinis from DUS2014N);  -- 7138 moteru daugiau nei vidurkis


select *, ABC - CBD from 
(
select lytis, count(*) as ABC from DUS2014N
where bdu_spalio > (select avg(bdu_spalio) as vidutinis from DUS2014N)
group by lytis
) as A
INNER JOIN
(
select lytis, count(*) as CBD from DUS2018N
where bdu_spalio > (select avg(bdu_spalio) as vidutinis from DUS2018N)
group by lytis
) as B
-- on B.lytis = A.lytis;
using (lytis);



-- select * from 
-- table left 
-- inner join
-- table right 
-- using (col_name);


-- Surūšiuokite respondentus pagal mėnesio pajamų rėžius - 'Iki MMA', 'Tarp MMA ir VDU', 'VDU ir daugiau'.
-- MMA 2014 metais - 1000 Lt. MMA 2018 metais - 400 €.
-- Suskaičiuokite, kiek kiekvienoje grupėje buvo respondentų, tiek 2014, tiek 2018 metais.
-- case, group by


select avg(bdu_spalio) as vidutinis from DUS2014N;    -- vidutinis atlyginimas 2014 

select avg(bdu_spalio) as vidutinis from DUS2018N;   -- vidutinis atlyginimas 2018

SELECT * from 
(
SELECT
  CASE
    WHEN bdu_spalio < 1000 THEN 'mažiau nei MMA'
    WHEN bdu_spalio BETWEEN 1000 AND (select avg(bdu_spalio) as vidutinis from DUS2014N) THEN 'tarp VDU ir MMA'
    WHEN bdu_spalio > (select avg(bdu_spalio) as vidutinis from DUS2014N) THEN 'daugiau nei MMA'
  END AS 'tipas',
  count(*) as '2014'
FROM DUS2014N
group by tipas
) as A
INNER JOIN
(
SELECT
  CASE
    WHEN bdu_spalio < 400 THEN 'mažiau nei MMA'
    WHEN bdu_spalio BETWEEN 400 AND (select avg(bdu_spalio) as vidutinis from DUS2018N) THEN 'tarp VDU ir MMA'
    WHEN bdu_spalio > (select avg(bdu_spalio) as vidutinis from DUS2018N) THEN 'daugiau nei MMA'
  END AS 'tipas',
  count(*) as '2018'
FROM DUS2018N
group by tipas) as B
on *;











