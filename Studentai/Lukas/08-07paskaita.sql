-- • Pateikite adresus su pašto kodais, miesto pavadinimu bei
-- šalimi. (address, city, country)
select * from address;
select* from city;
select * from country;
select address, postal_code , city, country
from address
join city on address.city_id = city.city_id
join country on city.country_id = country.country_id;


-- • Koks vidutinis filmų ilgis pagal kategorijas? (film,
-- film_category, category)
select * from film limit 2;
select * from film_category limit 2;
select * from category limit 2;
select avg(length), name
from film
join film_category on film.film_id = film_category.film_id
join category on film_category.category_id = category.category_id
group by name;


-- Kiek klientė Amy Lopez sumokėjo už filmo Rocky War nuomą?
-- (customer, payment, rental, inventory, film)
select first_name, last_name, sum(amount), title
from customer
join payment on customer.customer_id = payment.customer_id
join rental on payment.rental_id = rental.rental_id
join inventory on rental.inventory_id = inventory.inventory_id
join film on inventory.film_id = film.film_id
where first_name like 'amy' and title like 'Rocky%';


-- Kada paskutinį kartą ir kiek sumokėjo klientė BETTY WHITE?
-- (payment, customer)

select first_name, last_name, payment_date, amount
from customer
join payment on customer.customer_id = payment.customer_id
where first_name like 'betty'
order by payment_date desc limit 1;


-- Parašykite SQL užklausą, suteikiančią klientų vardus, pavardes, jų
-- iš viso nuomai išleidžiamą sumą (stulpelyje „Iš viso“), o stulpelyje
-- „Rėžiai“ pateikite suskirstytus klientus tokiu būdu:
-- • klientus, kurie iš viso nuomai išleidžia 100 ir daugiau,
-- pažymėkite kaip „Virš 100“,
-- • o išleidžiančius iki 100 pažymėkite „Iki 100“.
-- (customer, payment)
select first_name, last_name, sum(amount) as 'Is viso',
case
when sum(amount) > 100 then 'virs 100'
else 'iki 100'
end as 'reziai'
from customer
join payment on customer.customer_id = payment.customer_id
group by last_name;

create table KlientaiLB
(
	id int auto_increment not null primary key,
    vardas char(255),
    pavarde char(255)
);

drop table KlientaiLB;

insert into KlientaiLB (vardas, pavarde)
values('Jonas', 'Jonaitis'),
('Petras', null);

select * from KlientaiLB;

create temporary table Klientai_tempLB
(
id int not null primary key,
vardas varchar(255),
kompanija varchar(100)
);

select * from Klientai_tempLB;

-- • Sukurkite lentelės „customer“ kopiją kaip laikiną lentelę ir
-- išsaugokite ją pavadinimu „Klientai“.
create temporary table KlientaiLB
select * from customer;

select * from KlientaiLB;

-- • Lentelėje „Klientai“ pakeiskite klientės Linda Williams el.pašto
-- adresą į linda.williams@gmail.com.
update KlientaiLB
set email = 'linda.williams@gmail.com'
where first_name='linda' and last_name='williams';
-- • Lentelėje „Klientai“ pakeiskite adreso kodą iš 10 į 21 klientei
-- Jennifer Davis.
update KlientaiLB
set address_id = 21
where first_name='jennifer' and last_name='davis';

-- • Iš lentelės „Klientai“ pašalinkite klientę Mary Smith.
delete from KlientaiLB
where first_name='mary' and last_name='smith';

-- • Iš lentelės „Klientai“ pašalinkite klientus, kurių kodas yra
-- intervale [4, 6].
delete from KlientaiLB
where customer_id between 20 and 22;

-- kiek dalyvavo apklausose vyrų, moterų 2014 ir 2018 metais?
--  Parodykite absoliučius dydžius, jų skirtumą, bei pridėkite stulpelį dar, kur pokytis būtų procentais.
-- lytis, M - male, f - female
select *, kiekis2018 - kiekis2014 as skirtumas,(kiekis2018-kiekis2014)/kiekis2014*100.0 as `Δ[%]` from
(select count(*)as kiekis2014, lytis 
from DUS2014N 
group by lytis) as T
inner join
(select count(*) as kiekis2018, lytis from DUS2018N  
group by lytis) as D
using (lytis); 




-- Suraskite vidutinį vyrų, moterų atlyginimą 2014 metais ir 2018 metais. parodykite procentinį skirtumą tarp metų.
-- stulpelis bdu_spalio
-- spalio mėnesio atlyginimas

