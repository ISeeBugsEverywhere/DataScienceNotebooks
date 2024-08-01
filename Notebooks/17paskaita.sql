select last_name, first_name from actor;
-- čia komentaras ctrl /
select last_name, 'Labas' from actor;

select last_name, first_name from actor
order by last_name desc, first_name asc;

-- • Išveskite visus duomenis iš lentelės actor.
-- • Išveskite aktorių id ir pavardes iš lentelės actor.
-- • Išveskite vardus ir pavardes iš lentelės actor, surikiuotus
-- pagal pavardes mažėjimo tvarka.
-- • Išveskite aktorių id, vardus ir pavardes iš lentelės actor,
-- surikiuotus pagal vardus didėjimo, pavardes mažėjimo tvarka
select actor_id, first_name, last_name
from actor
order by first_name asc, last_name desc;

select actor_id as ID from actor;

select * from actor
order by first_name desc
limit 5;

select * from actor
where actor_id = 5 or actor_id = 6
order by actor_id desc
limit 1;

select * from actor
where actor_id > 6 and actor_id < 16;

select * from actor
where first_name = 'grace';

select * from film limit 2;

select * from address limit 2;
-- • Atrinkite visus adresus be pašto kodo ar telefono numerio.
-- Lentelė address
select * from address
where postal_code = '' or phone = '';
-- • Atrinkite visus adresus be pašto kodo ir telefono numerio.

select title, length from film
where length between 50 and 90;

select * from payment
where payment_date between '2005-07-01' and '2005-08-01';

select * from payment
where payment_date between
cast('2005-07-01' as DATE)
and cast('2005-08-01' as DATE);

select cast(1 as float);


select first_name from actor
where first_name between 'A' and 'C';

select * from actor
where actor_id not in (1,2,5,6);

select * from actor
where first_name like 'N%';

select * from actor
where first_name like '__E%';

select sum(actor_id) as Suma, avg(actor_id) from actor;

select sum(actor_id) as Suma, avg(actor_id)/3.4528,
count(*)
from actor
where first_name like 'A%';


select min(length), title from film;
select * from film limit 1;

select min(length) from film;

select title, length from film
where length in (select round(avg(length)) from film);

select concat(first_name,';', lower(last_name)), last_name from actor;

select replace(first_name, 'A', '3') from actor;

select trim(both 'K' from first_name), first_name from actor;

-- • Kokio filmo aprašymas ilgiausias?



-- • Pateikite filmus ir jų išleidimo metus viename stulpelyje,
-- pavadinimu Filmai
-- • Kaip suskaičiuosite su SQL funkcijomis sakinyje esančius
-- žodžius?
select length(description) - length(replace(description, ' ', '')) + 1 as z,
title, description
from film;
-- • Kokio filmo aprašymas turi daugiausia žodžių?
select length(description) - length(replace(description, ' ', '')) + 1 as z,
title, description
from film
order by z desc limit 2;

select * from film limit 5;

select rental_duration as NuomosTrukmė, count(*), 
avg(length), min(replacement_cost) as M, group_concat(title)
from film
where title like 'a%'
group by rental_duration
order by M desc;

select rental_duration, rental_rate, count(*)
from film
group by rental_duration, rental_rate;


-- • Po kiek buvo nuomojami filmai ir kiek filmų turėjo vienodas
-- nuomos kainas?
select rental_rate, count(*) from film group by rental_rate;
-- • Kiek kainuotų išsinuomoti visus to paties reitingo filmus?
select rating, sum(rental_rate) from film group by rating;
-- • Kiek kainuotų išsinuomoti visus filmus, kurie prasideda raide
-- ’A’, ir turi tą patį reitingą?
select rating, sum(rental_rate) from film
where title like 'a%'
group by rating;




