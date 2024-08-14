with T1 as 
(select actor_id, first_name from sakila.actor)
select * from T1;

with
	T1 as (select * from `life-expectancy` where year=2019),
    T2 as (select  from gov_forms)
select * from T1 inner join T2
on T1.Entity = T2.Name;



select *, row_number() over (order by `Constitutional form`) as rn 
from gov_forms;

select * , row_number() over (order by `Life expectancy`)as rn
from `life-expectancy`
order by Entity asc;

with
	T1 as 
			(select * ,row_number() over (order by `Life expectancy` desc)
            as rn
            from `life-expectancy`
            where year = 2019)
select * from T1 
where Code = 'LTU';


-- pvz kaip eleminuoti pasikartojancius irasus
select * from
(select * ,
row_number() over (partition by Name) as rn
from gov_forms) as T
where rn = 1;

with T1 as
(select gamintojas, modelis, price,
row_number() over (partition by gamintojas, modelis order by cast(replace(price, ' ', '') as float) desc) as rn
 from autopliuslt)
 select * from T1
 where rn < 4;
 
 
 -- Kiek skirtingų profesijų/profesijų grupių  buvo apklausta 2014 ir 2018 metais? 
-- Pateikite skirtumą tarp jų kiekio 2014 ir 2018 metais,
--  jei toks yra.
-- Profesijos turi turėti pavadinimus, ne kodais.

select profesija, count(*) from DUS2014N
group by profesija;


with
	T1 as
    (select profesija, count(*) as kiekis2014,
    row_number() over (order by profesija desc) as rn14
    from DUS2014N
    group by profesija),
    T2 as
    (select profesija, count(*)as kiekis2018,
    row_number() over (order by profesija desc) as rn18
    from DUS2018N
    group by profesija)
select rn14, rn18, rn18-rn14 as skirtumas from T1
left join T2
on T1.profesija = T2.profesija
limit 1;

-- pvz  uzduotis virsuje
select *, C18-C14 as Δ  from
(select count(*) as C14 from
(select count(*), profesija from DUS2014N group by profesija) as T1) as T2
join
(select count(*) as C18 from
(select count(*), profesija from DUS2018N group by profesija) as T1) as T3;



-- distinct atrenka unikalius irasus
select count(distinct lytis) from DUS2014N;

select *, C18-C14 as Δ
from
(select count(distinct profesija) as C14 from DUS2014N) as T1
join
(select count(distinct profesija) as C18 from DUS2018N) as T2;
    
    

-- Suraskite 5-kis top telefonų gamintojus. Kiek vienetų kiekvieno gamintojo telefonų 
-- turėjo klientai?
-- jei gamintojas (brand) nenurodytas - atmeskite.
select * from sa limit 2;


select count(NULLIF(device_brand, '')) as kiekis,  device_brand
from sa
group by device_brand
order by kiekis desc
limit 5;


-- Kiek rinkos dalies užėmė šie 5-ki gamintojai? Pateikite tai procentais.
-- Jei gamintojas nenurodytas, priskirkite tą įrašą prie 'Other brands'.

select *, kiekis / sum(kiekis) *100 as dalis from
-- select * from
(select count(*) as kiekis,
case 
when device_brand = '' then 'Other brands'
else device_brand
end as brand
from sa
group by brand
order by kiekis desc) as t1
limit 6;


-- pvz
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


-- rinkos dalis

select count(*) as Kiekis, count(*)/(select count(*) from sa)*100 as `Rinkos dalis`,
case 
when device_brand in (select * from(select brand from
(select count(*) as kiekis, device_brand as brand  from sa where device_brand<>'' group by device_brand) as D
order by kiekis desc limit 5)as f) then device_brand
else 'Other'
end as Brand from sa
group by Brand
order by kiekis desc;




select profesija, bdu_metinis
from DUS2014N
group by profesija
order by bdu_metinis desc
limit 5;


select profesija, bdu_metinis
from DUS2014N
group by profesija
order by bdu_metinis asc
limit 5;

select profesija, bdu_metinis
from DUS2018N
group by profesija
order by bdu_metinis asc
limit 5;

select profesija, bdu_metinis
from DUS2014N
where bdu_metinis between (select avg(bdu_metinis)*0.9 from DUS2014N) and (select avg(bdu_metinis)*1.1 from DUS2014N)
order by bdu_metinis desc;

select profesija, bdu_metinis
from DUS2014N
where bdu_metinis between (select avg(bdu_metinis)*0.99985 from DUS2014N) and (select avg(bdu_metinis)*1.00015 from DUS2014N)
order by bdu_metinis desc;

select avg(bdu_metinis) from DUS2014N;
-- 26026.65


select profesija, bdu_metinis
from DUS2018N
where bdu_metinis between (select avg(bdu_metinis)*0.9999 from DUS2018N) and (select avg(bdu_metinis)*1.0001 from DUS2018N)
order by bdu_metinis desc;

select avg(bdu_metinis) from DUS2018N;
-- 9782.74

