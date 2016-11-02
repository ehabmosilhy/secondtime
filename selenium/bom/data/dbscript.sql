select
	b.id
	 ,b.code
	 ,product_qty
	, uom.name as product_uom_name
	, b.product_uom
	, b.product_qty
	, b.product_tmpl_id
	, t.name as product_tmpl_name
	, b."type"
	, b."name"
	, b.product_id
	, p.name_template as product_name
FROM public.mrp_bom b
left join product_uom uom on b.product_uom = uom.id 
left join product_template t on b.product_tmpl_id = t.id 
left join product_product p on b.product_id = p.id
--where b.id  =216