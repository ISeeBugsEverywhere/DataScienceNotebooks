select * from profesijos limit 10;

-- Raskite 5 top 2014 metais apmokamas specialybes, atvaizduokite jų vidutinį atlyginimą stulpeline diagrama (bar arba barh).
-- Raskite 5 mažiausiai apmokamas specialybes 2014 metais, atvaizduokite jų vidutinį atlyginimą su bar arba barh.
-- Raskite 5 vidutiniškai apmokamas specialybes (0.9-1.1 VDU, imate arčiausiai 1.1 VDU esančias), atvaizduojate vidutinius atlyginimas su bar arba barh.
-- Tada surandate šių 15-kos specialybių atlyginimų pokytį tarp 2014 ir 2018 metų, pokytį vizualizuokite su bar arba barh. Kokios specialybėsm tas pokytis didžiausias?
-- Vietoj kodų - profesijų normalus pavadinimas!

-- top 5 max 2014
with
	T1 as (select round(avg(bdu_spalio/3.4528)) as alga, profesija as kod from DUS2014N
    group by kod),
    T2 as (select Kodas as kod, Profesija as prof from profesijos)
select * from T1 join T2 using (kod)
order by alga desc
limit 5;

-- top 5 min 2014
with
	T1 as (select round(avg(bdu_spalio/3.4528)) as alga, profesija as kod from DUS2014N
    group by kod),
    T2 as (select Kodas as kod, Profesija as prof from profesijos)
select * from T1 join T2 using (kod)
order by alga asc
limit 5;	

-- top 5 vid 2014
with
	T1 as (select round(avg(bdu_spalio/3.4528)) as alga, profesija as kod from DUS2014N
    group by kod
    having alga between (select avg(bdu_spalio/3.4528) *0.98 from DUS2014N) and (select avg(bdu_spalio/3.4528) *1.01 from DUS2014N)),
    T2 as (select Kodas as kod, Profesija as prof from profesijos)
select * from T1 join T2 using (kod)
order by alga desc;


select round(avg(bdu_spalio/3.4528)) as alga, profesija as kod
from DUS2014N
group by kod
having alga between (select avg(bdu_spalio/3.4528) *0.9 from DUS2014N) and (select avg(bdu_spalio/3.4528) *1.1 from DUS2014N);



-- 2014
with
T1 as((select round(avg(bdu_spalio/3.4528)) as alga14, profesija as kod from DUS2014N
group by kod
order by alga14 desc
limit 5)
union all
(select round(avg(bdu_spalio/3.4528)) as alga14, profesija as kod from DUS2014N
group by kod
having alga14 between (select avg(bdu_spalio/3.4528) *0.992 from DUS2014N) and (select avg(bdu_spalio/3.4528) *1.008 from DUS2014N)
order by alga14 desc
limit 5)
union all
(select round(avg(bdu_spalio/3.4528)) as alga14, profesija as kod from DUS2014N
group by kod
order by alga14 asc
limit 5)), 
T2 as (select Kodas as kod, Profesija as prof from profesijos)
select * from T1 join T2 using (kod);


-- 2018
with
T1 as((select round(avg(bdu_spalio)) as alga18, profesija as kod from DUS2018N
group by kod
order by alga18 desc
limit 5)
union all
(select round(avg(bdu_spalio)) as alga18, profesija as kod from DUS2018N
group by kod
having alga18 between (select avg(bdu_spalio) *0.992 from DUS2018N) and (select avg(bdu_spalio) *1.008 from DUS2018N)
order by alga18 desc
limit 5)
union all
(select round(avg(bdu_spalio)) as alga18, profesija as kod from DUS2018N
group by kod
order by alga18 asc
limit 5)), 
T2 as (select Kodas as kod, Profesija as prof from profesijos)
select * from T1 join T2 using (kod)
order by alga18 desc;

-- sujungiam 

with 
	T14 as
    (with
T1 as((select round(avg(bdu_spalio/3.4528)) as alga14, profesija as kod from DUS2014N
group by kod
order by alga14 desc
limit 5)
union all
(select round(avg(bdu_spalio/3.4528)) as alga14, profesija as kod from DUS2014N
group by kod
having alga14 between (select avg(bdu_spalio/3.4528) *0.992 from DUS2014N) and (select avg(bdu_spalio/3.4528) *1.008 from DUS2014N)
order by alga14 desc
limit 5)
union all
(select round(avg(bdu_spalio/3.4528)) as alga14, profesija as kod from DUS2014N
group by kod
order by alga14 asc
limit 5)), 
T2 as (select Kodas as kod, Profesija as prof from profesijos)
select * from T1 join T2 using (kod)),
	T18 as
    (select round(avg(bdu_spalio)) as alga18, profesija as kod from DUS2018N
    group by kod)
select prof, round((alga18-alga14)/alga14*100.0) as pokytis from T14 join T18 using (kod)
order by pokytis desc;

select round(avg(bdu_spalio)), profesija as kod from DUS2018N
where profesija = 111;


-- Pateikite lentelę, kurioje būtų vidutinė kaina jūsų pasirinktam ploto intervalui
-- pavyzdžiui, suskirstote butų plotus 5 kv m intervalais, ir suraskite vidutinę kainą tam intervalui.
-- Ar kaina yra linkusi didėti, didėjant plotui?

select * from aruodas;

select plotas, round(avg(price), 2) as P
from
(select 
ceil(cast(Plotas as float) / 5) * 5
as plotas,
cast(replace(`€/S`, '€/m²', '') as float) as price
from aruodas)
as T
group by plotas;


select 
ceil(cast(Plotas as float) / 5) * 5
as plotas,
cast(replace(`€/S`, '€/m²', '') as float)
from aruodas;

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


select Kambariai, round(avg(price), 2) as P
from
(select 
Kambariai,
cast(replace(`€/S`, '€/m²', '') as float) as price
from aruodas)
as T
group by Kambariai;

select *, C/(select count(*) from EismIvyk2020)*100 as '%' from
(select * from
(select schema1 as ivykiai, count(*) as C
from EismIvyk2020
group by ivykiai
order by C desc
limit 5) as T1
union all
select 'Others', count(*) as C
from EismIvyk2020
where ivykiai not in
(select ivykiai from (select schema1 as ivykiai, count(*) as C
from EismIvyk2020
group by ivykiai
order by C desc
limit 5) as T2)) as T3;


with
T1 as
(select schema1 as ivykiai, count(*) as C20
from EismIvyk2020
group by ivykiai),
T2 as (select schema1 as ivykiai, count(*) as C21 from EismIvyk2021)
select * from T1 join T2 using (ivykiai)
order by ivykiai desc;


with 
T1 as
(select schema1 as ivykiai, count(*) as C20
from EismIvyk2020
group by ivykiai),
T2 as
(select schema1 as ivykiai, count(*) as C21
from EismIvyk2021
group by ivykiai)
select *, round((C21-C20)/C20*100, 2) as pokytis from T1 join T2 using (ivykiai)
order by pokytis desc;
