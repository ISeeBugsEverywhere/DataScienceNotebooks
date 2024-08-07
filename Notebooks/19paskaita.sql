-- • Pateikite adresus su pašto kodais, miesto pavadinimu bei
-- šalimi. (address, city, country)
select address, postal_code, city, country
from address
inner join city using (city_id)
inner join country using (country_id);
-- • Koks vidutinis filmų ilgis pagal kategorijas? (film,
-- film_category, category)

select name, avg(length) from film
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
