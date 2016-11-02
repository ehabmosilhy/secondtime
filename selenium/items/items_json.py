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


 
def create_product(myrecord):
    global indi
    indi+=1
#     if indi not in [1917,2297]:return
    r_name= myrecord['name']
    my_category= myrecord['product_category']
    print (indi,str(datetime.datetime.now().time()),str(myrecord))
      
    #====================================
    #        INTERNAL CATEGORY 
    #===================================
      
    if my_category:
        _category=[_.strip() for _ in  myrecord['product_category'].split('/')]
    else:
        _category=['Inventory Items']
      
    if len(_category) ==1:
        categ_id = api.execute_kw(db, uid, password, 'product.category',    'search',    
                       [[('name','=',_category[0]),('parent_id','=',False)]])[0]
    elif len(_category) ==2:
        root_name=_category[0]
        root_id = api.execute_kw(db, uid, password, 'product.category', 'search',
                                  [[('name','=',root_name),('parent_id','=',False)]])[0]
          
        categ_id = api.execute_kw(db, uid, password, 'product.category',    'search',    
                        [[('name','=',_category[1]),('parent_id','=',root_id)]])[0]
        x=categ_id
    else:
        root_id = api.execute_kw(db, uid, password, 'product.category',    'search',    
                       [[('name','=',_category[0]),('parent_id','=',False)]])[0]
        parent_id = api.execute_kw(db, uid, password, 'product.category',    'search',    
                        [[('name','=',_category[1]),('parent_id','=',root_id)]])[0]
          
        categ_id = api.execute_kw(db, uid, password, 'product.category',    'search',    
                        [[('name','=',_category[1]),('parent_id','=',parent_id)]])[0]
    r_categ_id=categ_id
       
    #====================================
    #        UNIT OF MEASURE 
    #===================================
    uom_id = api.execute_kw(db, uid, password, 'product.uom','search',    
                       [[('name','=',myrecord['uom'])]])[0]
      
    #===========================================================================
      
      
    #====================================
    #        PURCHASE UNIT OF MEASURE 
    #===================================
    purchase_uom_id = api.execute_kw(db, uid, password, 'product.uom','search',    
                       [[('name','=',myrecord['purchase_uom'])]])[0]
      
    #===========================================================================
    sale_ok=myrecord['sale_ok'] if myrecord['sale_ok'] else False
    purchase_ok=myrecord['purchase_ok'] if myrecord['purchase_ok'] else False
    list_price =  myrecord['list_price'] if myrecord['list_price'] else 0
      
    r=[{'name':r_name 
        ,'categ_id':r_categ_id
        , 'uom_id':uom_id
        , 'sale_ok': sale_ok
        , 'purchase_ok': purchase_ok
        , 'list_price': list_price
        , 'uom_po_id':purchase_uom_id
        , 'company_id':False
        }
        ]
    if myrecord['default_code']:
        r[0]['default_code']= myrecord['default_code']
    product_id= rpc_do('product.product',r,'create')
    
def create_products():
    global start_time
    start_time=str(datetime.datetime.now().time())
    with open(os.getcwd() +'/data/json/import_products.json') as json_data:
        d = json.load(json_data)
        for i in d:
            my_record=''
            my_record=i
            try:
                create_product(my_record)
            except Exception as e:     # most generic exception you can catch
                with open("/home/ehab/secondtime/items_import_error.txt", "a") as logf:
                    logf.write(str(indi)+ " " +str(e) + '\n' + str(i) + '\n\n')
                print ('\n' +'Error' , str(i)+  '\n')
            finally:
                pass
indi=0


login_rpc(username, password, db)
# create_infrastructure()
create_products()
end_time=str(datetime.datetime.now().time())
print ('Started at:'+start_time + '\n'+'Finished at:'+end_time + '\n')

