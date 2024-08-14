-- Ar yra priklausomybė tarp šalių konstitucinės santvarkos ir vidutinės gyvenimo trukmės?
SELECT LE.Year, GF.`Constitutional form`, round(avg(LE.`Life expectancy`),0), group_concat(substring(Name,2)) FROM works.gov_forms as GF
left join `life-expectancy` as LE
on substring(Name,2) = LE.Entity
-- where LE.Year = 2018
group by GF.`Constitutional form`, LE.Year
;
select length(substring(Name,2)) from gov_forms;
select length(Entity) from `life-expectancy`;

-- Suraskite tris valstybes, kurios yra su ilgiausia gyvenimo trukme, tris su mažiausia, ir palyginkite su Lietuva. (2018 metams)
select * from 
(select Entity, round(`Life expectancy`,0) as Life_expectancy from `life-expectancy`
where Year = 2019
order by `Life expectancy` desc
limit 3) as F
union 
select * from 
(select Entity, round(`Life expectancy`,0) as Life_expectancy from `life-expectancy`
where Year = 2019
order by `Life expectancy` asc
limit 3) as S
union
select * from 
(select Entity, round(`Life expectancy`,0) as Life_expectancy from `life-expectancy`
where Entity = 'Lithuania' and Year = 2019
) as T
order by  Life_expectancy desc
;

-- DUS2014N ir DUS2018N,
-- suraskite 
-- kiek dalyvavo respondentų iš kiekvienos amžiaus grupės?alter
-- koks buvo vidutinis atlyginimas pagal amžiaus grupę?
-- (4 atskiros SQL užklausos)
SELECT count(*) as Dalyviai, amzius, 2014 as Metai FROM DUS2014N
group by amzius;
SELECT count(*) as Dalyviai, amzius, 2018 as Metai FROM DUS2018N
group by amzius;
SELECT round(avg(bdu_spalio)/3.4528,0) as `Vidutinis atlyginimas`, amzius, 2014 as Metai FROM DUS2014N
group by amzius;
SELECT round(avg(bdu_spalio),0) as `Vidutinis atlyginimas`, amzius, 2018 as Metai FROM DUS2018N
group by amzius;
-- Parodykite vienoje lentelėje ansktesnius duomenis ir pateikite
-- skirtumus tarp atlyginimų, dalyvių kiekių.
select AG, D1.Dalyviai as D14, D2.Dalyviai as D18, A1.`Vidutinis atlyginimas` as A14, A2.`Vidutinis atlyginimas` as A18, D2.Dalyviai-D1.Dalyviai as Dskir, A2.`Vidutinis atlyginimas`-A1.`Vidutinis atlyginimas` as Askir  from
(SELECT count(*) as Dalyviai, 
case
when amzius = '14-19' then '14-29'
when amzius = '20-29' then '14-29'
else amzius
end as AG
FROM DUS2014N
group by AG) as D1
join
(SELECT count(*) as Dalyviai, amzius as AG FROM DUS2018N
group by amzius) as D2
using (AG)
join 
(SELECT round(avg(bdu_spalio)/3.4528,0) as `Vidutinis atlyginimas`, case
when amzius = '14-19' then '14-29'
when amzius = '20-29' then '14-29'
else amzius
end as AG FROM DUS2014N
group by AG) as A1
using (AG)
join
(SELECT round(avg(bdu_spalio),0) as `Vidutinis atlyginimas`, amzius as AG FROM DUS2018N
group by amzius) as A2
using (AG);

-- Kiek respondenčių moterų uždirbo 2014 bei 2018 metais daugiau, nei vidutinį atlyginimą?
select round(avg(bdu_spalio)/3.4528,0) from DUS2014N;
select count(*) as mot_sk, 2014 as Metai from DUS2014N
where (bdu_spalio/3.4528)>(select round(avg(bdu_spalio)/3.4528,0) from DUS2014N) and lytis = 'F'
union
select count(*) as mot_sk, 2018 as Metai from DUS2018N
where bdu_spalio>(select round(avg(bdu_spalio),0) from DUS2018N) and lytis = 'F';
-- Kiek tai buvo daugiau/mažiau, lyginant su vyrų kiekiais, uždirbusiais daugiau, nei vidutinį atlyginimą, atitinkamais metais? (procentais, jei pavyksta)
select Metai, S.mot_sk, F.vyr_sk,S.mot_sk-F.vyr_sk as Skirtumas , round((S.mot_sk-F.vyr_sk)/S.mot_sk*100,2) as Proc from
(select count(*) as vyr_sk, 2014 as Metai from DUS2014N
where bdu_spalio>(select avg(bdu_spalio) from DUS2014N) and lytis = 'M'
union
select count(*) as vyr_sk, 2018 as Metai from DUS2018N
where bdu_spalio>(select avg(bdu_spalio) from DUS2018N) and lytis = 'M') as F
left join
(select count(*) as mot_sk, 2014 as Metai from DUS2014N
where bdu_spalio>(select avg(bdu_spalio) from DUS2014N) and lytis = 'F'
union
select count(*) as mot_sk, 2018 as Metai from DUS2018N
where bdu_spalio>(select avg(bdu_spalio) from DUS2018N) and lytis = 'F') as S
using (Metai);

-- Surūšiuokite respondentus pagal mėnesio pajamų rėžius - 'Iki MMA', 'Tarp MMA ir VDU', 'VDU ir daugiau'.
select amzius, bdu_spalio, 2014 as Metai,
case
when bdu_spalio<1000 then 'Iki MMA'
when bdu_spalio between 1000 and (select avg(bdu_spalio) from DUS2014N) then 'Tarp MMA ir VDU'
when bdu_spalio>(select avg(bdu_spalio) from DUS2014N) then 'VDU ir daugiau'
end as Pajamu_reziai
from DUS2014N
union
select amzius, bdu_spalio, 2018 as Metai,
case
when bdu_spalio<400 then 'Iki MMA'
when bdu_spalio between 400 and (select avg(bdu_spalio) from DUS2018N) then 'Tarp MMA ir VDU'
when bdu_spalio>(select avg(bdu_spalio) from DUS2018N) then 'VDU ir daugiau'
end as Pajamu_reziai
from DUS2018N;

-- MMA 2014 metais - 1000 Lt. MMA 2018 metais - 400 €.
-- Suskaičiuokite, kiek kiekvienoje grupėje buvo respondentų, tiek 2014, tiek 2018 metais.

select count(*) as Respondentai, 2014 as Metai,
case
when bdu_spalio<1000 then 'Iki MMA'
when bdu_spalio between 1000 and (select avg(bdu_spalio) from DUS2014N) then 'Tarp MMA ir VDU'
when bdu_spalio>(select avg(bdu_spalio) from DUS2014N) then 'VDU ir daugiau'
end as Pajamu_reziai
from DUS2014N
group by Metai, Pajamu_reziai
union
select count(*) as Respondentai, 2018 as Metai,
case
when bdu_spalio<400 then 'Iki MMA'
when bdu_spalio between 400 and (select avg(bdu_spalio) from DUS2018N) then 'Tarp MMA ir VDU'
when bdu_spalio>(select avg(bdu_spalio) from DUS2018N) then 'VDU ir daugiau'
end as Pajamu_reziai
from DUS2018N
group by Metai, Pajamu_reziai;