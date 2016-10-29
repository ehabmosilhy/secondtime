--select * from product_uom_categ order by id
--select * from product_uom order by id 
select p.id,p.name,pp.name  from product_category p inner join product_category pp on p.parent_id=pp.id  order by p.name