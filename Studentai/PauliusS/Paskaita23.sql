# Raskite 5 top 2014 metais apmokamas specialybes, atvaizduokite jų vidutinį atlyginimą stulpeline diagrama (bar arba barh).
# Raskite 5 mažiausiai apmokamas specialybes 2014 metais, atvaizduokite jų vidutinį atlyginimą su bar arba barh.
# Raskite 5 vidutiniškai apmokamas specialybes (0.9-1.1 VDU, imate arčiausiai 1.1 VDU esančias), atvaizduojate vidutinius 
# atlyginimas su bar arba barh.
# Tada surandate šių 15-kos specialybių atlyginimų pokytį tarp 2014 ir 2018 metų, pokytį vizualizuokite su bar arba barh. 
# Kokios specialybėsm tas pokytis didžiausias?



SELECT 
    atlyginimai.profesija, atlyginimai.atlyg, kita_lentele.kitas, round(((kita_lentele.kitas - atlyginimai.atlyg)/atlyginimai.atlyg*100), 2) as Procentai, trecia_lentele.Profesija
FROM 
    (
        (SELECT profesija, AVG(bdu_spalio / 3.456) AS atlyg
        FROM DUS2014N
        GROUP BY profesija
        ORDER BY AVG(bdu_spalio / 3.456) DESC
        LIMIT 5)

        UNION ALL

        (SELECT profesija, AVG(bdu_spalio / 3.456) AS atlyg
        FROM DUS2014N
        GROUP BY profesija
        ORDER BY AVG(bdu_spalio / 3.456) ASC
        LIMIT 5)

        UNION ALL

        (SELECT profesija, AVG(bdu_spalio / 3.456) AS atlyg
        FROM DUS2014N
        GROUP BY profesija
        HAVING AVG(bdu_spalio / 3.456) BETWEEN 
            (SELECT AVG(bdu_spalio / 3.456) * 0.9 FROM DUS2014N) AND 
            (SELECT AVG(bdu_spalio / 3.456) * 1.1 FROM DUS2014N)
        ORDER BY AVG(bdu_spalio / 3.456)
        LIMIT 5)
    ) AS atlyginimai
JOIN 
    (
        SELECT profesija, AVG(bdu_spalio) AS kitas 
        FROM DUS2018N
        GROUP BY profesija
    ) AS kita_lentele
ON 
    atlyginimai.profesija = kita_lentele.profesija  
JOIN 
	(
		SELECT * from profesijos
	) AS trecia_lentele
ON atlyginimai.profesija = trecia_lentele.Kodas;
        


-- LENTELE IS DVIEJU EILUCIU 

SELECT 
    round(((kita_lentele.kitas - atlyginimai.atlyg)/atlyginimai.atlyg*100), 2) as Procentai, trecia_lentele.Profesija
FROM 
    (
        (SELECT profesija, AVG(bdu_spalio / 3.456) AS atlyg
        FROM DUS2014N
        GROUP BY profesija
        ORDER BY AVG(bdu_spalio / 3.456) DESC
        LIMIT 5)

        UNION ALL

        (SELECT profesija, AVG(bdu_spalio / 3.456) AS atlyg
        FROM DUS2014N
        GROUP BY profesija
        ORDER BY AVG(bdu_spalio / 3.456) ASC
        LIMIT 5)

        UNION ALL

        (SELECT profesija, AVG(bdu_spalio / 3.456) AS atlyg
        FROM DUS2014N
        GROUP BY profesija
        HAVING AVG(bdu_spalio / 3.456) BETWEEN 
            (SELECT AVG(bdu_spalio / 3.456) * 0.9 FROM DUS2014N) AND 
            (SELECT AVG(bdu_spalio / 3.456) * 1.1 FROM DUS2014N)
        ORDER BY AVG(bdu_spalio / 3.456)
        LIMIT 5)
    ) AS atlyginimai
JOIN 
    (
        SELECT profesija, AVG(bdu_spalio) AS kitas 
        FROM DUS2018N
        GROUP BY profesija
    ) AS kita_lentele
ON 
    atlyginimai.profesija = kita_lentele.profesija  
JOIN 
	(
		SELECT * from profesijos
	) AS trecia_lentele
ON atlyginimai.profesija = trecia_lentele.Kodas
ORDER BY Procentai DESC;

---------------------------------------------------------------------------

SELECT 
    CASE 
        WHEN Plotas >= 5 AND Plotas < 10 THEN '5-10'
        WHEN Plotas >= 10 AND Plotas < 20 THEN '10-20'
        WHEN Plotas >= 20 AND Plotas < 30 THEN '20-30'
        WHEN Plotas > 30 THEN 'daugiau 30'
        ELSE 'kita'
    END AS Plotas_ABC,
    AVG(`€/S`) AS Vidurkis
FROM aruodas
GROUP BY Plotas_ABC
ORDER BY Plotas_ABC ASC;


-- -----------------------------------------------------------------------------

SELECT Kambariai, round(AVG(`€/S`)) from aruodas
group by Kambariai;












