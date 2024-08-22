-- 1) su plot() nubraižykite BrentOilPrices istorinius duomenis. Duomenis imkite iš SQL lentelės BrentOilPrices.
select * from BrentOilPrices;

-- 2) Pridėkite vartotojo įvestį, kad su input() būtų galima nurodyti metus (nuo, iki), kurių istorinius duomenis norite pamatyti.
select * from BrentOilPrices
where str_to_date(Date,'%d-%M-%y') between '2001-01-01' and '2002-01-01';

-- # EismoĮvykiai - kurį mėnesį įvyko daugiausiai eismo įvykių? Pateikite eismo įvykių kiekius su bar arba barh.
select count(*), substring(dataLaikas,6,2) as men from EismIvyk2021
group by men;
-- destytojo
select count(*), month(cast(dataLaikas as datetime)) as M from EismIvyk2021
group by M;
-- # kuriomis valandomis? Taip pat vizuallizuokite tai su bar arba barh. Stulpelis dataLaikas.
select *,count(*), substring(dataLaikas,12,2) as men from EismIvyk2021
group by men;
-- destytojo
select count(*), hour(cast(dataLaikas as datetime)) as H from EismIvyk2021
group by H;
-- # kokie top 5 adrresai, kuriuose yra daugiausiai eimso įvykių?
select ivykioVieta, count(*) as r from EismIvyk2021
group by ivykioVieta
order by r desc limit 5 ;

select count(*) from EismIvyk2021;
-- # kiek procentų nuo visų įvykių įvyko šiuose 5kiuose adresuose?
-- #procentinę vizulizaciją pateikite su pie plot.
select 
case
when ivykioVieta in (select * from(select ivykioVieta from EismIvyk2021 group by ivykioVieta order by count(*) desc limit 5)as f) then ivykioVieta
else 'Kitos'
end as Vieta, count(*) as r
from EismIvyk2021
group by Vieta;

-- # Suraskite, kuriuose rajonuose įvyksta daugiausiai susišaudymų? Vizualizuokite. nypd
select BORO, count(*) from nypd
group by BORO
order BY count(*) desc;
-- # suraskite, kuriomis valandomis įvyksta daugiausiai susišaudymų? Vizualizuokite.
select hour(cast(OCCUR_TIME as time)) as t, count(*) from nypd
group by t order by count(*) desc;
-- # Kuriomis valandomis (procentiškai) įvyksta daugiausiai mirtinų susišaudymų? Vizualizuokite.
select hour(cast(OCCUR_TIME as time)) as t, count(*) from nypd
where STATISTICAL_MURDER_FLAG = 1
group by t order by count(*) desc;

select * from nypd;

-- # turite informaciją apie užpuoliko lytį, amžiaus grupę, rasę, bei tą pačią infromaciją apie auką. 
-- # kokia vyraujanti aukos rasė, amžiaus grupė, lytis, užpuoliko amž grupė, rasė, lytis?
-- # Ar užpuolikai renkasi savo amžiaus, lyties, rasės aukas ar ne?

select PERP_RACE as PR, PERP_SEX, PERP_AGE_GROUP, VIC_RACE, VIC_SEX, VIC_AGE_GROUP, count(*) from nypd
where PERP_RACE<> '' and PERP_RACE <> 'UNKNOWN' and PERP_AGE_GROUP <> 'UNKNOWN'
group by PERP_RACE, PERP_SEX, PERP_AGE_GROUP, VIC_RACE, VIC_SEX, VIC_AGE_GROUP
order by count(*) desc limit 5;
