select  Gamintojas, round(avg(2024-substring(pagaminimo_data,1,4)),0) as amzius, round(avg(cast(replace(price,' ','') as float)),0) as Kaina, round(avg(cast(replace(replace(rida,' ',''),'km','')as float)),0) as Rida, count(*) as Kiekis  from autopliuslt
where Rida <> 'Nenurodyta'
group by Gamintojas
order by Kiekis desc
limit 10;