select
lytis, group_concat(bdu_spalio) as GC
from DUS2014N
group by lytis;

-- parodykite su boxplot atlyginimų pasiskirstymus nuo amžiaus grupės 2018 metams (vyrams ir moterims atskirai).
select amzius, group_concat(bdu_spalio) from DUS2018N
where lytis = 'F'
group by amzius;

select amzius, group_concat(bdu_spalio) from DUS2018N
where lytis = 'M'
group by amzius;


-- Taip pat parodykite su boxplot'ais atlyginimų pasiskirstymus nuo išsilavinimo, 2018 metams (visiems respondentams)
select issilavinimas, group_concat(bdu_spalio) from DUS2018N
group by issilavinimas;

-- Pateikite su boxplot'u  skelbimų kainų pasiskirtymą top 5 automobilių gamintojams.
select gamintojas, group_concat(cast(replace(price,' ','') as float)) as kaina from autopliuslt
group by gamintojas
order by count(*) desc
limit 5;

-- vidutinė kaina
select  round(avg(cast(replace(price,' ','') as float)),0) as kaina from autopliuslt;

-- pateikite su bar arba barh vidutines automobilių kainas
-- top 5 gamintojams, dviem variantais:
-- a) laikote, kad visi skelbimai yra unikalūs
select gamintojas, round(avg(cast(replace(price,' ','') as float)),0) as kaina from autopliuslt
group by gamintojas
order by count(*) desc
limit 5;
-- b) eliminuojate pasikartojančius skelbimus (jei skelbimo id kartojasi DB įrašuose
-- tai skelbimas nėra unikalus, jis dubliuojasi)
select * from
(select gamintojas, round(avg(cast(replace(price,' ','') as float)),0) as kaina from autopliuslt
group by gamintojas
order by count(*) desc
limit 5) as f
join
(select gamintojas, round(avg(kaina),0) as kaina from
(select distinct id, gamintojas, cast(replace(price,' ','') as float) as kaina  from autopliuslt) as s
group by gamintojas
order by count(*) desc
limit 5) as s
using (gamintojas);

-- atvaizduokite boxplotais kainos pasiskirstymą nuo ridos (15 000 km intervalais apvalintos)
select ceil(cast(replace(replace(rida,' ',''),'km','')as float)/15000)*15000 as ridas, group_concat(cast(replace(price,' ','') as float)) as kaina from autopliuslt
where rida <> 'Nenurodyta'
group by ridas  
;
-- # atvaziduokite boxplotu ridos pasiskirstymą nuo kuro rūšies/tipo
select kuro_tipas, group_concat(cast(replace(replace(rida,' ',''),'km','')as float)) as rida  from autopliuslt
group by kuro_tipas
order by count(*) desc;

-- # atvaizduokite boxplotais ridos pasiskirstymo priklausomybę nuo gamintojo 
select gamintojas, group_concat(cast(replace(replace(rida,' ',''),'km','')as float)) as rida  from autopliuslt
group by gamintojas
order by count(*) desc;


-- # suraskite visus gamintojus, kurių  modelių vidutinė kaina yra didesnė už vidutinę
-- # visų automobilių
-- # kainą.
-- # Iš jų atrinkite 5-kis brangiausius gamintojus, ir suraskite jų 
-- # parduodamų modelių vidutinį amžių.
(select round(avg(cast(replace(price,' ','') as float)),0) as vprc from autopliuslt;

select gamintojas, amzius from
(select gamintojas, round(avg(cast(replace(price,' ','') as float)),0) as gprc,
if(round(avg(cast(replace(price,' ','') as float)),0)>(select round(avg(cast(replace(price,' ','') as float)),0) as vprc from autopliuslt),'Did','Maz') as grup,
round(avg(2024-substring(pagaminimo_data,1,4)),6) as amzius, group_concat(cast(replace(price,' ','') as float)) as kaina
from autopliuslt
group by gamintojas
having grup = 'Did'
order by gprc desc
limit 5) as f;

-- # taip pat atvaizduokite su boxplot'ais šių 5-kių gamintojų parduodamų modelių kainų pasiskirstymą.
select gamintojas, kaina from
(select gamintojas, round(avg(cast(replace(price,' ','') as float)),0) as gprc,
if(round(avg(cast(replace(price,' ','') as float)),0)>(select round(avg(cast(replace(price,' ','') as float)),0) as vprc from autopliuslt),'Did','Maz') as grup,
round(avg(2024-substring(pagaminimo_data,1,4)),6) as amzius, group_concat(cast(replace(price,' ','') as float)) as kaina
from autopliuslt
group by gamintojas
having grup = 'Did'
order by gprc desc
limit 5) as f;