param = objects.execute_kw(db, uid, pwd, 'sale.order', 'create', [
    {'partner_id' :customer_ids[0].get('id'),
     'validity_date':datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
     'order_line': {'product_id':product2_ids[0].get('id'), 'name':'test', 'product_uom_qty':10, 'price_unit':30000}}])
objects.execute_kw(db, uid, pwd, 'sale.order.line', 'create', [
    {'order_id' :param, 'product_id':product_ids[0].get('id'),
     'name':'test2', 'product_uom':product_ids[0].get('uom_id')[0], 'product_uom_qty':20, 'price_unit':50000, 'price_total':1000000}])
objects.execute_kw(db, uid, pwd, 'sale.order.line', 'create', [
    {'order_id' :param, 'product_id':product2_ids[0].get('id'),
     'name':'test45', 'product_uom':product2_ids[0].get('uom_id')[0], 'product_uom_qty':10, 'price_unit':50000, 'price_total':5000000}])
salesorder = objects.execute_kw(db, uid, pwd, 'sale.order', 'search', [[['id', '=', param]]])
print objects.execute_kw(db, uid, pwd, 'sale.order', 'read', [salesorder], {'fields':
                                                                      ['name',
                                                                       'id',
                                                                       'order_line']})
