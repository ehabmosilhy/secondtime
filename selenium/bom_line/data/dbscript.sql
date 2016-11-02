SELECT 
 l.bom_id
, l.ingredient_cost
,p.name_template as product_name --, l.product_id
, l.product_qty
, l.product_rounding
, u.name as uom_name  --, l.product_uom
, l.product_uos
, l.product_uos_qty
, l."type"
, l."sequence"
, l.reference_id
FROM 
mrp_bom_line l
inner join product_product p on p.id = l.product_id
left join product_uom u on l.product_uom = u.id
