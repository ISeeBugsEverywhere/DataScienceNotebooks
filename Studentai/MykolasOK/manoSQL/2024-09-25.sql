SELECT gamintojas, count(*) n, GROUP_CONCAT(cast(replace(price,' ','') as float)) kainos
    FROM works.autopliuslt 
    GROUP BY gamintojas
    order by n desc limit 10;

# 2025-09-25 pirmosios užduoties pirmoji dalis - duomenų gavimas:
# Atrinkti 10 populiariausių gamintojų iš autopliuslt, 
# pateikti tokius stulpelius - gamintojas, vidutinė kaina, vidutinė rida, vidutinis amžius, modelių kiekis. 

SELECT 	gamintojas, 
		ROUND(AVG(cast(replace(price,' ','') as float))) kaina,
		ROUND(AVG(cast(replace(replace(rida,' ',''),'km','') as float))) r,
		ROUND(AVG(cast(pagaminimo_data) as float)) data,
		pagaminimo_data,
		count(*) n
    FROM works.autopliuslt 
    GROUP BY gamintojas
    order by n desc limit 10;