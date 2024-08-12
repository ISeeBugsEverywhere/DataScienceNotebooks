with T1 as
(select actor_id, first_name from sakila.actor)
select * from T1;

with 
	T1 as (select * from `life-expectancy` where Year = 2019),
    T2 as (select substring(Name, 2, length(Name)) as Country,
    `Constitutional form` from gov_forms)
select * from T1 inner join T2
on T1.Entity = T2.Country
where Code = 'LTU';

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

with T1 as
(select gamintojas, modelis, price,
row_number() over 
(partition by gamintojas, modelis order by cast(replace(price, ' ', '') as float) desc) as rn
from autopliuslt)
select * from T1
where rn < 4;

select *, C18-C14 as Δ  from
(select count(*) as C14 from
(select count(*), profesija from DUS2014N group by profesija) as T1) as T2
join
(select count(*) as C18 from
(select count(*), profesija from DUS2018N group by profesija) as T1) as T3;


select count(*) from (select count(*), profesija from DUS2014N group by profesija) as T5;

select count(distinct lytis) from DUS2014N;




select *, C18-C14 as Δ
from
(select count(distinct profesija) as C14 from DUS2014N) as T1
join
(select count(distinct profesija) as C18 from DUS2018N) as T2;


select *, C/(select count(*) from sa)*100 as 'Rinkos dalis %' from
(select * from
(select device_brand as B, count(*) as C
from sa
where device_brand != ''
group by device_brand
order by C desc limit 5) as T1
union all
select 'Other brands', count(*) as C
from sa
where device_brand
not in (select B from
(select device_brand as B, count(*) as C
from sa
where device_brand != ''
group by device_brand
order by C desc limit 5) as T1)) as T2;





