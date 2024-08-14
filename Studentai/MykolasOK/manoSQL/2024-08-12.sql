-- with

--------

-- Numeracija

select *,
	row_number() over (partition by name) as rn 
	from gov_forms gf ;

select * from (
	select *,
		row_number() over (partition by name) as rn 
		from gov_forms gf ) as T
where rn=1;

select gamintojas, modelis, price
	from autopliuslt;

with T1 as
(select gamintojas, modelis, price, 
	ROW_NUMBER() over 
	(partition by gamintojas, modelis 
	order by cast(replace(price, ' ', '') as float) desc
	) as rn 
	from autopliuslt a );
select * from T1;

-- Kiek skirtingų profesijų/profesijų grupių  buvo apklausta 2014 ir 2018 metais? 
-- Pateikite skirtumą tarp jų kiekio 2014 ir 2018 metais,
-- jei toks yra.
-- Profesijos turi turėti pavadinimus, ne kodais.

select count(*), p.Kodas, p.Profesija 
from DUS2014N du14
left join profesijos p
on du14.profesija=p.Kodas
group by p.Kodas;

select count(*), p.Kodas, p.Profesija 
from DUS2018N du18
left join profesijos p
on du18.profesija=p.Kodas
group by p.Kodas;

----

select  from (
	select count(*) as c
	from DUS2014N du14
	left join profesijos p
	on du14.profesija=p.Kodas
	group by p.Kodas )
join (
	select count(*) as c
	from DUS2018N du18
	left join profesijos p
	on du18.profesija=p.Kodas
	group by p.Kodas )
using(pk)
grop by pk;
