-- Raskite 5 top 2014 metais apmokamas specialybes, atvaizduokite jų vidutinį atlyginimą stulpeline diagrama (bar arba barh).
select round(f.atl,0) as a, s.Profesija from
(select profesija, avg(bdu_spalio) as atl from DUS2014N
group by profesija
order by atl desc
limit 5) as f
join
(select * from profesijos) as s
on f.profesija = s.Kodas
order by a desc;

-- Raskite 5 mažiausiai apmokamas specialybes 2014 metais, atvaizduokite jų vidutinį atlyginimą su bar arba barh.
select round(f.atl,0) as a, s.Profesija from
(select profesija, avg(bdu_spalio) as atl from DUS2014N
group by profesija
order by atl asc
limit 5) as f
join
(select * from profesijos) as s
on f.profesija = s.Kodas
order by a asc;
-- Raskite 5 vidutiniškai apmokamas specialybes (0.9-1.1 VDU, imate arčiausiai 1.1 VDU esančias), atvaizduojate vidutinius atlyginimas su bar arba barh.
select round(f.atl,0) as a, s.Profesija from
(select * from
(select profesija, avg(bdu_spalio) as atl,
case
when avg(bdu_spalio)>(select avg(bdu_spalio)*0.9 from DUS2014N) and avg(bdu_spalio)<=(select avg(bdu_spalio)*1.1 from DUS2014N) then 'Vid_apmok'
else 'ne'
end as vdu
from DUS2014N
group by profesija) as t
where vdu = 'Vid_apmok'
order by atl desc
limit 5) as f
join
(select * from profesijos) as s
on f.profesija = s.Kodas
order by a desc;
-- Tada surandate šių 15-kos specialybių atlyginimų pokytį tarp 2014 ir 2018 metų, pokytį vizualizuokite su bar arba barh. Kokios specialybėsm tas pokytis didžiausias?
select t.a/3.4528 as d14, t.p, u.a as d18, (u.a-(t.a/3.4528))/(t.a/3.4528)*100 as pok from
(select f.atl as a, s.Profesija as p, s.Kodas as c from
(select profesija, avg(bdu_spalio) as atl from DUS2014N
group by profesija
order by atl desc
limit 5) as f
join
(select * from profesijos) as s
on f.profesija = s.Kodas
union all
select round(f.atl,0) as a, s.Profesija, s.Kodas from
(select profesija, avg(bdu_spalio) as atl from DUS2014N
group by profesija
order by atl asc
limit 5) as f
join
(select * from profesijos) as s
on f.profesija = s.Kodas
union all
select round(f.atl,0) as a, s.Profesija, s.Kodas from
(select * from
(select profesija, avg(bdu_spalio) as atl,
case
when avg(bdu_spalio)>(select avg(bdu_spalio)*0.9 from DUS2014N) and avg(bdu_spalio)<=(select avg(bdu_spalio)*1.1 from DUS2014N) then 'Vid_apmok'
else 'ne'
end as vdu
from DUS2014N
group by profesija) as t
where vdu = 'Vid_apmok'
order by atl desc
limit 5) as f
join
(select * from profesijos) as s
on f.profesija = s.Kodas
order by a desc) as t
left join
(select profesija as c, round(avg(bdu_spalio),0) as a from DUS2018N
group by profesija) as u
using (c)
order by pok desc;

-- Pateikite lentelę, kurioje būtų vidutinė kaina jūsų pasirinktam ploto intervalui
-- pavyzdžiui, suskirstote butų plotus 5 kv m intervalais, ir suraskite vidutinę kainą tam intervalui.
-- Ar kaina yra linkusi didėti, didėjant plotui?
select round(avg(vid),0) as prc, grup from
(select *, substring(`€/S`,1,4) as vid, ceil(Plotas/5)*5 as grup
from aruodas) as f
group by grup;

-- Ar vidutinė kaina priklauso nuo kambarių skaičiaus?
select round(avg(vid),0) as prc, grup from
(select *, substring(`€/S`,1,4) as vid, kambariai as grup
from aruodas) as f
group by grup;

-- kokie eismo įvykiai sudarė top5? Pateikite procentinę vizualizaciją (pie chart). Lentelė EismIvyk2020, stulpelis schema1. 
select count(*) as proc, rusis from EismIvyk2020
group by rusis
order by proc desc limit 5;
-- pateikite šių eismo įvykių pokytį tarp 2020 ir 2021 metų, procentais, barh grafiku.

select schema1, (s.proc-f.proc)/f.proc*100 as skir from 
(select count(*) as proc, schema1 from EismIvyk2020
group by schema1
order by proc desc) as f
left join
(select count(*) as proc, schema1 from EismIvyk2021
group by schema1) as s
using(schema1)
order by skir desc;