select count(*) as C, 
rating as R
from film
group by rating
having count(*) > 200;

-- 

select count(*) as C, 
rating as R
from film
group by rating
having C > 200;

select count(*), rating, avg(length) from film
group by rating
having avg(length)>118;

select actor_id, first_name,
case
when actor_id MOD 3 = 0 then 'Dalus is triju'
when actor_id MOD 2 = 0 then 'Lyginis'
else 'Nelyginis'
end as Lyginumas, last_name
from actor;

--

select 
case
when actor_id MOD 3 = 0 then 'Dalus is triju'
when actor_id MOD 2 = 0 then 'Lyginis'
else 'Nelyginis'
end as Lyginumas, count(*)
from actor
group by Lyginumas;

select actor_id,
if((actor_id % 2) = 0, 'Lyg', 'Nelyg') as IFas
from actor;

-- Kas antro aktoriaus vardą parašykite mažosiomis raidėmis, kas
-- trečio - pavardę.
select actor_id as ID,
case
when actor_id MOD 2 = 0 then lower(first_name)
else first_name
end as Vardas,
case
when actor_id MOD 3 = 0 then lower(last_name)
else last_name
end as Pavardė
from actor
order by ID asc;

-- Iš lentelės rental išrinkite įrašus, kurių return_date būtų
-- birželio mėnuo.
select * from rental
where return_date like '%-06-%'
order by return_date asc;
-- Suskaičiuokite kiek klientų (lentelė customer) yra aktyvių ir
-- kiek pasyvių. Jei stulpelyje active yra reikšmė 1 - tai aktyvus
-- klientas, o jei 0 - tai neaktyvus.
-- Naudodami CASE aiškiai parodykite, kur yra aktyvūs klientai, o kur - ne.
select count(*) as Klientų_skaičius, 
case
when active = 1 then 'Aktyvus'
when active = 0 then 'Pasyvus'
end as Aktyvumas 
from customer
group by active;

select rating, group_concat(title separator ';;')
from film
group by rating;
-- simboliu paemimas nuo pirmo po tris
select substring(first_name, 1 , 3) from actor;
-- apatinis apvalinimas
select floor(3/4);
-- virsutinis apvalinimas
select ceil(3/4);

SELECT STR_TO_DATE('Wednesday, 10 February 2021, 12:30:20', '%W, %d %M %Y, %T');
-- jungimas
select last_name, first_name from actor
union all -- su pasikartojančiomis eilutėmis
select last_name, first_name from customer;
-- jungimas
select last_name, first_name from actor
union -- be pasikartojančiu eiluciu
select last_name, first_name from customer;
-- jungimas
select last_name, first_name from actor
union all -- su pasikartojančiomis eilutėmis
select customer_id, email from customer;
-- jungimas butinai vienodai stulpeliu
select last_name, first_name, null from actor
union all -- su pasikartojančiomis eilutėmis
select customer_id, email, last_name from customer;

-- Parašykite SQL užklausą, pateikiančią klientų id, sumokamą
-- mokestį už nuomą. Tuos klientus, kurie sumoka už nuomą vienu
-- kartu virš 10, pažymėkite kaip „Virš 10“, o išleidžiančius iki 10,
-- pažymėkite „Iki 10“. Surūšiuokite pagal nuomos mokestį
-- mažėjimo tvarka. Payment lentele

select customer_id as ID, sum(amount) as Nuomos_mokestis, payment_date as Mok_data,
if(sum(amount)>=10,'Virš 10','Iki 10') as M
from payment
group by ID, payment_date
order by Nuomos_mokestis desc, ID asc;

-- Pateikite klientų sąrašą (lentelė payment) su mokėjimo data ir
-- didžiausiu kiekvieno kliento mokėjimu, bet tik tų klientų,
-- kurių didžiausias mokėjimas tą dieną yra šiame sąraše: 2.99,
-- 3.99 ir 4.99.
select customer_id as ID, MAX(amount) as Max_mokėjimas, date(payment_date) as Data
from payment
group by ID, date(payment_date)
having MAX(amount) in (2.99,3.99,4.99);
-- inner join, left join, right join
select customer.customer_id, first_name, last_name, amount
from payment
inner join customer
on payment.customer_id = customer.customer_id; 
-- trumpiau
select customer.customer_id, first_name, last_name, amount
from payment
inner join customer
using (customer_id);
-- dar trumpiau
select C.customer_id, C.first_name, C.last_name, P.amount
from payment as P
inner join customer as C
using (customer_id);

select C.customer_id, C.first_name, C.last_name, P.amount, S.first_name, S.last_name
from payment as P
inner join customer as C
using (customer_id)
inner join staff as S
using (staff_id)
where P.rental_id between 1 and 11;

-- Kiek kiekvienas darbuotojas surinko klientų apmokėjimų
-- (kiekis, suma)? (staff, payment)
select S.staff_id as ID, S.first_name as Vardas, S.last_name as Pavarde, sum(P.amount) as Suma, count(*) as Kiekis
from payment as P
inner join staff as S
using (staff_id)
group by staff_id;
-- Suraskite, kuriuos klientus kuris darbuotojas aptarnavo?
-- (staff, customer)
select S.first_name as D_vardas, S.last_name as D_pavarde, C.first_name as K_vardas, C.last_name as K_pavarde
from payment as P
inner join customer as C
using (customer_id)
inner join staff as S
using (staff_id)
group by staff_id, customer_id;