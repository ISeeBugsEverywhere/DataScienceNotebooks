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
	
