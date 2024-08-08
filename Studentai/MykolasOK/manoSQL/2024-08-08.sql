-- DUS2014N ir DUS2018N,
-- suraskite 
-- kiek dalyvavo respondentų iš kiekvienos amžiaus grupės?alter
-- koks buvo vidutinis atlyginimas pagal amžiaus grupę?
-- (4 atskiros SQL užklausos)
-- Parodykite vienoje lentelėje ansktesnius duomenis ir pateikite
-- skirtumus tarp atlyginimų, dalyvių kiekių.

select *, C18-C14 as Δ, A18-A14 as `Δ€`
from
	(select case
	when amzius = '14-19' then '14-29'
	when amzius = '20-29' then '14-29'
	else amzius
	end as Amz,
	count(*) as C14, round(avg(bdu_spalio)/3.4528) as A14
	from DUS2014N
	group by Amz) as T14
join
	(select amzius as Amz, count(*) as C18, round(avg(bdu_spalio)) as A18
	from DUS2018N
	group by amzius) as T18
using (Amz);

-- Po pertraukos

