-- Vakar dienos paskutinė užklausa:
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

---------------

-- Autoplius analizė.

-- Raskite 5-kis populiariausius autopliuslt skelbimuose esančius gamintojus, 
-- suraskite, kokia buvo kiekvienam iš šių gamintojų automobilių 
-- vidutinė kaina, rida, automobilių amžius. (viena kompleksinė SQL užklausa)

select 
	count(*) as kiek, 
	avg(cast(replace(price,' ','') as float)) as kaina,
	avg(cast(replace(replace(rida,'km',''),' ','') as float)) as rida,
	avg(cast(replace(replace(pagaminimo_data,'-',''),' ','')) as float) as kada,
	gamintojas from autopliuslt a 
where rida != 'Nenurodyta'
group by gamintojas
order by kiek desc
limit 5;
