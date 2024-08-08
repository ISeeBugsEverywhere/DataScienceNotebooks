select count(*) as C,  -- --nurodome stulpelio name  
rating as R
from film
group by rating
having count(*) > 200;    -- apsiribojame grupemis >200 -- Klasikinis SQL

--
select count(*) as C,  -- --nurodome stulpelio name  
rating as R
from film
group by rating
having C > 200 and R = 'PG-13';    -- naudojame C raide vietoje count(*) -- galima naudoti select'e C arba R (MySQL feature).

--
select count(*), rating from film 
group by rating 
having avg(length) > 118; -- lenght - stulpelio pavadinimas 

-- where - veikia pagal stulpeli 
-- having - gali dirbti su grupemis 

-- CASE skaidres 

select actor_id,
case                                         -- case stulpelis atsiranda toje pacioje pozicijoje kurioje parasote 
when actor_id MOD 3= 0 then 'Dalus is 3'
when actor_id MOD 2 = 0 then 'Lygins'   -- veikia panasiai kaip IF
else 'Nelyginis'       
end as Lyginumas, last_name                           
from actor;


select count(*),
case                                         -- case stulpelis atsiranda toje pacioje pozicijoje kurioje parasote 
when actor_id MOD 3= 0 then 'Dalus is 3'
when actor_id MOD 2 = 0 then 'Lygins'   -- veikia panasiai kaip IF
else 'Nelyginis'       
end as Lyginumas                          
from actor
group by Lyginumas; 



select actor_id,
if((actor_id % 2) = 0, 'Lyg', 'Nelyg') as IFas    -- trumpa IF forma
from actor;

-- ----------------------------------------------------------------------------------------------------------
-- Kas antro aktoriaus vardą parašykite mažosiomis raidėmis, kas
-- trečio - pavardę.

SELECT 
    actor_id,
    IF(actor_id MOD 2 = 0, LOWER(first_name), first_name) AS vardas,
    CASE
        WHEN actor_id MOD 3 = 0 THEN LOWER(last_name)
        ELSE last_name
    END AS Pavarde
FROM actor
ORDER BY actor_id ASC;
-- -------------------------------------------------------------------------------------------------------------

-- • Iš lentelės rental išrinkite įrašus, kurių return_date būtų
-- birželio mėnuo.

select * from rental where month(return_date) = 6;

select return_date from rental 
where return_date like '%-06-%';

-- • Suskaičiuokite kiek klientų (lentelė customer) yra aktyvių ir
-- kiek pasyvių. Jei stulpelyje active yra reikšmė 1 - tai aktyvus
-- klientas, o jei 0 - tai neaktyvus. Naudodami CASE aiškiai
-- parodykite, kur yra aktyvūs klientai, o kur - ne.

select *,
IF(active = 0, 'pasyvus', 'aktyvus') AS aktyvumas
from customer;

SELECT count(*),
    CASE 
        WHEN active = 0 THEN 'pasyvus'
        ELSE 'aktyvus'
    END AS aktyvumas
FROM customer
group by active;

SELECT 
    CASE 
        WHEN active = 1 THEN 'Aktyvus'
        ELSE 'Neaktyvus'
    END AS Kliento_statusas,
    COUNT(*) AS Klientu_skaicius
FROM customer
GROUP BY Kliento_statusas;

-- --------------------------------------------------------
-- Group concat - sutraukia visus grupes objektus i teksta. 

select rating, group_concat(title separator '//')
from film 
group by rating;


-- -----------------------------------------------------------
-- substring('where', start, length)  - teksto iskirpimas 

select substring(first_name, 1,3) from actor;

-- ------------------------------------------------------------
-- FLOOR(x.y)  - apavalina prie arciausio sveiko skaiciaus. 
-- CEIL()

select floor(3/4);
select ceil(3/4);


-- -----------------------------------------------------------------
-- STR_TO_DATE() - teksta konvertuoja i norima datos sablona. 

SELECT STR_TO_DATE('Wednesday, 10 February 2021, 12:30:20', '%W,%d %M %Y, %T') as Data ;


-- -----------------------------------------------------------------------
--    JUNGIMAS VERTIKALIAI 
-- UNION (nepalieka eiluciu) ir UNION ALL (palieka eilutes)  - raktazodziai sujungti 
 
 select first_name, last_name, 'stulpelis treciam columns' from actor 
 union all                  						     -- netikrina kokie duomenys yra stulpelyje 
 select customer_id, last_name, last_name from customer;

-- -----------------------------------------------------------------------

 select first_name, last_name from actor 
 union                        							-- istrina absoluciai vienodas eilutes 
 select first_name, last_name from customer;

-- -----------------------------------------------------------------------

-- Parašykite SQL užklausą, pateikiančią klientų id, sumokamą
-- mokestį už nuomą. Tuos klientus, kurie sumoka už nuomą vienu
-- kartu virš 10, pažymėkite kaip „Virš 10“, o išleidžiančius iki 10,
-- pažymėkite „Iki 10“. Surūšiuokite pagal nuomos mokestį
-- mažėjimo tvarka.

select customer_id, amount, 
IF(amount > 10, 'virs 10', 'maziau 10') AS Mokejimo_dydis
from payment
order by amount desc;



SELECT 
    customer_id, amount,
    CASE 
        WHEN MAX(amount) > 10 THEN 'virs 10'
        ELSE 'maziau 10'
    END AS Mokejimo_dydis
FROM payment
GROUP BY customer_id
ORDER BY MAX(amount) DESC;


select customer_id, amount, if(amount > 10, 'Virš 10', 'Iki 10') as C from payment
order by amount desc;


select customer_id, amount, 'virš 10'as C from payment
where amount > 10
union all
select customer_id, amount, 'Iki 10' from payment
where amount < 10
order by amount desc;


-- -----------------------------------------------------------------------
-- • Pateikite klientų sąrašą (lentelė payment) su mokėjimo data ir
-- didžiausiu kiekvieno kliento mokėjimu, bet tik tų klientų,
-- kurių didžiausias mokėjimas tą dieną yra šiame sąraše: 2.99,
-- 3.99 ir 4.99.

-- HINTAI: grazinate data atmesdami laika date(), max funkcija, having šaka, in;
select * from payment;

select customer_id, max(amount), date(payment_date) from payment
where amount = 2.99 or amount = 3.99 or amount = 4.99
GROUP BY customer_id, DATE(payment_date);

SELECT customer_id, DATE(payment_date) AS payment_day, MAX(amount) AS max_amount
FROM payment
GROUP BY customer_id, DATE(payment_date)
HAVING MAX(amount) IN (2.99, 3.99, 4.99)
ORDER BY customer_id, payment_day;

-- Teisingas sprendimas -- 
select customer_id, date(payment_date), max(amount)
from payment 
group by customer_id, date(payment_date)
having max(amount) in (2.99,3.99,4.99);

-- -----------------------------------------------------------------------
-- LENTELIU SUJUNGIMAS: JOIN tipas 
-- Inner joinas - prarandame info is desionios ir kairiosios lenteliu 
-- Left joinas - palieka info is kairiosios lenteles ir paima info is desionios lenteles (ten kur truksta duomenu - null).
-- Right joinas - veikia atvirksciai nei left joinas. 
-- rasoma is kaires i desine. 

select *  from customer limit 2;

select customer.customer_id, first_name, last_name, amount
from payment 
inner join customer
on payment.customer_id = customer.customer_id    -- arba using (customer_id)
where payment.rental_id between 1 and 11;


SELECT 
    C.customer_id, 
    C.first_name, 
    C.last_name, 
    P.amount, 
    S.first_name, 
    S.last_name
FROM payment AS P
INNER JOIN customer AS C USING (customer_id)
INNER JOIN staff AS S USING (staff_id)
WHERE P.rental_id BETWEEN 1 AND 11;

-- • Kiek kiekvienas darbuotojas surinko klientų apmokėjimų
-- (kiekis, suma)? (staff, payment)

select * from staff; 
select * from payment;

select staff.staff_id, staff.first_name, sum(payment.amount) from staff 
inner join payment
on payment.staff_id = staff.staff_id
group by first_name;



SELECT staff.staff_id, staff.first_name, SUM(payment.amount), count(payment.amount) AS total_collected
FROM staff 
INNER JOIN payment 
ON payment.staff_id = staff.staff_id
GROUP BY staff.staff_id, staff.first_name;



-- • Suraskite, kuriuos klientus kuris darbuotojas aptarnavo?
-- (staff, customer)  hint: store_id



SELECT 
    staff.first_name, staff.last_name, staff.store_id
FROM
    ↪ staff
        INNER JOIN
    store ON staff.store_id = store.store_id;

-- --------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------

-- • Pateikite adresus su pašto kodais, miesto pavadinimu bei
-- šalimi. (address, city, country)
-- • Koks vidutinis filmų ilgis pagal kategorijas? (film,
-- film_category, category)

select * from address;   -- address_id, address, address2, district, city_id, postal_code, phone, last_update
select * from city;    -- city_id, city, country_id, last update
select * from country;  -- country_id, country, last_update 


select address.address, address.postal_code, city.city, country.country from address
INNER JOIN city 
ON address.city_id = city.city_id
INNER JOIN country
ON country.country_id = city.country_id;


-- --------------------------------------------------------------------------------------------------------------
-- (customer, payment)
-- Kiek klientė Amy Lopez sumokėjo už filmo Rocky War nuomą?
-- (customer, payment, rental, inventory, film)
-- Kada paskutinį kartą ir kiek sumokėjo klientė BETTY WHITE?
-- (payment, customer)

-- ???????????????????????????????????????????????
select * from payment;    -- payment_id, customer_id, staff_id, rental_id, amount
select * from inventory;  -- film_id, inventory_id, store_id
select * from customer;    -- customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update
select * from rental;     -- customer.customer_id, customer.first_name, customer.last_name, customer.email, rental.rental_id, rental.rental_date,  rental.return_date
select * from film;    -- film_id, 

SELECT customer.first_name, customer.last_name, customer.customer_id, payment.rental_id, payment.amount from customer
INNER JOIN payment ON payment.customer_id = customer.customer_id
where customer.first_name = 'Amy';

select last_name, first_name, amount, title
from customer
join payment using (customer_id)
join rental using (rental_id)
join inventory using (inventory_id)
join film using (film_id)
where last_name = 'lopez' and first_name = 'amy'
and title = "rocky war";



SELECT customer.first_name, customer.last_name, customer.customer_id, payment.rental_id, payment.amount, payment.payment_date from customer
INNER JOIN payment ON payment.customer_id = customer.customer_id
where customer.first_name = 'Betty'
ORDER BY payment.payment_date DESC
Limit 1;   -- teisingas 

select last_name, first_name, amount, payment_date from 
payment
join customer using (customer_id)
where last_name = 'white' and first_name = 'Betty'
order by payment_date desc limit 1; -- kitas budas

-- --------------------------------------------------------------------------------------------------------------
-- Parašykite SQL užklausą, suteikiančią klientų vardus, pavardes, jų
-- iš viso nuomai išleidžiamą sumą (stulpelyje „Iš viso“), o stulpelyje
-- „Rėžiai“ pateikite suskirstytus klientus tokiu būdu:
-- • klientus, kurie iš viso nuomai išleidžia 100 ir daugiau,
-- pažymėkite kaip „Virš 100“,
-- • o išleidžiančius iki 100 pažymėkite „Iki 100“.
-- (customer, payment)


select * from payment;    -- payment_id, customer_id, staff_id, rental_id, amount
select * from inventory;  -- film_id, inventory_id, store_id
select * from customer;    -- customer_id, store_id, first_name, last_name, email, address_id, active, create_date, last_update


select first_name, last_name, sum(amount) from customer
inner join payment 
on customer.customer_id = payment.customer_id
group by first_name, last_name; 

-- --------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------
-- --------------------------------------------------------------------------------------------------------------
-- LENTELIU KURIMAS  

select * from
(select * from actor) as T;


SELECT * 
FROM (SELECT * 
      FROM actor
      ORDER BY actor_id DESC
      LIMIT 10) AS T
limit 3;

select 2/(select avg(length) from film);   -- gauname kazkoki skaiciu atsakymui 

select * from actor
where first_name in (select first_name from actor
where first_name like 'a%');


-- 
-- lenteles sukurimas 
create table KlientaiPS
(
 id int not null primary key,   -- primary key = unikalus dublikatas
 vardas char(255),
 pavarde char(255)
);

-- lenteles pasalinimas 
drop table KlientaiPS;

-- iterpimas i lentle 
select * from KlientaiPS;

insert into KlientaiPS (id, vardas, pavarde)
values (1, 'Patras', 'Petraitis'), 
(2, 'as', 'asdsad');

drop table KlientaiPS;

create table KlientaiPS
(
 id int auto_increment not null primary key,   -- primary key = unikalus dublikatas
 vardas char(255), 								-- auto_increment, leidzia pakartotinius insert (id yra auto_increment: 1,2,3,4,5)
 pavarde char(255)
);

insert into KlientaiPS (vardas, pavarde)
values ('Patras', 'Petraitis'), 
('as', 'asdsad');


select * from KlientaiPS;

-- Sukuriame laikina lentele 
 create temporary table Klientai_tempPS
(
id int not null primary key,
vardas varchar(255),
kompanija varchar(100)
);

select * from Klientai_tempPS;

create temporary table ATS   -- sukuria laikina lentele 
SELECT name, AVG(length), AVG(rental_duration) 
FROM film
JOIN film_category USING (film_id)
JOIN category USING (category_id)
GROUP BY name;


select * from ATS;

delete from ATS;  -- istrina visas eilutes 

drop table ATS;

delete from ATS
where name = 'Action';  -- istrina action eilute 

select * from ATS;

alter table ATS 
add STULPELIS float;  -- pridedame stulpeli 

update ATS 
set STULPELIS = (`avg(length)` + `avg(rental_duration)`)/100  -- idedame i back tick'us 
where name like 'D%'; 


-- --------------------------------------------------------------------------------------------


-- • Sukurkite lentelės „customer“ kopiją kaip laikiną lentelę ir
-- išsaugokite ją pavadinimu „Klientai“.

create temporary table KlientaiPS   -- sukuria laikina lentele 
SELECT * 
FROM customer;

select * from KlientaiPS;

--  • Lentelėje „Klientai“ pakeiskite klientės Linda Williams el.pašto
-- -- adresą į linda.williams@gmail.com.

update KlientaiPS
SET email = 'linda@gmail.com'
where first_name = 'LINDA' and last_name = 'Williams';


-- • Lentelėje „Klientai“ pakeiskite adreso kodą iš 10 į 21 klientei
-- Jennifer Davis.

update KlientaiPS
SET address_id = 21
where first_name = 'Jennifer' and last_name = 'Davis';

-- • Iš lentelės „Klientai“ pašalinkite klientę Mary Smith.

delete from KlientaiPS
where first_name = 'Mary' and last_name = 'Smith';



-- • Iš lentelės „Klientai“ pašalinkite klientus, kurių kodas yra
-- intervale [4, 6].

DELETE FROM KlientaiPS
WHERE customer_id BETWEEN 4 AND 6;


-- ------------------------------------------------------------------------------
-- WORKS DB 
select issilavinimas, avg(bdu_spalio)
from DUS2018N
group by issilavinimas;

select issilavinimas, avg(bdu_spalio)
from DUS2014N
group by issilavinimas;

-- norime paskaiciuoti skirtuma 

SELECT *, A18-A14 as delta
FROM 
    (SELECT issilavinimas, AVG(bdu_spalio) AS avg_bdu_spalio_2018  
     FROM DUS2018N
     GROUP BY issilavinimas) as T
INNER JOIN 
    (SELECT issilavinimas, AVG(bdu_spalio) AS avg_bdu_spalio_2014
     FROM DUS2014N
     GROUP BY issilavinimas) AS A14
USING (issilavinimas);
-- KLAIDA -------------------------------------------------

-- kiek dalyvavo apklausose vyrų, moterų 2014 ir 2018 metais? 
-- Parodykite absoliučius dydžius, jų skirtumą, bei pridėkite stulpelį dar, 
-- kur pokytis būtų procentais.
-- lytis, M - male, f - female



SELECT lytis, count(*) as '2018m' from DUS2018N
group by lytis
INNER JOIN
(SELECT lytis, count(*) as '2014m' from DUS2014N);




SELECT lytis, COUNT(*) AS count, '2018' AS year
FROM DUS2018N
GROUP BY lytis
INNER JOIN
SELECT lytis, COUNT(*) AS count, '2014' AS year
FROM DUS2014N
GROUP BY lytis;



-- Suraskite vidutinį vyrų, moterų atlyginimą 2014 metais ir 2018 metais. parodykite procentinį skirtumą tarp metų.
-- stulpelis bdu_spalio
-- spalio mėnesio atlyginimas










