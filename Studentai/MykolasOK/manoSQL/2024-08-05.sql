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


