import csv,datetime, time, xmlrpclib,json,os
# from twisted.test import myrebuilder1
# from gdata.books.service import ACCOUNT_TYPE

baseurl = "http://localhost:8069"
username = "admin"
password = "1"
db='final_database_01'

def login_rpc(_username,_password,_db):
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(baseurl))
    global uid
    uid = common.authenticate(_db, _username, _password, {})
    global api
    api = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(baseurl))

def rpc_do(_mymodule,_myrecord,_operation):
    ids=api.execute_kw(db,uid,password,_mymodule,_operation,_myrecord)
    return ids

indi=0
def create_account(myrecord):
    global indi
    indi+=1
    print (indi, myrecord)
    
    # Get all data about the imported account 
    
    ac_name= myrecord['account_name']
    ac_code=str(myrecord['account_code'])
    ac_internal_type=myrecord['internal_type']
    ac_user_type=myrecord['account_type']
    
    ac_company_name=myrecord['company_name']
    ac_company_id = api.execute_kw(db, uid, password, 'res.company','search',  [[('name','=',ac_company_name)]])[0]
    
    ac_parent_name=myrecord['parent_name']
    
    ac_account_type=myrecord['account_type']    
    ac_user_type_id = api.execute_kw(db, uid, password, 'account.account.type','search',[[('name','=',ac_account_type)]])
    
    ac_parent_code =  str(myrecord['parent_code'])
    
    if ac_parent_code:
        ac_parent_id = api.execute_kw(db, uid, password, 'account.account','search',  
                                  [[('code','=',ac_parent_code),('company_id','=',ac_company_id)]])

    ac_account_id = api.execute_kw(db, uid, password, 'account.account','search',    
        [[('code','=',ac_code), ('company_id','=',ac_company_id)]])
    
    # if the imported account exists and has the code 0, 1 or 2 change only its name 
    if ac_account_id:
        if ac_code in ['0','1','2']:
            # Change name only
            
            api.execute_kw(db,uid,password,'account.account','write',[[ac_account_id[0]],
                                                                      {'name':ac_name
                                                                       }])
        else:
            
            api.execute_kw(db,uid,password,'account.account','write',[[ac_account_id[0]],
                                                                      {'name':ac_name
                                                                       ,'type':ac_internal_type
                                                                       , 'user_type': ac_user_type_id[0]
                                                                       }])
    else:
    # if the imported acccount does not exist 
    # we will insert it 
    # but if it's parent exists with a different name, we change the parent name
        if ac_parent_id:
            api.execute_kw(db,uid,password,'account.account','write',[[ac_parent_id[0]],
                                                                          {'name':ac_parent_name
                                                                           }])
            
        r=[{'name':ac_name 
        ,'code':ac_code
        , 'type': ac_internal_type
        , 'user_type': ac_user_type_id[0]
        , 'company_id': ac_company_id
        , 'parent_id':ac_parent_id[0]
        }
        ]
        print (r)
        if not r[0]['parent_id']:
            r[0]['parent_id']=False
        account_id= rpc_do('account.account',r,'create')
       
def create_accounts():
    with open('/home/ehab/secondtime/selenium/accounts/data/import_accounts.json') as json_data:
        d = json.load(json_data)
        logf = open("/home/ehab/secondtime/selenium/accounts/accounts_error_log.txt", "w")
        for i in d:
            my_record=''
            my_record=i
            
            create_account(my_record)
#             try:
#                 create_account(my_record)
#             except Exception as e:     # most generic exception you can catch
#                 logf.write(str(e) + '\n' + str(i) + '\n')
#                 print ('Error' , str(i))
#             finally:
#                 pass

login_rpc(username, password, db)
create_accounts()

