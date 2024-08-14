with T1 as
(select actor_id, first_name from sakila.actor)
select * from T1;

with 
	T1 as (select * from `life-expectancy` where Year = 2019),
    T2 as (select substring(Name, 2 , length(Name)) as Country, `Constitutional form` from gov_forms)
select * from T1 inner join T2
on T1.Entity = T2.Country
where Code = 'LTU';

select * from TOP_Profesija_2014_JT;

select *, row_number() over (order by `Constitutional form`) as rn
	from gov_forms;
    
select *, row_number() over (order by `Life expectancy` desc) as rn
from `life-expectancy`
order by Entity asc;

with 
	t1 as
		(select *, row_number() over (order by `Life expectancy` desc)
        as rn
        from `life-expectancy`
        where Year = 2019)
select * from t1
where Code = 'LTU';

select * from
(select *, 
row_number() over (partition by Name) as rn
from gov_forms) as T
where rn = 1;

-- 3 brangiausi auto pagal modelius
with T1 as
(select gamintojas, modelis, price,
row_number() over (partition by gamintojas, modelis order by cast(replace(price,' ', '') as float) desc) as rn
from autopliuslt)
select * from T1
where rn < 4;

-- Kiek skirtingų profesijų/profesijų grupių  buvo apklausta 2014 ir 2018 metais?
-- Pateikite skirtumą tarp jų kiekio 2014 ir 2018 metais,
--  jei toks yra.
select D2014, D2018, D2018-D2014 as skirtumas from
(select count(*) as D2014, nr from 
(select *, row_number() over (partition by profesija order by profesija asc) as nr from DUS2014N) as D1
where nr = 1) as T1
join
(select count(*) as D2018, nr from 
(select *, row_number() over (partition by profesija order by profesija asc) as nr from DUS2018N) as D2
where nr = 1) as T2 using(nr);

select *, C18-C14 as Δ
from
(select count(distinct profesija) as C14 from DUS2014N) as T1
join
(select count(distinct profesija) as C18 from DUS2018N) as T2;

-- Suraskite 5-kis top telefonų gamintojus. Kiek vienetų kiekvieno gamintojo telefonų 
-- turėjo klientai?
-- jei gamintojas (brand) nenurodytas - atmeskite.
-- sa lentele
select *from
(select count(*) as kiekis, device_brand as brand  from sa where device_brand<>'' group by device_brand) as D
order by kiekis desc limit 5
;

-- rinkos dalis

select *, kiekis/(select count(*) from sa)*100 as `Rinkos dalis`  from
(select count(*) as kiekis, 
device_brand as brand
from sa where device_brand <> '' group by device_brand) as D
order by kiekis desc
;

select brand from
(select count(*) as kiekis, device_brand as brand  from sa where device_brand<>'' group by device_brand) as D
order by kiekis desc limit 5
;

select count(*) as Kiekis, count(*)/(select count(*) from sa)*100 as `Rinkos dalis`,
case 
-- when device_brand in (select brand from
-- (select count(*) as kiekis, device_brand as brand  from sa where device_brand<>'' group by device_brand) as D
-- order by kiekis desc limit 5) then device_brand
when device_brand = 'Samsung' then device_brand
when device_brand = 'Nokia' then device_brand
when device_brand = 'BlackBerry' then device_brand
when device_brand = 'LG' then device_brand
when device_brand = 'SonyEricsson' then device_brand
else 'Other'
end as Brand from sa
group by Brand
order by kiekis desc;