
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
from DUS2014N du
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
