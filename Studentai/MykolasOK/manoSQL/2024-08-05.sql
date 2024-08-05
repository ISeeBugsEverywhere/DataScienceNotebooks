select actor_id as ID,
	CASE
		when actor_id MOD 100 = 0 then 'Šimtinis'
		when actor_id MOD 10 = 0 then 'Dešimtinis'
		when actor_id MOD 2 = 0 then 'Lyginis'
		else 'Nelyginis'
	END AS Lyginumas, first_name, last_name 
	from actor
	order by ID asc;
	
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

select MONTH(return_date) from rental;

select * from rental
	WHERE MONTH(return_date)=6;

-- Suskaičiuokite kiek klientų (lentelė customer) yra aktyvių ir kiek pasyvių. 
-- Jei stulpelyje active yra reikšmė 1 - tai aktyvus klientas, o jei 0 - tai neaktyvus. 
-- Naudodami CASE aiškiai parodykite, kur yra aktyvūs klientai, o kur - ne.

select count(*),
	case
		when active = 0 then 'Pasyvus'
		else 'Aktyvus'
	end as aktyvumas
	from customer group by active ;

SELECT rating, GROUP_CONCAT(title separator ', ') 
	from film 
	group by rating;

SELECT SUBSTRING(first_name, 1, 3) from actor;

SELECT first_name, last_name from actor a 
	union all
SELECT first_name, last_name from customer c; 

SELECT first_name, last_name, 'actor' from actor a 
	union all
SELECT first_name, last_name, 'customer' from customer c; 

-- Parašykite SQL užklausą, pateikiančią klientų id, sumokamą mokestį už nuomą. 
-- Tuos klientus, kurie sumoka už nuomą vienu kartu virš 10, pažymėkite kaip „Virš 10“, 
-- o išleidžiančius iki 10, pažymėkite „Iki 10“. Surūšiuokite pagal nuomos mokestį mažėjimo tvarka.

SELECT customer_id, amount,
	IF (amount>10,'Virš 10','Iki 10') as ar_brangiai
	from payment
	WHERE amount>0
	order by amount DESC ;

-- Pateikite klientų sąrašą (lentelė payment) su mokėjimo data 
-- ir didžiausiu kiekvieno kliento mokėjimu, 
-- bet tik tų klientų, kurių didžiausias mokėjimas tą dieną yra šiame sąraše: 2.99, 3.99 ir 4.99.
-- Galima naudoti: in, having, date(), max()

SELECT date(payment_date), customer_id, MAX(amount) as did 
	from payment
	group by date(payment_date), customer_id
	having did IN( 2.99, 3.99, 4.99 );

