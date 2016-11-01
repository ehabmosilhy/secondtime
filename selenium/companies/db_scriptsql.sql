select c1.id , c1.name as comapny_name,c2.name as parent_name   from 
res_company c1
full outer join res_company c2 

on c1.parent_id = c2.id
order by c1.id