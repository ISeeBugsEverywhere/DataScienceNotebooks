SELECT 
    *
FROM
    `life-expectancy`
LIMIT 10;
select * from
(select *, row_number() over (order by `Life expectancy` desc)
from `life-expectancy` where year = 2019) as T
where Entity = 'Lithuania';

with ER as
(
	select *, 
	row_number() over (order by `Life expectancy` desc) as RC 
	from `life-expectancy` 
	where year = 2019
)
select *
from ER
where Entity = 'Lithuania';

with CTE as
(select *, row_number() over (partition by Entity order by Year desc) as RC from
`life-expectancy`)
select * from CTE
where RC = 1;

select *, 
row_number() over (partition by Entity order by Year desc) as RC 
from `life-expectancy` 
order by `Life expectancy`;

with T1 as
(select gamintojas, modelis, price,
row_number() over (partition by gamintojas, modelis order by cast(replace(price, ' ','') as float) desc) as rn
from autopliuslt)
select gamintojas, modelis, price
from T1
where rn <= 3;

select * from
(select *, row_number() over (partition by gamintojas order by kaina desc) as rn
from
(select gamintojas, modelis,
avg(cast(replace(price,' ','') as float)) as kaina
from autopliuslt
group by gamintojas, modelis) as T1)
as T2
where rn <= 3;

with D14f as
(select case
when amzius in ('14-19', '20-29') then '14-29'
else amzius
end as A, count(*)
from DUS2014N
where lytis = 'F'
group by A),
D14m as
(select case
when amzius in ('14-19', '20-29') then '14-29'
else amzius
end as A, count(*)
from DUS2014N
where lytis = 'M'
group by A)
select * from D14f join D14m using (A);

with D18f as
(select amzius, count(*)
from DUS2018N
where lytis = 'F'
group by amzius),
D18m as
(select amzius, count(*)
from DUS2018N
where lytis = 'M'
group by amzius)
select * from D18f join D18m using (amzius);

with A as 
(select amzius, avg(bdu_spalio)
from DUS2018N
where lytis = 'F'
group by amzius),
B as
(
select amzius, avg(bdu_spalio)
from DUS2018N
where lytis = 'M'
group by amzius
)
select * from A join B using (amzius);

-- • Raskite 5-kis populiariausius autopliuslt skelbimuose  
-- esančius gamintojus, suraskite, kokia buvo kiekvienam  
-- iš šių gamintojų automobilių vidutinė kaina, rida,  
-- automobilių amžius. (viena kompleksinė SQL užklausa)
-- vizualizuokite šią informaciją stulpeline ar kitokia diagrama

select gamintojas, count(*) as C,
round(avg(cast(replace(replace(rida, ' ', ''), 'km', '') as float))) as VRida,
round(avg(cast(replace(price, ' ', '') as float))) as VKaina,
round(avg(2024-cast(substring(pagaminimo_data, 1, 4) as float))) as VAmzius
from autopliuslt
where rida != 'Nenurodyta'
group by gamintojas
order by C desc
limit 5;

select Rida, round(avg(Kaina), 2) as P
from
(select 
ceil(cast(replace(replace(rida, ' ', ''), 'km', '') as float) / 5000.0) * 5000.0
as Rida,
cast(replace(price, ' ', '') as float) as Kaina
from autopliuslt
where rida != 'Nenurodyta')
as T
group by Rida;

select Am, round(avg(K),2) as P
from
(select 
2024-cast(substring(pagaminimo_data, 1, 4) as float) as Am,
cast(replace(price, ' ', '') as float) as K
from
autopliuslt) as T1
group by Am
order by Am asc;

-- ceil, floor, round 
select ceil(1/5000)*5000;




