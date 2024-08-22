select
lytis, group_concat(bdu_spalio) as gc
from DUS2014N
group by lytis;


select amzius, group_concat(bdu_spalio)
from DUS2018N
where lytis = 'M'
group by amzius;

select amzius, group_concat(bdu_spalio)
from DUS2018N
where lytis = 'F'
group by amzius;

select issilavinimas, group_concat(bdu_spalio)
from DUS2018N
where lytis = 'M'
group by issilavinimas;

select gamintojas, count(*) as kiekis,
group_concat(cast(replace(price, ' ', '') as float)) as kaina
-- group_concat(cast(replace(rida, ' ', '') as float)) as rid
-- 2024-avg(cast(substring(pagaminimo_data, 1, 4) as float)) as amzius
-- cast(substring(pagaminimo_data, 1, 4) as float) as pagaminta
from autopliuslt
 -- where rida != 'Nenurodyta' and cast(substring(pagaminimo_data, 1, 4) as float) = 2020
group by gamintojas
order by kiekis desc
limit 5;  

select 
-- gamintojas,
--  count(*) as kiekis,
 
avg(cast(replace(price, ' ', '') as float)) as kaina
from autopliuslt
where gamintojas in ('BMW', 'Volkswagen', 'Audi', 'Mercedes-Benz', 'Toyota');
-- group by gamintojas
-- order by kiekis desc
-- limit 5;

with T1 as
(select gamintojas, 
cast(replace(price, ' ', '') as float) as kaina,
row_number() over (partition by id) as rn
from autopliuslt)
select gamintojas, count(*) as kiekis, round(avg(kaina))
from T1
where rn < 2
group by gamintojas
order by kiekis desc
limit 5; 

with T1 as
(select gamintojas, modelis, price,
row_number() over 
(partition by gamintojas, modelis order by cast(replace(price, ' ', '') as float) desc) as rn
from autopliuslt)
select * from T1
where rn < 4;


select Rida, group_concat(Kaina) as P
from
(select 
ceil(cast(replace(replace(rida, ' ', ''), 'km', '') as float) / 15000.0) * 15000.0
as Rida,
cast(replace(price, ' ', '') as float) as Kaina
from autopliuslt
where rida != 'Nenurodyta')
as T
group by Rida;

select count(*)as kiekis,
-- group_concat(cast(replace(price, ' ', '') as float)) as Kaina, 
ceil(cast(replace(replace(rida, ' ', ''), 'km', '') as float) / 15000.0) * 15000.0 as Rida
from autopliuslt
where rida != 'Nenurodyta'
group by Rida
order by  kiekis desc;

select Rida, group_concat(Kaina) as P
from
(select 
ceil(cast(replace(replace(rida, ' ', ''), 'km', '') as float) / 15000.0) * 15000.0
as Rida,
cast(replace(price, ' ', '') as float) as Kaina

from autopliuslt
where rida != 'Nenurodyta')
as T
group by Rida;

select kuro_tipas,
group_concat(cast(replace(replace(rida, ' ', ''), 'km', '') as float))  as Rida
from autopliuslt
group by kuro_tipas;

-- ridos pasiskirstymas nuo gamintojo
select gamintojas,
group_concat(cast(replace(replace(rida, ' ', ''), 'km', '') as float))  as Rida
from autopliuslt
group by gamintojas;


-- visu vidutine kaina
select
avg(cast(replace(price, ' ', '') as float)) as Kaina
from autopliuslt;

select gamintojas, modelis, avg(cast(replace(price, ' ', '') as float)) as Kaina,
2024-avg(cast(substring(pagaminimo_data, 1, 4) as float)) as amzius,
count(*) as kiekis
from autopliuslt
where cast(replace(price, ' ', '') as float) > (select
avg(cast(replace(price, ' ', '') as float)) as Kaina
from autopliuslt)
group by gamintojas, modelis
order by Kaina desc
limit 5;
