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


 
def create_bom(myrecord):
    global indi
    indi+=1
#     if indi <47 :return
    r_id = myrecord['id']
    r_code=myrecord['code']
    r_product_tmpl_name=myrecord['product_tmpl_name']
    r_type=myrecord['type']
    r_name=myrecord['name']
    r_product_name=myrecord['product_name']
       

    print (indi,str(datetime.datetime.now().time()),str(myrecord))
    
    r_product_tmpl_id = api.execute_kw(db, uid, password, 'product.template',    'search',    
                       [[('name','=',r_product_tmpl_name)]])[0]
                       
    r_product_id = api.execute_kw(db, uid, password, 'product.product',    'search',    
                       [[('name_template','=',r_product_tmpl_name)]])[0]

    r_new_name = str(r_id)+ '$$' + r_name
    r=[{
        'code':r_code
        ,'name':r_new_name 
        ,'product_id':r_product_id 
        ,'product_tmpl_id':r_product_tmpl_id
        ,'type':'phantom'
        , 'company_id':False
        }
        ]
    if not myrecord['code']:
        r[0]['code']= 'N'
    product_id= rpc_do('mrp.bom',r,'create')
    
def create_boms():
    global start_time
    start_time=str(datetime.datetime.now().time())
    with open(os.getcwd() +'/data/import_bom.json') as json_data:
        d = json.load(json_data)
        for i in d:
            my_record=''
            my_record=i
            create_bom(my_record)
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
create_boms()
end_time=str(datetime.datetime.now().time())
print ('Started at:'+start_time + '\n'+'Finished at:'+end_time + '\n')

