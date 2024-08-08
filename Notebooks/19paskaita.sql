use sakila;
-- • Pateikite adresus su pašto kodais, miesto pavadinimu bei
-- šalimi. (address, city, country)
select address, postal_code, city, country
from address
inner join city using (city_id)
inner join country using (country_id);


-- • Koks vidutinis filmų ilgis pagal kategorijas? (film,
-- film_category, category)

select name, avg(length), avg(rental_duration) from film
join film_category using (film_id)
join category using (category_id)
group by name;



-- Parašykite SQL užklausą, suteikiančią klientų vardus, pavardes, jų
-- iš viso nuomai išleidžiamą sumą (stulpelyje „Iš viso“), o stulpelyje
-- „Rėžiai“ pateikite suskirstytus klientus tokiu būdu:
-- • klientus, kurie iš viso nuomai išleidžia 100 ir daugiau,
-- pažymėkite kaip „Virš 100“,
-- • o išleidžiančius iki 100 pažymėkite „Iki 100“.
-- (customer, payment)

select customer_id, first_name, last_name, sum(amount) as C,
case
when sum(amount) > 100 then 'Virš 100'
else 'Iki 100'
end as Rėžiai
from customer
join payment using (customer_id)
group by customer_id; 

-- Kiek klientė Amy Lopez sumokėjo už filmo Rocky War nuomą?
-- (customer, payment, rental, inventory, film)
select last_name, first_name, amount, title
from customer
join payment using (customer_id)
join rental using (rental_id)
join inventory using (inventory_id)
join film using (film_id)
where last_name = 'lopez' and first_name = 'amy'
and title = "rocky war";




-- Kada paskutinį kartą ir kiek sumokėjo klientė BETTY WHITE?
-- (payment, customer)

select last_name, first_name, amount, payment_date from 
payment
join customer using (customer_id)
where last_name = 'white' and first_name = 'Betty'
order by payment_date desc limit 1;


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

-- 
create table Klientai
(
	id int auto_increment not null primary key,
    vardas char(255),
    pavardė char(255)
);

-- pašalinimas
drop table Klientai;

select * from Klientai;

insert into Klientai (vardas, pavardė)
values ('Petras', 'Petraitis'),
('Unė Vardenė', 'UPS');


create temporary table Klientai_temp
(
id int not null primary key,
vardas varchar(255),
kompanija varchar(100)
);

select * from Klientai_temp;

create temporary table ATS
select name, avg(length), avg(rental_duration) from film
join film_category using (film_id)
join category using (category_id)
group by name;

select * from ATS;

delete from ATS
where name = 'Action';

drop table ATS;

select * from ATS;

alter table ATS
add STULPELIS float;

update ATS
set STULPELIS=(`avg(length)`+`avg(rental_duration)`)/100
where name like 'D%';
;
-- WORKS DB

select *, (A18-A14)/A14*100.0 as `Δ[%]` from
(select lytis, round(avg(bdu_spalio)/3.4528) as A14
from DUS2014N
group by lytis) as T
inner join
(select lytis, round(avg(bdu_spalio)) as A18
from DUS2018N
group by lytis) as D
using (lytis);










