-- DUS2014N ir DUS2018N,
-- suraskite 
-- kiek dalyvavo respondentų iš kiekvienos amžiaus grupės?alter
-- koks buvo vidutinis atlyginimas pagal amžiaus grupę?
-- (4 atskiros SQL užklausos)
-- Parodykite vienoje lentelėje ansktesnius duomenis ir pateikite
-- skirtumus tarp atlyginimų, dalyvių kiekių.

select *, C18-C14 as Δ, A18-A14 as `Δ€`
from
	(select case
	when amzius = '14-19' then '14-29'
	when amzius = '20-29' then '14-29'
	else amzius
	end as Amz,
	count(*) as C14, round(avg(bdu_spalio)/3.4528) as A14
	from DUS2014N
	group by Amz) as T14
join
	(select amzius as Amz, count(*) as C18, round(avg(bdu_spalio)) as A18
	from DUS2018N
	group by amzius) as T18
using (Amz);

-- Po pertraukos

-- Kiek respondenčių moterų uždirbo 2014 bei 2018 metais daugiau, nei vidutinį atlyginimą?

select * from
	(select * from
		(select 
		case
			when bdu_spalio >= (select avg(bdu_spalio) from DUS2014N) then 'Daugiau nei vid.'
			else 'Mažiau nei vid.'
		end as 'MD', 
		count(*) as KiekisMot2014
		from DUS2014N
		where lytis = 'F'
		group by `MD`) as T1
	join
		(select 
		case
			when bdu_spalio >= (select avg(bdu_spalio) from DUS2014N) then 'Daugiau nei vid.'
			else 'Mažiau nei vid.'
		end as 'MD', 
		count(*) as KiekisVyr2014
		from DUS2014N
		where lytis = 'M'
		group by `MD`) as T2
	using (MD)) as T14
join
	(select * from
		(select 
		case
			when bdu_spalio >= (select avg(bdu_spalio) from DUS2018N) then 'Daugiau nei vid.'
			else 'Mažiau nei vid.'
		end as 'MD', 
		count(*) as KiekisMot2018
		from DUS2018N
		where lytis = 'F'
		group by `MD`) as T1
	join
		(select 
		case
			when bdu_spalio >= (select avg(bdu_spalio) from DUS2018N) then 'Daugiau nei vid.'
			else 'Mažiau nei vid.'
		end as 'MD', 
		count(*) as KiekisVyr2018
		from DUS2018N
		where lytis = 'M'
		group by `MD`) as T2
	using (MD)) as T18
using (MD);

-- Pagalbiniai SQL
select avg(bdu_metinis) from DUS2014N;
select lytis from DUS2014N;
select avg(bdu_metinis) from DUS2014N where lytis LIKE 'F';
select count(*), lytis from DUS2014N group by lytis;
select * from 
	(select lytis, count(*) as kiekis from DUS2014N
		where bdu_metinis>(select avg(bdu_metinis) as vidutinis from DUS2014N)
	)group by lytis;
	
-- Kiek tai buvo daugiau/mažiau, lyginant su vyrų kiekiais, uždirbusiais daugiau, nei vidutinį atlyginimą, atitinkamais metais? (procentais, jei pavyksta)


-- Surūšiuokite respondentus pagal mėnesio pajamų rėžius - 'Iki MMA', 'Tarp MMA ir VDU', 'VDU ir daugiau'.
-- MMA 2014 metais - 1000 Lt. MMA 2018 metais - 400 €.
-- Suskaičiuokite, kiek kiekvienoje grupėje buvo respondentų, tiek 2014, tiek 2018 metais.
-- Naudoti: case, group by, union

	select
		case
			when bdu_spalio<1000 then 'Iki MMA'
			when bdu_spalio<(select avg(bdu_spalio) from DUS2014N) then 'MMA..VDU'
			else 'VDU ir daugiau'
		end as rėžis, 
		count(*) as kiekis 
		from DUS2014N
		group by rėžis;

	select
		case
			when bdu_spalio<400 then 'Iki MMA'
			when bdu_spalio<(select avg(bdu_spalio) from DUS2018N) then 'MMA..VDU'
			else 'VDU ir daugiau'
		end as rėžis, 
		count(*) as kiekis from DUS2018N
	group by rėžis;

select * from
	(select
		case
			when bdu_spalio<1000 then 'Iki MMA'
			when bdu_spalio<(select avg(bdu_spalio) from DUS2014N) then 'MMA..VDU'
			else 'VDU ir daugiau'
		end as rėžis, 
		count(*) as kiekis from DUS2014N
	group by rėžis)
join
	(select
		case
			when bdu_spalio<400 then 'Iki MMA'
			when bdu_spalio<(select avg(bdu_spalio) from DUS2018N) then 'MMA..VDU'
			else 'VDU ir daugiau'
		end as rėžis, 
		count(*) as kiekis from DUS2018N
	group by rėžis)
using(rėžis);

-------------
select
		case
			when bdu_spalio<1000 then 'Iki MMA'
			when bdu_spalio<(select avg(bdu_spalio) from DUS2014N) then 'MMA..VDU'
			else 'VDU ir daugiau'
		end as rėžis, 
		count(*) as kiekis from DUS2014N
	group by rėžis;
	