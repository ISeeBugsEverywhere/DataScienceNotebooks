
(select avg(du.bdu_spalio) viddu, p.Kodas, p.Profesija, 'Didžiausi' tmp
from DUS2014N du
left join profesijos p
on du.profesija=p.Kodas
group by p.Kodas
order by viddu desc
limit 3)
	union all
(select avg(du.bdu_spalio) viddu, p.Kodas, p.Profesija,
abs(avg(du.bdu_spalio)-(select avg(du.bdu_spalio) from DUS2014N du)) skirtumas
from DU8S2014N du
left join profesijos p
on du.profesija=p.Kodas
group by p.Kodas
order by skirtumas asc
limit 3)
	union all
(select avg(du.bdu_spalio) viddu, p.Kodas, p.Profesija, 'Mažiausi' tmp
from DUS2014N du
left join profesijos p
on du.profesija=p.Kodas
group by p.Kodas
order by viddu asc
limit 3);

-- Pokytis 2014..2018:

select * from 
(select * from 
(select avg(du.bdu_spalio) viddu, p.Kodas, p.Profesija, 'Didžiausi'
from DUS2014N du
left join profesijos p
on du.profesija=p.Kodas
group by p.Kodas
order by viddu desc
limit 5) as t1
	union all
select * from
(select avg(du.bdu_spalio) viddu, p.Kodas, p.Profesija,
abs(avg(du.bdu_spalio)-(select avg(du.bdu_spalio) from DUS2014N du)) skirtumas
from DUS2014N du
left join profesijos p
on du.profesija=p.Kodas
group by p.Kodas
order by skirtumas asc
limit 5) as t2
	union all
select * from
(select avg(du.bdu_spalio) viddu, p.Kodas, p.Profesija, 'Mažiausi'
from DUS2014N du
left join profesijos p
on du.profesija=p.Kodas
group by p.Kodas
order by viddu asc
limit 5) as t3) as du14
left join DUS2018N du18 on du18.profesija=du14.Kodas
order by viddu asc;
