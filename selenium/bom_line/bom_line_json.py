import csv,datetime, time, xmlrpclib,json,os
# from twisted.test import myrebuilder1
# from gdata.books.service import ACCOUNT_TYPE

baseurl = "http://localhost:8069"
username = "admin"
password = "1"
db='final_database_01'

# Selenium - Global Variable
# driver = webdriver.Chrome()

def login_rpc(_username,_password,_db):
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(baseurl))
#     print (common.version())
    global uid
    uid = common.authenticate(_db, _username, _password, {})
#     print ('uid: ' , str(uid))
    global api
    api = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(baseurl))

def rpc_do(_mymodule,_myrecord,_operation):
    ids=api.execute_kw(db,uid,password,_mymodule,_operation,_myrecord)
#     print ("Module: "+_mymodule + ' ids: ' + str(ids))
    return ids

def create_bom_line(myrecord):
    global indi
    indi+=1
#     if indi <27 :return
    old_bom_id = myrecord['bom_id']
    ingredient_cost = myrecord['ingredient_cost']
    product_name = myrecord['product_name']
    product_qty = myrecord['product_qty']
    product_rounding = myrecord['product_rounding']
    product_uom_name = myrecord['uom_name']
    product_uos = myrecord['product_uos']
    product_uos_qty = myrecord['product_uos_qty']
    sequence = myrecord['sequence']
    reference_id = myrecord['reference_id']
    
    bom_id = api.execute_kw(db, uid, password, 'mrp.bom',    'search',    
                       [[('name','like',str(old_bom_id)+'%')]])[0]
                       
    product_id = api.execute_kw(db, uid, password, 'product.product',    'search',    
                       [[('name_template','=',product_name)]])[0]

    product_tmpl_id = api.execute_kw(db, uid, password, 'product.template',    'search',    
                       [[('name','=',product_name)]])[0]
    
    product_uom = api.execute_kw(db, uid, password, 'product.uom',    'search',    
                       [[('name','=',product_uom_name)]])[0]
                       
    type='phantom'
                

    r=[{
        'bom_id':bom_id
        ,'ingredient_cost':ingredient_cost 
        ,'product_id':product_id
        ,'product_tmpl_id':product_tmpl_id
        ,'product_qty':product_qty
        ,'product_rounding':product_rounding
        ,'product_uom':product_uom
        ,'product_uos':product_uos
        ,'product_uos_qty':product_uos_qty
        ,'type':type
        
        }
        ]
    if not r[0]['product_uos']:
        r[0]['product_uos']=False
    
    if not r[0]['product_uos_qty']:
        r[0]['product_uos_qty']=False
    
    
    
    print (indi, r)
    bom_line_id= rpc_do('mrp.bom',r,'create')
    
def create_bom_lines():
    global start_time
    start_time=str(datetime.datetime.now().time())
    with open(os.getcwd() +'/data/import_bom_line.json') as json_data:
        d = json.load(json_data)
        for i in d:
            my_record=''
            my_record=i
            create_bom_line(my_record)
            '''
            try:
                create_bom(my_record)
            except Exception as e:     # most generic exception you can catch
                with open("/home/ehab/secondtime/bom_import_error.txt", "a") as logf:
                    logf.write(str(indi)+ " " +str(e) + '\n' + str(i) + '\n\n')
                print ('\n' +'Error' , str(i)+  '\n')
            finally:
                pass
            '''
indi=0


login_rpc(username, password, db)
# create_infrastructure()
create_bom_lines()
end_time=str(datetime.datetime.now().time())
print ('Started at:'+start_time + '\n'+'Finished at:'+end_time + '\n')

