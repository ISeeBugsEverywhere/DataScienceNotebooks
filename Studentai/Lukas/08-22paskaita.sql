select *from BrentOilPrices limit 10;


select *, str_to_date(Date, "%d-%b-%y") as DATA
from BrentOilPrices
where str_to_date(Date, "%d-%b-%y") between cast('2001-01-01' as date) and cast('2001-02-01' as date);

(select str_to_date(Date, "%d-%M-%Y") from BrentOilPrices)  between cast('2001-01-01' as date) and cast('2001-02-01' as date)
-- where (select str_to_date(Date, "%d-%M-%Y") from BrentOilPrices)  between cast('2001-01-01' as date) and cast('2001-02-01' as date)
;

SELECT STR_TO_DATE('Wednesday, 10 February 2021, 12:30:20', '%W,
↪ %d %M %Y, %T');

select month(dataLaikas) as menuo, count(*) as kiekis
from EismIvyk2021
group by menuo;

select ivykioVieta, count(*) as kiekis, group_concat(schema1) as ivykiai
from EismIvyk2021
group by ivykioVieta
order by kiekis desc
limit 5;

select *, C/(select count(*) from EismIvyk2021)*100 as '%' from
(select * from
(select ivykioVieta as vieta, count(*) as C
from EismIvyk2021
group by ivykioVieta
order by C desc
limit 5) as T1
union all
select 'Others', count(*) as C
from EismIvyk2021
where ivykioVieta not in
(select vieta from (select ivykioVieta as vieta, count(*) as C
from EismIvyk2021
group by ivykioVieta
order by C desc
limit 5) as T2)) as T3;

select * from nypd limit 10;

select BORO as rajonas, count(*) as kiekis
from nypd
group by rajonas
order by kiekis desc;

select hour(OCCUR_TIME) as laikas, count(*) as kiekis
from nypd
where STATISTICAL_MURDER_FLAG=1
group by laikas;

select VIC_RACE, count(*) as vicC
from nypd
where PERP_RACE='BLACK'
group by VIC_RACE
order by vicC desc;

select VIC_AGE_GROUP, count(*) as C
from nypd
where PERP_RACE='BLACK' and VIC_RACE='BLACK'
group by VIC_AGE_GROUP
order by C desc;
