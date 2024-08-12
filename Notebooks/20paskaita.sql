-- select *, row_number() over (order by Entity) as E from `life-expectancy`;
select * from
(select Entity, `Life expectancy` as LE from `life-expectancy`
where Year = 2019
order by LE desc limit 3) as T
union all
select Entity, `Life expectancy` as LE from `life-expectancy`
where Year = 2019 and Entity = 'Lithuania'
union all
select * from
(select Entity, `Life expectancy` as LE from `life-expectancy`
where Year = 2019
order by LE asc limit 3) as T2;

-- DUS2014N ir DUS2018N,
-- suraskite 
-- kiek dalyvavo respondentų iš kiekvienos amžiaus grupės?alter
-- koks buvo vidutinis atlyginimas pagal amžiaus grupę?
-- (4 atskiros SQL užklausos)

select amzius, count(*) as C14, round(avg(bdu_spalio)/3.4528) as A14
from DUS2014N
group by amzius;

select amzius as Amz, count(*) as C18, round(avg(bdu_spalio)) as A18
from DUS2018N
group by amzius;

-- amžiaus grupių suvienodinimas
select case
when amzius = '14-19' then '14-29'
when amzius = '20-29' then '14-29'
else amzius
end as Amz,
count(*) as C14, round(avg(bdu_spalio)/3.4528) as A14
from DUS2014N
group by Amz;



-- Parodykite vienoje lentelėje ansktesnius duomenis ir pateikite
-- skirtumus tarp atlyginimų, dalyvių kiekių.


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


-- Kiek respondenčių moterų uždirbo 2014 bei 2018 metais daugiau,
--  nei vidutinį atlyginimą?
-- Kiek tai buvo daugiau/mažiau, lyginant su vyrų kiekiais, 
-- uždirbusiais daugiau, nei vidutinį atlyginimą, 
-- atitinkamais metais? (procentais, jei pavyksta
select * from
(select * from
(select 
case
when bdu_spalio >= (select avg(bdu_spalio) from DUS2014N) then 'Daugiau nei vid.'
else 'Mažiau nei vid.'
end as 'MD', count(*) as KiekisMot2014
from DUS2014N
where lytis = 'F'
group by `MD`) as T1
join
(select 
case
when bdu_spalio >= (select avg(bdu_spalio) from DUS2014N) then 'Daugiau nei vid.'
else 'Mažiau nei vid.'
end as 'MD', count(*) as KiekisVyr2014
from DUS2014N
where lytis = 'M'
group by `MD`) as T2
using (MD)) as T14
join

(select * from
(select 
case
when bdu_spalio >= (select avg(bdu_spalio) from DUS2018N) then 'Daugiau nei vid.'
else 'Mažiau nei vid.'
end as 'MD', count(*) as KiekisMot2018
from DUS2018N
where lytis = 'F'
group by `MD`) as T1
join
(select 
case
when bdu_spalio >= (select avg(bdu_spalio) from DUS2018N) then 'Daugiau nei vid.'
else 'Mažiau nei vid.'
end as 'MD', count(*) as KiekisVyr2018
from DUS2018N
where lytis = 'M'
group by `MD`) as T2
using (MD)) as T18

using (MD);

-- Surūšiuokite respondentus pagal mėnesio pajamų rėžius - 'Iki MMA', 
-- 'Tarp MMA ir VDU', 'VDU ir daugiau'.
-- MMA 2014 metais - 1000 Lt. MMA 2018 metais - 400 €.
-- Suskaičiuokite, kiek kiekvienoje grupėje buvo respondentų, tiek 2014, tiek 2018 metais.

select case
when bdu_spalio < 1000 then 'Iki MMA'
when bdu_spalio >= 1000 and bdu_spalio < (select avg(bdu_spalio) from DUS2014N) then 'Trap MMA ir VDU'
else 'Virš VDU'
end as Rėžiai,
count(*) as Kiekis2014
from DUS2014N
group by Rėžiai;


