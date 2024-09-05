-- # Turite nusiskaityti iš SQL DB lentelės autopliuslt į Pandas DataFrame gamintoją, 
-- # kainą, pagaminimo datą, ridą, pavarų tipą, variklio informaciją. 
-- # SQL užklausoje turite atmesti tuos įrašus, kur rida nenurodyta, taip pat palikite 
-- # tik nesikartojančius įrašus (atranka pagal ID stuleplį - jei ID sutampa - reiškia, jog skelbimas dubliuojasi)

select Gamintojas, pagaminimo_data as Data, cast(replace(price,' ','') as float) as Kaina, cast(replace(replace(rida,' ',''),'km','')as float) as Rida, pavaros as Pavaros, variklis as Variklis  from autopliuslt
where Rida <> 'Nenurodyta'
group by id;

select distinct id, rida, pagaminimo_data, price, rida from autopliuslt
where rida <> 'Nenurodyta';

with T1
as (select *, row_number() over (partition by id) as rc from autopliuslt)
select gamintojas, rida, price as kaina,
pagaminimo_data as data,
pavaros, variklis
from T1
where rc = 1 and rida != 'Nenurodyta' order by gamintojas;
