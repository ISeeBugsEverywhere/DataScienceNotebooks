select actor_id as id,
	case
		when actor_id MOD 100 = 0 then 'Šimtinis'
		when actor_id MOD 10 = 0 then 'Dešimtinis'
		when actor_id MOD 2 = 0 then 'Lyginis'
		else 'Nelyginis'
	end as Lyginumas, first_name, last_name 
	from actor
	order by id asc;
	
Kas antro aktoriaus vardą parašykite mažosiomis raidėmis, 
kas trečio - pavardę.

select actor_id as id,
	if(actor_id mod 2 = 0, lower(first_name), first_name) as vardas,
	case
		when actor_id mod 3 = 0 then lower(last_name)
		else last_name
	end as pavardė
	from actor
	order by id asc;

select actor_id as id,
	if(actor_id mod 2 = 0, lower(first_name), first_name) as vardas,
	if(actor_id mod 3 = 0, lower(last_name), last_name) as pavardė
	from actor
	order by id;
	
-- Iš lentelės rental išrinkite įrašus, kurių return_date būtų birželio mėnuo.

select month(return_date) from rental;

select * from rental
	where month(return_date)=6;

-- Suskaičiuokite kiek klientų (lentelė customer) yra aktyvių ir kiek pasyvių. 
-- Jei stulpelyje active yra reikšmė 1 - tai aktyvus klientas, o jei 0 - tai neaktyvus. 
-- Naudodami CASE aiškiai parodykite, kur yra aktyvūs klientai, o kur - ne.

select count(*),
	case
		when active = 0 then 'Pasyvus'
		else 'Aktyvus'
	end as aktyvumas
	from customer group by active ;

select rating, group_concat(title separator ', ') 
	from film 
	group by rating;

select substring(first_name, 1, 3) from actor;

select first_name, last_name from actor
	union all
select first_name, last_name from customer; 

select first_name, last_name, 'actor' from actor
	union all
select first_name, last_name, 'customer' from customer
	order by last_name, first_name; 

-- Parašykite SQL užklausą, pateikiančią klientų id, sumokamą mokestį už nuomą. 
-- Tuos klientus, kurie sumoka už nuomą vienu kartu virš 10, pažymėkite kaip „Virš 10“, 
-- o išleidžiančius iki 10, pažymėkite „Iki 10“. Surūšiuokite pagal nuomos mokestį mažėjimo tvarka.

select customer_id, amount,
	if (amount>10,'virš 10','iki 10') as ar_brangiai
	from payment
	where amount>0
	order by amount desc ;

-- Pateikite klientų sąrašą (lentelė payment) su mokėjimo data 
-- ir didžiausiu kiekvieno kliento mokėjimu [tą dieną], 
-- bet tik tų klientų, kurių didžiausias mokėjimas tą dieną yra šiame sąraše: 2.99, 3.99 ir 4.99.
-- Rekomenduojama naudoti: having, in(), date(), max()

select customer_id, date(payment_date), max(amount) as didelis
	from payment
	group by date(payment_date), customer_id
	having didelis in( 2.99, 3.99, 4.99 )
	order by payment_date, customer_id;

-- Kitų studentų bandymas - naudoja 'where' prieš grupavimą.
-- Neeatitinka užduoties sąlygos, 
-- nes leidžia tuos, kur didžiausias mokėjimas ne iš sąrašo:
select customer_id, date(payment_date), max(amount) as didelis
	from payment
	where amount in( 2.99, 3.99, 4.99 )
	group by date(payment_date), customer_id
	order by payment_date, customer_id;

-- Tema: 'join'

select * from customer;
select * from payment;

select first_name, last_name, amount
	from payment p
	inner join customer c
	on p.customer_id=c.customer_id;

select customer_id, first_name, last_name, amount
	from payment as p
	inner join customer as c
	using (customer_id);

select customer_id as id, first_name as `First name`, last_name as `Last name`, amount as Amount
	from payment as p
	inner join customer as c
	using (customer_id)
	where amount>10;

select customer_id id, first_name `First name`, last_name `Last name`, amount Amount
	from payment p
	inner join customer c
	using (customer_id)
	where amount>10
	order by last_name;

-- Kiek kiekvienas darbuotojas surinko klientų apmokėjimų (kiekis, suma)? 
-- [lentelės] (staff, payment)

select sum(p.amount), count(p.amount), st.first_name, st.last_name
	from staff st
	left join payment p
	using (staff_id)
	group by st.staff_id;

-- Suraskite, kuriuos klientus kuris darbuotojas aptarnavo?
-- [lentelės] (staff, customer)

select	st.first_name `St. first`, st.last_name `St. last`,
		c.first_name `Cust. first`, c.last_name `Cust. last`
	from staff st
	left join customer c
	using (store_id)
	order by c.last_name, c.first_name;

