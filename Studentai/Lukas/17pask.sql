select first_name, last_name from actor;
select last_name, 'Labas' from actor;

select last_name, first_name from actor order by last_name desc, first_name asc;

-- • Atrinkti visus filmus kurie trunka daugiau negu 100 minučių.
-- Lentelė film.
select * from film limit 5;
select title, release_year, length from film where length > 100;
-- • Raskite adresus, kurie yra Ahal rajone (district). Lentelė
-- address.
select * from address limit 5;
select address, district from address where district = 'ahal';
-- • Parašykite užklausą, kuri pateiktų visą informaciją apie
-- filmus, kurių nuomos trukmė yra 3 dienos.
select * from film where rental_duration = 3;

-- • Pateikite filmo pavadinimą, aprašymą, išleidimo metus,
-- reitingą, kur reitingas yra G.
select title, description, release_year, rating from film where rating = 'G';

-- • Atrinkite visus filmus, trunkančius trumpiau nei 50 min arba
-- ilgiau nei 140 min.
select title, length from film where length <=50 or length >=140;

-- • Atrinkite visus adresus be pašto kodo ar telefono numerio.
-- Lentelė address
select * from address limit 5;
select address from address where postal_code='' or phone='';

-- • Atrinkite visus adresus be pašto kodo ir telefono numerio.
select address from address where postal_code='' and phone='';


-- • Atrinkite filmus,kurie buvo nuomoti ilgiau nei 5 dienoms, o jų
-- pakeitimo kaina mažesnė arba lygi 20.
select *from film limit 5;
select title, rental_duration, replacement_cost from film where rental_duration > 5 and replacement_cost <= 20;

-- • Atrinkite ’R’ reitingo filmus, kurių nuomos kaina yra didesnė
-- nei 3.
select title from film where rating = 'R' and rental_rate > 3;
-- • Išveskite informaciją apie pirmus penkis klientus. Lentelė
-- customer.
select * from customer limit 5;
-- • Raskite 10 trumpiausių filmų, išveskite jų pavadinimus ir
-- trukmę.
select * from film limit 2;
select title, length from film order by length asc limit 10;

-- • Suraskite, kokia mažiausia filmų trukmė. Lentelė film.
select title, min(length) from film;
select title, length from film where length = 46;

-- • Suraskite ilgiausią filmų trukmę.
select title, max(length) from film;
select title, length from film where length in (select max(length) from film);

-- • Kokia vidutinė filmų trukmė? (115.2720 min.)
select avg(length) from film;
-- • Kiek reikėtų praleisti valandų, norint peržiūrėti visus filmus,
-- esančius DB? (1921.2 h)
select sum(length)/60 from film;

-- • Atrinkite filmus, kurių trukmė yra a) minimali; b) maksimali; c)
-- vidutinė
-- • Ar yra filmų, kurių trukmė yra minimali, o antroji pavadinimo
-- raidė yra 'L'?
select title from film where length = 46 and title like '_L%';

select title, length from film
where length in (select min(length) from film);

select title, length from film
where length in (select max(length) from film);

select title, length from film
where length in (select round(avg(length)) from film);

-- • Kokio filmo aprašymas ilgiausias?
select title, max(length(description)) from film
where length(description) in (select max(length(description)) from film);


-- • Pateikite filmus ir jų išleidimo metus viename stulpelyje,
-- pavadinimu Filmai
select concat(title, ' ', release_year) as Filmai from film;

-- • Kokio filmo aprašymas turi daugiausia žodžių?
select length(description) - length(replace(description, ' ', '')) + 1 as z,
title, description
from film order by z desc limit 3;
-- • Kaip suskaičiuosite su SQL funkcijomis sakinyje esančius
-- žodžius?

-- • Po kiek buvo nuomojami filmai ir kiek filmų turėjo vienodas
-- nuomos kainas?
select rental_rate, count(*)
from film
group by rental_rate;

-- • Kiek kainuotų išsinuomoti visus to paties reitingo filmus?
select rental_rate, sum(rental_rate), count(*), rating
from film
group by rating, rental_rate;
-- • Kiek kainuotų išsinuomoti visus filmus, kurie prasideda raide
-- ’A’, ir turi tą patį reitingą?
select rating, sum(rental_rate)
from film
where title like 'a&'
group by rating;



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

select rating, sum(rental_rate) from film
where title like 'a%'
group by rating;