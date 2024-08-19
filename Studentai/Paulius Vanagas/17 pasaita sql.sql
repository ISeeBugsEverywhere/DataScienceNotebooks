select last_name, first_name from actor;
-- komentaras
select 4+3 from actor;

select last_name, first_name from actor
order by last_name desc, first_name asc;

select * from actor;

select actor_id, last_name from actor;

select first_name, last_name from actor 
order by last_name desc;

select actor_id, first_name, last_name from actor 
order by first_name asc, last_name desc;

select * from actor
limit 5;

select * from actor
where actor_id = 5 or actor_id >= 20
order by first_name desc
limit 5;

select * from actor
where first_name = 'grace';

-- Atrinkti visus filmus kurie trunka daugiau negu 100 minučių.
-- Lentelė film.

select title, length from film
where length > 100;

-- Raskite adresus, kurie yra Ahal rajone (district). Lentelė
-- address.

select * from address
where district = 'ahal';

select * from film
where rental_duration = 3;

select title, description, release_year, rating from film
where rating='g';

select title from film
where length <50 or length > 140;

select address from address
where postal_code='' or phone='';

select address from address
where postal_code='' and phone='';

-- trinkite filmus,kurie buvo nuomoti ilgiau nei 5 dienoms, o jų
-- pakeitimo kaina mažesnė arba lygi 20

select title from film
where rental_duration >5 and replacement_cost <=20;

-- Atrinkite ’R’ reitingo filmus, kurių nuomos kaina yra didesnė
-- nei 3.

select title from film
where rating = 'r' and rental_rate >3;

select * from customer
limit 5;

select title, length from film
order by length asc
limit 10;

select * from payment
where payment_date between '2005-07-01' and '2005-08-01';

select * from payment
where payment_date between
cast('2005-07-01' as DATE)
and cast('2005-08-01' as DATE);


select first_name from actor
where first_name between 'A' and 'C';

select * from actor
where actor_id in (1, 5, 6, 8, 9, 15);

select * from actor
where first_name like 'N%';

select * from actor
where first_name like '_E%';

select title, min(length) from film;

select title, max(length) from film;

select avg(length) from film;

select sum(length)/60 from film;

select title, min(length) from film
where title like '_L%';

select min(length) from film;

select title, length from film
where length in (select min(length) from film);

select title, length from film
where length in (select max(length) from film);

select title, length from film
where length in (select round(avg(length)) from film);

select title from film
where description in (select max(description) from film);

select concat(title, ' ', release_year) as Filmai from film;

select title, length(description) - length(replace(description, ' ', '')) +1  from film;

select title, length(description) - length(replace(description, ' ', '')) +1 as ilgis from film
order by ilgis desc
limit 5;

select rental_rate, count(*) from film
group by rental_rate;

select rating, sum(rental_rate) from film
group by rating;

select rating, sum(rental_rate) from film
where title like 'A%'
group by rating;