-- Kiek respondentų dalyvavo apklausoje 2014 bei 2018 metais iš kiekvienos amžiaus grupės?
select AG, D1.Dalyviai as D14, D2.Dalyviai as D18, 'F' as lyt  from
(SELECT count(*) as Dalyviai, 
case
when amzius = '14-19' then '14-29'
when amzius = '20-29' then '14-29'
else amzius
end as AG, lytis
FROM DUS2014N
where lytis ='f'
group by AG
) as D1
join
(SELECT count(*) as Dalyviai, amzius as AG FROM DUS2018N
where lytis = 'f'
group by AG) as D2
using (AG)
union all
select AG, D1.Dalyviai as D14, D2.Dalyviai as D18, 'M' as lyt  from
(SELECT count(*) as Dalyviai, 
case
when amzius = '14-19' then '14-29'
when amzius = '20-29' then '14-29'
else amzius
end as AG, lytis
FROM DUS2014N
where lytis ='m'
group by AG
) as D1
join
(SELECT count(*) as Dalyviai, amzius as AG FROM DUS2018N
where lytis = 'm'
group by AG) as D2
using (AG);

-- 2018 metams, parodykite vaizdžiai vidutinio atlyginimo priklausomybę nuo amžiaus grupės, atskirai vyrams, atskirai moterims.



select AG, A1.`Vidutinis atlyginimas` as M18, A2.`Vidutinis atlyginimas` as F18 from
(SELECT round(avg(bdu_spalio),0) as `Vidutinis atlyginimas`, amzius as AG FROM DUS2018N
where lytis = 'm'
group by amzius) as A1
join
(SELECT round(avg(bdu_spalio),0) as `Vidutinis atlyginimas`, amzius as AG FROM DUS2018N
where lytis = 'f'
group by amzius) as A2
using (AG);

-- Raskite 5-kis populiariausius autopliuslt skelbimuose  
-- esančius gamintojus, suraskite, kokia buvo kiekvienam  
-- iš šių gamintojų automobilių vidutinė kaina, rida,  
-- automobilių amžius. (viena kompleksinė SQL užklausa)
-- vizualizuokite šią informaciją stulpeline ar kitokia diagrama
select *, round(avg(2024-substring(pagaminimo_data,1,4)),0) from autopliuslt;
select gamintojas, count(*) as kiek, round(avg(cast(replace(price,' ','') as float)),0) as avgp,
 round(avg(cast(replace(replace(rida,' ',''),'km','')as float)),0) as rid, 
 round(avg(2024-substring(pagaminimo_data,1,4)),2) as amzius from autopliuslt
 where rida <> 'nenurodyta'
group by gamintojas
order by kiek desc
limit 5;

-- Sugrupuokite automobilius pagal jų amžių, ir suraskite
-- vidutinę kainą kiekvienam amžiui.
-- Ar didėjant automobilių amžiui, jų kaina yra linkusi mažėti?
-- Pateikite vizualizaciją, atsakančią į pateiktą klausimą.

select round(avg(cast(replace(price,' ','') as float)),0) as avgp,
 round(2024-substring(pagaminimo_data,1,4),0) as amzius from autopliuslt
group by amzius
order by amzius asc
;

-- Sugrupuokite automobilius pagal ridą, intervalais kas 5000 km, ir suraskite vidutinę kainą
-- kiekviename intervale. Apvalinimas turi būti į
-- didesnę pusę: 500 km turi tapti 5000 km.
-- Ar didėjant ridai, automobilių kaina yra linkusi mažėti?
-- Pateikite vizualizaciją, atsakančią į pateiktą klausimą.

select ceil(cast(replace(replace(rida,' ',''),'km','')as float)/5000)*5000 as ridas, round(avg(cast(replace(price,' ','') as float)),0) as avgp  from autopliuslt
where rida <> 'Nenurodyta'
group by ridas
order by ridas asc;
