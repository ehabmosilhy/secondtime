select  pt.id 
, pt.name
, pt.sale_ok
, pt.purchase_ok
, pu.name as uom
, pt.list_price, pp.default_code
,case when 
	(select  down2.name  from pos_category as root left outer join pos_category as down1   on down1.parent_id = root.id left outer join pos_category as down2 	on down2.parent_id = down1.id   
	where  down2.id= pt.pos_categ_id) is null 
	then
			(select  concat (root.name ,' / ' ,down1.name  ) 	from pos_category as root left outer join pos_category as down1   on down1.parent_id = root.id left 
			outer join pos_category as down2 	on down2.parent_id = down1.id   
			where  down1.id= pt.pos_categ_id) 
	else
			(select  concat (root.name ,' / ' ,down1.name , ' / ' , down2.name  ) 	from pos_category as root left outer join pos_category as down1   on down1.parent_id = root.id left 
			outer join pos_category as down2 	on down2.parent_id = down1.id   
			where  down2.id= pt.pos_categ_id) 
	end as pos_category
,	(select  concat (root.name ,' / ' ,down1.name  ) 	from product_category as root left outer join product_category as down1   on down1.parent_id = root.id left 
	outer join product_category as down2 	on down2.parent_id = down1.id   
	where  (down1.id= pt.categ_id) 
		) product_category
from product_product pp
inner join product_template pt on pp.product_tmpl_id=pt.id
left join product_uom pu on pt.uom_id=pu.id
left join pos_category pcat on pt.pos_categ_id=pcat.id