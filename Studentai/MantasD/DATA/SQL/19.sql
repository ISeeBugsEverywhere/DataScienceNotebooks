-- Pateikite adresus su pašto kodais, miesto pavadinimu bei
-- šalimi. (address, city, country)
select A.address as Adresas, A.postal_code as Pašto_kodas , C.city as Miestas, CO.country as Šalis
from address as A
left join city as C
using (city_id)
left join country as CO
using (country_id);
-- Koks vidutinis filmų ilgis pagal kategorijas? (film,
-- film_category, category)
select avg(F.length) as Vidutinis_ilgis, C.name as Kategorija
from film as F
left join film_category as FC
using (film_id)
left join category as C
using (category_id)
group by category_id;
-- Kiek klientė Amy Lopez sumokėjo už filmo Rocky War nuomą?
-- (customer, payment, rental, inventory, film)
select * from film
where title = 'rocky war';
select C.first_name, C.last_name, F.title, P.amount, P.payment_date
from customer as C
left join payment as P
using (customer_id)
left join rental as R
using (rental_id)
left join inventory as I
using (inventory_id)
left join film as F
using (film_id)
where C.first_name = 'amy' and C.last_name = 'lopez' and F.title = 'rocky war' ;
-- Kada paskutinį kartą ir kiek sumokėjo klientė BETTY WHITE?
-- (payment, customer)
select C.first_name, C.last_name, P.amount, P.payment_date
from customer as C
left join payment as P
using (customer_id)
where C.first_name = 'betty' and C.last_name = 'white'
order by P.payment_date desc
limit 1;
-- Parašykite SQL užklausą, suteikiančią klientų vardus, pavardes, jų
-- iš viso nuomai išleidžiamą sumą (stulpelyje „Iš viso“), o stulpelyje
-- „Rėžiai“ pateikite suskirstytus klientus tokiu būdu:
--  klientus, kurie iš viso nuomai išleidžia 100 ir daugiau,
-- pažymėkite kaip „Virš 100“,
-- o išleidžiančius iki 100 pažymėkite „Iki 100“.
-- (customer, payment)
select C.first_name as Vardas, C.last_name as Pavarde, sum(P.amount) as Suma,
if(sum(P.amount)>=100,'Virš 100', 'Iki 100') as Rėžiai
from customer as C
left join payment as P
using (customer_id)
group by C.first_name, C.last_name;

select * from
(select * from actor) as T;

select * from
(select * from actor
order by actor_id desc
limit 10) as T
limit 2;

select 2/(select avg(length) from film);

select * from actor
where first_name in (select first_name from actor
where first_name like 'a%');

-- lenteles kurimas
create table Klientai_MD
(
	id int auto_increment not null primary key,
    vardas char(255),
    pavardė char(255)
) ;
--  lenteles pasalinimas
drop table Klientai_MD;

select * from Klientai_MD;

insert into Klientai_MD (vardas, pavardė)
values ('Petras', 'Petraitis'),
('Unė Vardenė', 'UPS');

create temporary table Klientai_temp_MD
(
id int not null primary key,
vardas varchar(255),
kompanija varchar(100)
);

select * from Klientai_temp_MD;

create temporary table ATS_MD
select avg(F.length) as Vidutinis_ilgis, C.name as Kategorija
from film as F
left join film_category as FC
using (film_id)
left join category as C
using (category_id)
group by category_id;

select * from ATS_MD;

delete from ATS_MD
where Kategorija = 'Action';

drop table ATS_MD;

alter table ATS_MD
add STULPELIS float;

update ATS_MD
set STULPELIS = (Vidutinis_ilgis+5)/100
where Kategorija like 'D%';

-- Sukurkite lentelės „customer“ kopiją kaip laikiną lentelę ir
-- išsaugokite ją pavadinimu „Klientai“.
create temporary table KlientaiMD
select * from customer;
-- Lentelėje „Klientai“ pakeiskite klientės Linda Williams el.pašto
-- adresą į linda.williams@gmail.com.
select * from KlientaiMD;
update KlientaiMD
set email = 'linda.williams@gmail.com'
where first_name = 'linda' and last_name = 'williams';
-- Lentelėje „Klientai“ pakeiskite adreso kodą iš 10 į 21 klientei
-- Jennifer Davis.
update KlientaiMD
set address_id = 21
where first_name = 'Jennifer' and last_name = 'Davis' and address_id = 10;
-- Iš lentelės „Klientai“ pašalinkite klientę Mary Smith.
delete from KlientaiMD
where first_name = 'mary' and last_name = 'smith';
-- Iš lentelės „Klientai“ pašalinkite klientus, kurių kodas yra
-- intervale [4, 6].
delete from KlientaiMD
where customer_id between 4 and 6;

select * from KlientaiMD;

drop table KlientaiMD;

-- WORKS DB
select issilavinimas, avg(bdu_spalio)
from DUS2014N
group by issilavinimas;

-- Reikšmių sąrašas
-- "G1" Pradinis arba pagrindinis
-- (rengiama)
-- "G2" Vidurinis (Povidurinis profesinis, Specialusis vidurinis, Aukštesnysis)
-- (rengiama)
-- "G3" Aukštasis (bakalauro studijos)
-- (rengiama)
-- "G4" Aukštasis (magistro studijos ir doktorantūra)

select issilavinimas, avg(bdu_spalio)
from DUS2018N
group by issilavinimas;

select *, A18-A14 as Delta from
(select issilavinimas, avg(bdu_spalio)/3.4528 as A14
from DUS2014N
group by issilavinimas) as T
inner join
(select issilavinimas, avg(bdu_spalio) as A18
from DUS2018N
group by issilavinimas) as D
using (issilavinimas);

-- kiek dalyvavo apklausose vyrų, moterų 2014 ir 2018 metais? 
-- Parodykite absoliučius dydžius, jų skirtumą, bei pridėkite stulpelį dar, kur pokytis būtų procentais.
select *,K2018-K2014 as skirtumas , round((K2018-K2014)/K2014*100,2) as pokytis from
(select count(*) as K2014 , lytis from DUS2014N
group by lytis) as F
inner join
(select count(*) as K2018 , lytis from DUS2018N
group by lytis) as S
using (lytis);

-- Suraskite vidutinį vyrų, moterų atlyginimą 2014 metais ir 2018 metais. parodykite procentinį skirtumą tarp metų.
select *, round(A18-A14,0) as skirtumas, round((A18-A14)/A14*100,2) as pokytis from
(select lytis, round(avg(bdu_spalio)/3.4528,0) as A14
from DUS2014N
group by lytis) as T
inner join
(select lytis, round(avg(bdu_spalio),0) as A18
from DUS2018N
group by lytis) as D
using (lytis);

