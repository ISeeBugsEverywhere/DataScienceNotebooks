-- Paskutinės dvi vakarykštės užduotys:
-- (1) Kiek kiekvienas darbuotojas surinko klientų apmokėjimų (kiekis, suma)? 
-- [lentelės] (staff, payment)

select count(p.amount), sum(p.amount), st.first_name, st.last_name
	from staff st
	left join payment p
	using (staff_id)
	group by st.staff_id;

-- (2) Suraskite, kuriuos klientus kuris darbuotojas aptarnavo?
-- [lentelės] (staff, customer)

select	st.first_name `St. first`, st.last_name `St. last`,
		c.first_name `Cust. first`, c.last_name `Cust. last`
	from staff st
	left join customer c
	using (store_id)
	order by c.last_name, c.first_name;

-- (2M) Visi vardai ir pavardės taisyklingai iš didžiosios:

select
	CONCAT(
        UPPER(SUBSTRING(st.first_name, 1, 1)),
        LOWER(SUBSTRING(st.first_name, 2, LENGTH(st.first_name)))
    ) AS `Staff first n.`, 
	CONCAT(
        UPPER(SUBSTRING(st.last_name, 1, 1)),
        LOWER(SUBSTRING(st.last_name, 2, LENGTH(st.last_name)))
    ) AS `Staff last n.`,
	CONCAT(
        UPPER(SUBSTRING(c.first_name, 1, 1)),
        LOWER(SUBSTRING(c.first_name, 2, LENGTH(c.first_name)))
    ) AS `Customer first n.`, 
	CONCAT(
        UPPER(SUBSTRING(c.last_name, 1, 1)),
        LOWER(SUBSTRING(c.last_name, 2, LENGTH(c.last_name)))
    ) AS `Customer last n.`
	from staff st
	left join customer c
	using (store_id)
	order by c.last_name, c.first_name;

------------------- Nauja paskaita: -------------------

-- 1. Pateikite adresus su pašto kodais, miesto pavadinimu bei šalimi. 
-- (address, city, country)

select address.address, address.address2, address.postal_code , city.city, country.country
	from address
	left join city using( city_id )
	left join country using( country_id );
	
-- 2. Koks vidutinis filmų ilgis pagal kategorijas?
-- (film, film_category, category)

select AVG(film.length), category.name 
	from film
	right join film_category using( film_id )
	left join category using( category_id )
	group by category_id;

-- 3. Kiek klientė Amy Lopez sumokėjo už filmo Rocky War nuomą?
-- (customer, payment, rental, inventory, film)

select payment.amount 
	from customer
	join payment using( customer_id )
	join rental using( rental_id )
	join inventory using( inventory_id )
	join film using( film_id )
	where customer.first_name like 'Amy' and customer.last_name like 'Lopez'
		and film.title like 'Rocky War'
	order by payment.payment_date DESC;

-- 4. Kada paskutinį kartą ir kiek sumokėjo klientė BETTY WHITE?
-- (payment, customer)

select payment.amount 
	from payment
	right join customer using( customer_id )
	where customer.first_name like 'BETTY' and customer.last_name like 'WHITE'
	order by payment.payment_date desc
	limit 1;

-- 5. Parašykite SQL užklausą, suteikiančią klientų vardus, pavardes,
-- jų iš viso nuomai išleidžiamą sumą (stulpelyje „Iš viso“), 
-- stulpelyje „Rėžiai“ pateikite suskirstytus klientus tokiu būdu:
-- klientus, kurie iš viso nuomai išleidžia 100 ir daugiau,
-- pažymėkite kaip „Virš 100“,
-- išleidžiančius iki 100 pažymėkite „Iki 100“.
-- (customer, payment)

select	customer.first_name, customer.last_name, 
		sum(payment.amount) as `Iš viso`,
		if(sum(payment.amount)>100,'Virš 100','Iki 100') as `Rėžiai`
	from customer
	left join payment using(customer_id)
	group by customer.customer_id;

------------------- -------------------
