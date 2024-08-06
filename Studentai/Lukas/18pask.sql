-- Kas antro aktoriaus vardą parašykite mažosiomis raidėmis, kas trečio - pavardę.
select actor_id,
CASE
when actor_id MOD 3 = 0 then lower(last_name) else last_name
end as pavarde,
case 
when actor_id MOD 2 =0 then lower(first_name) else first_name
end as vardas
from actor;

select actor_id,
if(actor_id mod 2 = 0, lower(first_name), first_name) as vardas,
case
when actor_id mod 3 = 0 then lower(last_name)
else last_name
end as pavardė
from actor
order by actor_id asc;

-- • Iš lentelės rental išrinkite įrašus, kurių return_date būtų
-- birželio mėnuo.
select * from rental
where return_date between cast('2005-06-01'as DATE) and cast('2005-07-01'as DATE);

select rental_date
from rental
where return_date like '%-06-%';

-- • Suskaičiuokite kiek klientų (lentelė customer) yra aktyvių ir
-- kiek pasyvių. Jei stulpelyje active yra reikšmė 1 - tai aktyvus
-- klientas, o jei 0 - tai neaktyvus. Naudodami CASE aiškiai
-- parodykite, kur yra aktyvūs klientai, o kur - ne.
select count(*),
if (active = 1, 'aktyvus', 'neaktyvus') as aktyvumas
from customer
group by aktyvumas;

select count(*),
case
when active = 1 then 'Taip'
when active = 0 then 'Ne'
end as aktyvumas
from customer
group by aktyvumas;

SELECT STR_TO_DATE('Wednesday, 10 February 2021, 12:30:20', '%W, %d %M %Y, %T');

-- Parašykite SQL užklausą, pateikiančią klientų id, sumokamą
-- mokestį už nuomą. Tuos klientus, kurie sumoka už nuomą vienu
-- kartu virš 10, pažymėkite kaip „Virš 10“, o išleidžiančius iki 10,
-- pažymėkite „Iki 10“. Surūšiuokite pagal nuomos mokestį
-- mažėjimo tvarka. payment lentele
select * from payment limit 5;

select customer_id, amount,
if(amount > 10, 'virs10', 'iki10') as mokejimas
from payment
order by amount desc;

select customer_id, amount, if(amount > 10, 'Virš 10', 'Iki 10') as C from payment
order by amount desc;

select customer_id, amount, 'virš 10'as C from payment
where amount > 10
union all
select customer_id, amount, 'Iki 10' from payment
where amount < 10
order by amount desc;

-- • Pateikite klientų sąrašą (lentelė payment) su mokėjimo data ir
-- didžiausiu kiekvieno kliento mokėjimu, bet tik tų klientų,
-- kurių didžiausias mokėjimas tą dieną yra šiame sąraše: 2.99,
-- 3.99 ir 4.99.
-- date() max(), having saka, in operatorius

select  amount, group_concat(customer_id), count(*), date(payment_date)
from payment
-- where amount in (2.99, 3.99, 4.99)
group by date(payment_date), amount
having MAX(amount) in (2.99, 3.99, 4.99);

select customer_id, date(payment_date), max(amount)
from payment
group by customer_id, date(payment_date)
having max(amount) in (2.99,3.99,4.99);

-- • Kiek kiekvienas darbuotojas surinko klientų apmokėjimų
-- (kiekis, suma)? (staff, payment)
select P.staff_id, sum(P.amount), count(*), S.first_name, S.last_name
from payment as P
join staff as S
on P.staff_id = S.staff_id
group by P.staff_id;

-- • Suraskite, kuriuos klientus kuris darbuotojas aptarnavo?
-- (staff, customer)

select C.first_name, C.last_name, S.staff_id
from customer as C
join staff as S
on C.store_id = S.store_id;





