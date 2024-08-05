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
having C > 200 and R = 'PG-13';

select count(*), rating from film
group by rating
having avg(length) > 118;

select actor_id, first_name,
case
when actor_id MOD 3 = 0 then 'Dalus iš trijų'
when actor_id MOD 2 = 0 then 'Kažkas'
else "Nelyginis"
end as Lyginumas, last_name
from actor;

select count(*),
case
when actor_id MOD 3 = 0 then 'Dalus iš trijų'
when actor_id MOD 2 = 0 then 'Kažkas'
else "Nelyginis"
end as Lyginumas
from actor
group by Lyginumas;

select actor_id,
if((actor_id % 2) = 0, 'Lyg', 'Nelyg') as IFas
from actor;

select actor_id,
if(actor_id mod 2 = 0, lower(first_name), first_name) as vardas,
case
when actor_id mod 3 = 0 then lower(last_name)
else last_name
end as pavardė
from actor
order by actor_id asc;

select return_date from rental
where return_date like '%-06-%';

select rating, group_concat(title separator ';;')
from film
group by rating;

select substring(first_name, 1, 3) from actor;

select floor(3/4);

select ceil(3/4);

SELECT STR_TO_DATE('Wednesday, 10 February 2021, 12:30:20', '%W, %d %M %Y, %T');


select first_name, last_name from actor
union all
select first_name, last_name from customer;

select customer_id, amount, if(amount > 10, 'Virš 10', 'Iki 10') as C from payment
order by amount desc;

select customer_id, amount, 'virš 10'as C
from payment
where amount > 10
union all
select customer_id, amount, 'Iki 10' from payment
where amount < 10
order by amount desc;

-- Pateikite klientų sąrašą (lentelė payment) su mokėjimo data ir
-- didžiausiu kiekvieno kliento mokėjimu, bet tik tų klientų,
-- kurių didžiausias mokėjimas tą dieną yra šiame sąraše: 2.99,
-- 3.99 ir 4.99.

select customer_id, date(payment_date), max(amount)
from payment
group by customer_id, date(payment_date)
having max(amount) in (2.99,3.99,4.99);

-- inner join, left join, right join
select * from customer limit 2;
select * from payment limit 2;

select customer.customer_id, first_name, last_name, amount
from payment
inner join customer
on payment.customer_id = customer.customer_id;

select C.customer_id, C.first_name, C.last_name, P.amount, S.first_name, S.last_name
from payment as P
inner join customer as C
using (customer_id)
inner join staff as S
using (staff_id)
where P.rental_id between 1 and 11;









