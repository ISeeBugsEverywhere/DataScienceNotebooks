select last_name from actor;                   -- Paprastas duomenu paemimas
select last_name, 'labas'  from actor;         -- Paima last_name stulpeli ir sukuria salia stulpeli su 'labas' 
select last_name, first_name from actor
order by last_name desc, first_name asc;       -- Surusiuojame pagal didejimo/mazejimo skaidre 


-- • Išveskite visus duomenis iš lentelės actor.
-- • Išveskite aktorių id ir pavardes iš lentelės actor.
-- • Išveskite vardus ir pavardes iš lentelės actor, surikiuotus
-- pagal pavardes mažėjimo tvarka.
-- • Išveskite aktorių id, vardus ir pavardes iš lentelės actor,
-- surikiuotus pagal vardus didėjimo, pavardes mažėjimo tvarka

select * from actor;

select actor_id, first_name, last_name from actor 
order by last_name desc, first_name asc;

select 4*5;

select actor_id as ID from actor;

select * from actor
order by first_name desc
limit 5;

select * from actor 
where actor_id <=6 OR actor_id = 50
order by actor_id desc
limit 1;

select * from actor
where actor_id > 6 and actor_id < 16;

select * from actor
where first_name = 'grace';

select * from film limit 2;   -- pasitikriname kas yra lenteleje 

select * from film 
where length < 100;   -- Atrinkti visus filmus kurie trunka daugiau negu 100 minučių. Lentelė film.

select * from address where district = 'Ahal'; -- • Raskite adresus, kurie yra Ahal rajone (district). Lentelė address.

select * from film 
where rental_duration = 3;  -- • Parašykite užklausą, kuri pateiktų visą informaciją apie filmus, kurių nuomos trukmė yra 3 dienos.

select title, description, release_year, rating from film   -- • Pateikite filmo pavadinimą, aprašymą, išleidimo metus, reitingą, kur reitingas yra G.
where rating = 'G';

select * from address
where postal_code = '';   -- Lentelė address • Atrinkite visus adresus be pašto kodo ir telefono numerio.

select * from address
where postal_code = '' OR phone = '';   -- • Atrinkite visus adresus be pašto kodo ar telefono numerio. 


select * from film 
where rental_duration > 5 AND replacement_cost <= 20;   -- • Atrinkite filmus,kurie buvo nuomoti ilgiau nei 5 dienoms, o jų pakeitimo kaina mažesnė arba lygi 20.

select * from film 
where rating = 'R' AND rental_rate > 3;    -- • Atrinkite ’R’ reitingo filmus, kurių nuomos kaina yra didesnė nei 3.

select * from customer   -- • Išveskite informaciją apie pirmus penkis klientus. 
limit 5;


select title, length from film   -- • Raskite 10 trumpiausių filmų, išveskite jų pavadinimus ir trukmę.
order by length asc
limit 10;

select * from payment
where payment_date between '2005-07-01' and '2005-08-01';

select * from payment
where payment_date between
cast('2005-07-01' as DATE) and cast('2005-08-01' as DATE);   

select * from actor 
where first_name like 'N%';   -- Isrusiuojame visus vardus pagal N 

select * from actor 
where first_name like '_E%';


select sum(actor_id) as Suma, avg(actor_id) from actor   -- PASIAISKINTI 
where first_name like 'A%';

SELECT * FROM film
WHERE length = (SELECT MIN(length) FROM film);   -- • Suraskite, kokia mažiausia filmų trukmė. Lentelė film.

SELECT avg(length) FROM film;   -- • Kokia vidutinė filmų trukmė? (115.2720 min.)

select * from film 
where rating like 'D%';    -- • Kiek reikėtų praleisti valandų, norint peržiūrėti visus filmus, -- esančius DB? (1921.2 h)

select * from film
WHERE length = (SELECT MIN(length) FROM film) AND length = '_L%';   -- • Ar yra filmų, kurių trukmė yra minimali, o antroji pavadinimo raidė yra 'L'?

select * from film
WHERE length = (SELECT MIN(length) FROM film) OR length = (SELECT MAX(length) FROM film) OR length = (SELECT AVG(length) FROM film);  -- • Atrinkite filmus, kurių trukmė yra a) minimali; b) maksimali; c)vidutinė

SELECT title, length 
FROM film 
WHERE length IN ((SELECT MIN(length) FROM film), (SELECT round(AVG(length)) FROM film), (SELECT MAX(length) FROM film));

SELECT * FROM film WHERE LENGTH(title) = (SELECT MAX(LENGTH(title)) FROM film);   -- • Kokio filmo aprašymas ilgiausias?

SELECT CONCAT(title, ' (', release_year, ')') AS Filmai FROM film;  -- • Pateikite filmus ir jų išleidimo metus viename stulpelyje, pavadinimu Filmai



select * from film;

SELECT description, LENGTH(description) AS raides, LENGTH(REPLACE(title, ' ', '')) as tarpai FROM film;   -- • Kokio filmo aprašymas turi daugiausia žodžių?

SELECT LENGTH(REPLACE(description, ' ', '')) as tarpai FROM film;


-- • Kiek kainuotų išsinuomoti visus to paties reitingo filmus?




SELECT rental_rate, COUNT(*) AS kiekis FROM film GROUP BY rental_rate;  -- • Po kiek buvo nuomojami filmai ir kiek filmų turėjo vienodas nuomos kainas?

SELECT rating, SUM(rental_rate) AS grupes_kaina FROM film WHERE title LIKE 'A%' GROUP BY rating; -- • Kiek kainuotų išsinuomoti visus filmus, kurie prasideda raide ’A’, ir turi tą patį reitingą?


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



 



