select T1.c, T2.auto, T2.badge - T1.c as Delta, T2.badge as Total from 
(
select count(*) as c, gamintojas from TAutos
group by gamintojas order by c desc
) as T1
right join autoNames as T2
on T1.gamintojas = T2.auto
order by Delta desc;