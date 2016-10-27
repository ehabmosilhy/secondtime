from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import csv, time, xmlrpclib,json,os

baseurl = "http://localhost:8069"
username = "admin"
password = "z"
db='a_wh_pos_05'

# driver.maximize_window()

def navigate(url='',menu='',action=''):
    if menu=='' and action =='' and url!='':
        pass
    else:
        url =baseurl + '/web#menu_id='+menu + '&action='+action
    
    return (url)
            
def fetchx(mycontrol,myclass=''):
#     //div[contains(@class, 'atag') and contains(@class ,'btag')]
    elem=""
    if (mycontrol=='id'):
         elem= driver.find_element(By.ID,myclass)
    elif (mycontrol=='name'):
        elem= driver.find_element(By.NAME,myclass)
    
    elif (mycontrol=='placeholder'):
        item="//input[@placeholder='"+ myclass+"']"
        elem= driver.find_element(By.XPATH,item)
    
    elif (mycontrol=='button_text'):
        item="//button[text()='"+ myclass+"']"
        elem= driver.find_element(By.XPATH,item)
        
    elif (mycontrol=='select_name'):
        elem = Select(driver.find_element_by_name(myclass))
    elif (mycontrol=='select_id'):
        elem = Select(driver.find_element_by_id(myclass))
    else:
        
        x= '//'+mycontrol +"["
        _class=myclass.split(' ')
        indi=0
        for i in _class:
            
            indi+=1
            if indi<=len(_class) and indi>1: x+=' and'
            x+=" contains(@class," 
            x+= "'" + i + "')"
            
        x+="]"
        elem= driver.find_element(By.XPATH,x)
   
    return (elem)
    
def login(username,password,db):
    dbctrl = fetchx('select_name','db').select_by_visible_text(db)

    driver.implicitly_wait(0.5)    
    usercontrol=fetchx('id','login')
    usercontrol.send_keys("admin")
    driver.implicitly_wait(0.5)
    passctrl = fetchx('id','password')
    passctrl.send_keys(password)
    passctrl.submit()

def create_account(row,myiterator):
    time.sleep(0.3)   
    driver.implicitly_wait(10)
#     row.replace(',')
    print (row)


        # Create new Account
    if myiterator==1:
        btn_create= fetchx('button', 'oe_list_add btn btn-primary btn-sm')
    else:
        btn_create= fetchx('button', 'oe_form_button_create btn btn-default btn-sm')
                            

    btn_create.click()
    
    driver.implicitly_wait(3)
# ================= Account Company  ==================================
    account_company=row[6].strip() 
    company_ctrl = fetchx('id','oe-field-input-7')
    company_ctrl.clear()
    company_ctrl.send_keys(account_company)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, account_company))
        
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
#===================================================================

# ================= Account Code  =============================
    account_code=row[0].strip()    
    txt_account_code = fetchx('id', 'oe-field-input-2')
    txt_account_code.send_keys(account_code)

# ================= Account Name  =============================
    account_name=row[1].strip()
    txt_account_name=fetchx('placeholder', 'Account name')
    txt_account_name.send_keys(account_name)
    
# ================= Account Parent  =============================
    if row[2].strip() and row[3].strip():
        account_parent=row[2].strip()+' '+row[3].strip()
    # Check if Parent is not Empty
    
        parent_ctrl = fetchx('id','oe-field-input-3')
        parent_ctrl.send_keys(account_parent)
        print (account_name + '::' + account_parent)
        try:
            element = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.LINK_TEXT, account_parent))
            
            )
        finally:
            pass
        element.click()
    driver.implicitly_wait(3)
#===================================================================


# ================= Account Internal Type  =============================
    internal_type=row[4].strip() 
    internal_type_ctrl = fetchx('select_id','oe-field-input-4')
    internal_type_ctrl.select_by_visible_text(internal_type)
#     try:
#         element = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.LINK_TEXT, account_internal_type))
#         )
#     finally:
#         pass
    driver.implicitly_wait(3)
#===================================================================

# ================= Account Type  ==================================
    account_type=row[5].strip()
    parent_ctrl = fetchx('id','oe-field-input-5')
    parent_ctrl.send_keys(account_type)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, account_type))
        
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
#===================================================================



    
    btn_save=fetchx('button', 'oe_form_button_save btn btn-primary btn-sm')
    btn_save.click()

    driver.get(navigate('',menu_id,action))
    driver.implicitly_wait(2)
    
    with open('/home/ehab/exported_data/companies.csv', 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            if myiterator>0:
                create_company(row[1],row[2],myiterator)
            myiterator+=1

def create_accounts(menu_id,action):
#     driver.implicitly_wait(20)
    time.sleep(2)
    driver.get(navigate('',menu_id,action))
    time.sleep(2)
#     driver.implicitly_wait(20)
    with open('/home/ehab/exported_data/accounts.csv', 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            if myiterator>0:
                create_account(row,myiterator)
            myiterator+=1

def login_rpc(_username,_password,_db):
    common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(baseurl))
#     print (common.version())
    global uid
    uid = common.authenticate(_db, _username, _password, {})
#     print ('uid: ' , str(uid))
    global api
    api = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(baseurl))
    
def rpc_create(_mymodule,_myrecord):
    ids=api.execute_kw(db,uid,password,_mymodule,'create',_myrecord)
#     print ("Module: "+_mymodule + ' ids: ' + str(ids))
    return ids

def rpc_delete(_mymodule,_ids):
    api.execute_kw(db,uid,password,_mymodule,'unlink',[[1,2,3,4,5]])

login_rpc(username, password, db)

#===============================================#
# 1. Create a category with the name 'general'  #
#===============================================#

# Delete the default product
_model ='product.template'
rpc_delete(_model , [[_ for _ in range(1,2)]])

# emtpy the categ table

_model ='product.uom.categ'
rpc_delete(_model , [[_ for _ in range(1,6)]])

my_record=[{'name':'General'}]
category_id= rpc_create('product.uom.categ',my_record )

#=============================================
#2. Insert product_uom
#=============================================
_model ='product.uom'
rpc_delete(_model , [[_ for _ in range(1,20)]])

with open(os.getcwd() +'/data/data_product_uom.json') as json_data:
    d = json.load(json_data)
    for i in d:
        my_record=''
        i['category_id']=category_id
        my_record=[i]
#         print (my_record)
        uom_id = rpc_create(_model,my_record )

#=============================================
#3. Insert product_category
#=============================================

# First delete the default two categories
_model ='product.category'
rpc_delete(_model , [[_ for _ in range(1,3)]])

new_parents =[]
with open(os.getcwd() +'/data/data_product_category.json') as json_data:
    d = json.load(json_data)
    for i in [_ for _ in d if not _["parent_id"]]:
        print (i)
        my_record=[{"name":i["name"]}]
        product_category_id = rpc_create('product.category',my_record )
        new_parents.append({"new_id":product_category_id,"old_id":i["id"]})

    for x in [_ for _ in d if _["parent_id"]]:
        my_record=[
            {
                "name":x["name"],
                "parent_id":[_["new_id"] for _ in new_parents if _["old_id"]==x["parent_id"]][0]
            }]
        product_category_id_ = rpc_create(_model ,my_record )
        print (product_category_id_)

#=============================================
#4. Insert POS
#=============================================
'''
# First delete the default two categories
_model ='pos.category'

# It's Empty by default
# rpc_delete(_model , [[_ for _ in range(1,3)]])
my_record=[]
new_parents =[]
with open(os.getcwd() +'/data/data_pos_category.json') as json_data:
    d = json.load(json_data)
    for i in [_ for _ in d if not _["parent_id"]]:
        print (i)
        my_record=[{"name":i["name"]}]
        pos_category_id = rpc_create('pos.category',my_record )
        new_parents.append({"new_id":pos_category_id,"old_id":i["id"]})

    for x in [_ for _ in d if _["parent_id"]]:
        my_record=[
            {
                "name":x["name"],
                "parent_id":[_["new_id"] for _ in new_parents if _["old_id"]==x["parent_id"]][0]
            }]
        print (my_record)
        pos_category_id_ = rpc_create(_model ,my_record )
        
#         print (pos_category_id_)
   '''     



'''
driver = webdriver.Chrome()
login(username, password,db)
driver.get( navigate  (baseurl))
'''

# create_accounts('175','173')

    


