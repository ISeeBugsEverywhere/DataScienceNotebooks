select * from actor ;
select * from film where `length`<50 OR `length`>140;
select * from address where postal_code='' OR phone='';
SELECT * FROM film where rental_duration>5 AND replacement_cost<=20;
SELECT * FROM film WHERE rating LIKE 'R' AND film.rental_rate>3;
SELECT * FROM customer ORDER BY customer_id limit 3;
SELECT title, length FROM film order by `length` ASC LIMIT 10;
SELECT * FROM film WHERE `length` BETWEEN 60 AND 90;
SELECT * FROM payment WHERE payment_date BETWEEN cast('2005-07-01' AS date) AND '2005-08-01';
SELECT * FROM actor WHERE first_name LIKE 'BE%';

SELECT `length` from film order by `length` LIMIT 1;
SELECT `length` from film order by `length` DESC LIMIT 1;
SELECT AVG(`length`) from film;
SELECT SUM(`length`) from film;
SELECT SUM(`length`) from film;
SELECT * FROM film WHERE length=46 and title like '_L%';

SELECT min(LENGTH) from film ;
SELECT * FROM film WHERE `length` in (SELECT MIN(`length`) FROM film);

select title, length from film where length in (select min(length) from film);
select title, length from film where length in (select max(length) from film);
select title, length from film where length in (select ROUND(avg(length)) from film);

SELECT CONCAT(first_name,' ',UPPER(last_name)) from actor;
SELECT REPLACE(first_name,'A','4') as `First name` from actor WHERE first_name LIKE '%A%';

SELECT LENGTH(title) as FL, title from film f order by FL desc limit 1;
SELECT CONCAT(title,' ',release_year) from film;
SELECT LENGTH(description)-LENGTH(replace(description ,' ',''))+1 as ZODZIAI, description, title from film order by ZODZIAI desc; 

SELECT * FROM film limit 5;
SELECT rental_duration as `Nuomos trukmė`, count(*) as N, ROUND(AVG(`length`)) as `Vid. ilgis` FROM film GROUP BY rental_duration ;

