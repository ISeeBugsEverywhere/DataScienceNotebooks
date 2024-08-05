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





