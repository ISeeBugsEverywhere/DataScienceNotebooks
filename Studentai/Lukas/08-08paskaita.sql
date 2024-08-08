-- ar yra priklausomybė tarp šalių konstitucinės santvarkos ir vidutinės gyvenimo trukmės?

select avg(L.`Life expectancy`), G.`Constitutional form`
from gov_forms as G
join `life-expectancy`as L on substring(Name, 2, length(Name)) = L.Entity
where L.Year = 2018
group by G.`Constitutional form`;

-- suraskite tris valstybes, kurios yra su ilgiausia gyvenimo trukme, tris su mažiausia, ir palyginkite su Lietuva. (2018 metams)
(select `Life expectancy`as life, Entity
from `life-expectancy`as LE
where Year = 2019
order by life desc
limit 3)
union all
(select `Life expectancy`as life, Entity
from `life-expectancy`as LE
where Year = 2019 and Entity='Lithuania')
union all
(select `Life expectancy`as life, Entity
from `life-expectancy`as LE
where Year = 2019
order by life asc
limit 3);

-- DUS2014N ir DUS2018N,
-- suraskite 
-- kiek dalyvavo respondentų iš kiekvienos amžiaus grupės?alter
-- koks buvo vidutinis atlyginimas pagal amžiaus grupę?
-- (4 atskiros SQL užklausos)
-- amzius, bdu_spalio

select count(*), amzius as A14
from DUS2014N
group by amzius;

select count(*), avg(bdu_spalio),
case
when amzius in ('14-19', '20-29') then '14-29'
else amzius
end as naujasamzius
from DUS2014N
group by naujasamzius;



select count(*), amzius as A14,avg(bdu_spalio/3.4528)as spalis14
from DUS2014N
group by amzius;

select count(*), amzius as A18,avg(bdu_spalio) as spalis14
from DUS2018N
group by amzius;

select count(*), amzius as A18
from DUS2018N
group by amzius;

-- Parodykite vienoje lentelėje ansktesnius duomenis ir pateikite
-- skirtumus tarp atlyginimų, dalyvių kiekių.

select *, (A18-A14) as `Δ` from
(select amzius, avg(bdu_spalio)/3.4528 as A14
from DUS2014N
group by amzius) as T
inner join
(select amzius, avg(bdu_spalio) as A18
from DUS2018N
group by amzius) as D
using (amzius);

select *,round(A18-A14) as `Δ`, round(C18-C14)as delta from
(select count(*)as C14, avg(bdu_spalio/3.4528)as A14,
case
when amzius in ('14-19', '20-29') then '14-29'
else amzius
end as naujasamzius
from DUS2014N
group by naujasamzius) as T
inner join
(select count(*) as C18, amzius, avg(bdu_spalio) as A18
from DUS2018N
group by amzius) as D
on T.naujasamzius = D.amzius;

-- pvz
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


-- Kiek respondenčių moterų uždirbo 2014 bei 2018 metais daugiau, nei vidutinį atlyginimą?

-- Kiek tai buvo daugiau/mažiau, lyginant su vyrų kiekiais, uždirbusiais daugiau,
-- nei vidutinį atlyginimą, atitinkamais metais? (procentais, jei pavyksta)

select lytis, bdu_metinis
from DUS2014N 
where bdu_metinis > avg(bdu_metinis) and lytis = 'F'
limit 100;

-- having bdu_metinis > round(avg(bdu_metinis))

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



-- Surūšiuokite respondentus pagal mėnesio pajamų rėžius - 'Iki MMA', 'Tarp MMA ir VDU', 'VDU ir daugiau'.
-- MMA 2014 metais - 1000 Lt. MMA 2018 metais - 400 €.
-- Suskaičiuokite, kiek kiekvienoje grupėje buvo respondentų, tiek 2014, tiek 2018 metais.
-- naudoti case ir grupavima

select count(*),
case 
when bdu_spalio < 1000 then 'iki MMA'
when bdu_spalio between 1000 and (select avg(bdu_spalio) from DUS2014N) then 'Tarp MMA ir VDU'
else 'VDU ir daugiau'
end as atlygis
from DUS2014N
group by atlygis;


