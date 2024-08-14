select last_name, first_name from actor;
-- čia komentaras ctrl /
select last_name, 'Labas' from actor;

select last_name, first_name from actor
order by last_name desc, first_name asc;

-- Išveskite visus duomenis iš lentelės actor.
select * from actor;

-- Išveskite aktorių id ir pavardes iš lentelės actor.
select actor_id, last_name from actor;

-- Išveskite vardus ir pavardes iš lentelės actor, surikiuotus
-- pagal pavardes mažėjimo tvarka.
select first_name, last_name from actor
order by last_name desc;

-- Išveskite aktorių id, vardus ir pavardes iš lentelės actor,
-- surikiuotus pagal vardus didėjimo, pavardes mažėjimo tvarka
select actor_id, first_name, last_name from actor
order by first_name asc, last_name desc;
-- pervadinimas
select actor_id as ID from actor;
-- Rezultato apribojimas
select * from actor
limit 5;
-- 5 eilutės surikiuotos
select * from actor
order by first_name desc
limit 5;
-- atrenkamos konkrečios eilutės
select * from actor
where actor_id = 5 or actor_id = 6;

select * from actor
where first_name = 'grace';

select * from film limit 2;

-- Atrinkti visus filmus kurie trunka daugiau negu 100 minučių.
-- Lentelė film.
select * from film
where length >100;
-- Raskite adresus, kurie yra Ahal rajone (district). Lentelė
-- address.
select * from address
where district = 'Ahal';
-- Parašykite užklausą, kuri pateiktų visą informaciją apie
-- filmus, kurių nuomos trukmė yra 3 dienos.
select * from film
where rental_duration = 3;
-- Pateikite filmo pavadinimą, aprašymą, išleidimo metus,
-- reitingą, kur reitingas yra G.
select title, description, release_year, rating from film
where rating = 'G';
-- Atrinkite visus filmus, trunkančius trumpiau nei 50 min arba
-- ilgiau nei 140 min.
select * from film
where length <50 or length>140;
-- Atrinkite visus adresus be pašto kodo ar telefono numerio.
-- Lentelė address
select * from address
where postal_code = '' or phone = '';
-- Atrinkite visus adresus be pašto kodo ir telefono numerio.
select * from address
where postal_code = '' and phone = '';
-- Atrinkite filmus, kurie buvo nuomoti ilgiau nei 5 dienoms, o jų
-- pakeitimo kaina mažesnė arba lygi 20.
select * from film
where rental_duration > 5 and replacement_cost <= 20;
-- Atrinkite ’R’ reitingo filmus, kurių nuomos kaina yra didesnė
-- nei 3.
select * from film
where rating = 'R' and rental_rate > 3;
-- Išveskite informaciją apie pirmus penkis klientus. Lentelė
-- customer.
select * from customer
limit 5;
-- Raskite 10 trumpiausių filmų, išveskite jų pavadinimus ir
-- trukmę.
select title, length from film
order by length asc
limit 10;
-- datą supranta nepilną
select * from payment
where payment_date between '2005-07-01' and '2005-08-01';
-- su cast():
select * from payment
where payment_date between
cast('2005-07-01' as DATE)
and cast('2005-08-01' as DATE);
-- Jei vertė yra alfabetiškai tarp ’A’ ir ’B’ - ji bus rezultate.
select first_name from actor
where first_name between 'A' and 'C';
-- prasideda N raide
select * from actor
where first_name like 'N%';
-- 2 simbolis E raide
select * from actor
where first_name like '_E%';
-- viskas su E raide
select * from actor
where first_name like '%E%';
-- susumuoti visus actoriu id
select sum(actor_id) as Suma, avg(actor_id) from actor;
-- atrinktų eilučių atsakymai
select sum(actor_id) as Suma, avg(actor_id) from actor
where first_name like 'A%';

-- Suraskite, kokia mažiausia filmų trukmė. Lentelė film.
select min(length) from film;
-- Suraskite ilgiausią filmų trukmę.
select max(length) from film;
-- Kokia vidutinė filmų trukmė? (115.2720 min.)
select avg(length) from film;
-- Kiek reikėtų praleisti valandų, norint peržiūrėti visus filmus,
-- esančius DB? (1921.2 h)
select sum(length)/60 from film;
-- Atrinkite filmus, kurių trukmė yra a) minimali;
select title from film
where length = 46;
-- b) maksimali; 
select title from film
where length = 185;
-- c) vidutinė
select title from film
where length = 115;
-- Ar yra filmų, kurių trukmė yra minimali, o antroji pavadinimo
-- raidė yra 'L'?
select title from film
where length = 46 and title like '_L%';
-- Atrinkite filmus, kurių trukmė yra a) minimali; 
select title, length from film
where length in (select min(length) from film);
-- b) maksimali; 
select title, length from film
where length in (select max(length) from film);
-- c) vidutinė
select title, length from film
where length in (select round(avg(length),0) from film);
-- sujungimas
select concat(first_name,' ', lower(last_name)) from actor;
-- simboliu pakeitimas
select replace(first_name, 'A', '3') from actor;
-- pašalina paskutinį simbolį
select trim(trailing'M' from'MADAM');
-- pašalina ir pirmą ir paskutinį simbolį
select trim(both 'M' from'MADAM');
-- pašalina pirmą simbolį
select trim(leading 'M' from'MADAM');


-- Kokio filmo aprašymas ilgiausias?
select length(description) as ilgis, title, description from film
order by ilgis desc
limit 1;
-- Pateikite filmus ir jų išleidimo metus viename stulpelyje,
-- pavadinimu Filmai
select concat(title, ' ' , release_year) as Filmai from film;
-- Kaip suskaičiuosite su SQL funkcijomis sakinyje esančius
-- žodžius?
select length(description) - length(replace(description, ' ', '')) + 1 as Žodziai, title, description from film
order by Žodziai desc;
-- Kokio filmo aprašymas turi daugiausia žodžių?
select length(description) - length(replace(description, ' ', '')) + 1 as Žodziai, title, description from film
order by Žodziai desc
limit 2;

select * from film limit 5;

select rental_duration, count(*), avg(length), min(replacement_cost) as M, group_concat(title)
from film
where title like 'a%'
group by rental_duration
order by M desc;

select rental_duration, rental_rate, count(*)
from film
group by rental_duration, rental_rate;

-- Po kiek buvo nuomojami filmai ir kiek filmų turėjo vienodas
-- nuomos kainas?
select rental_rate, count(*) from film group by rental_rate;
-- Kiek kainuotų išsinuomoti visus to paties reitingo filmus?
select rating, sum(rental_rate) from film group by rating;
-- Kiek kainuotų išsinuomoti visus filmus, kurie prasideda raide
-- ’A’, ir turi tą patį reitingą?
select rating, sum(rental_rate) from film where title like 'a%' group by rating;