from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import csv,datetime, time, xmlrpclib,json,os

baseurl = "http://localhost:8069"
username = "admin"
password = "z"
db='a__test_07'


# Selenium - Global Variable
driver = webdriver.Chrome()

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
        
    elif (mycontrol=='href'):
        item="//a[@href='"+ myclass+"']"
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

def create_product(row,myiterator):
    time.sleep(0.9)   
    driver.implicitly_wait(10)
#     row.replace(',')
    print (row,datetime.datetime.now())


        # Create new product
    if myiterator==1:
        btn_create= fetchx('button', 'oe_list_add btn btn-primary btn-sm')
    else:
        btn_create= fetchx('button', 'oe_form_button_create btn btn-default btn-sm')

    btn_create.click()
    time.sleep(0.4)
    driver.implicitly_wait(3)

# Goto first TAB
    
    _tab="href"
    element=fetchx('href', '#notebook_page_5')
    element.click()
    driver.implicitly_wait(3)

# ================= product name  ==================================
    product_name=unicode(row[1].strip() , "utf-8")
    name_ctrl = fetchx('id','oe-field-input-2')
    name_ctrl.clear()
    name_ctrl.send_keys(product_name)
    driver.implicitly_wait(3)
#===================================================================

# ================= Sale OK  =============================
    sale_ok=row[2].strip().lower()
    if sale_ok=="false":   
        chk_sale_ok = fetchx('id', 'oe-field-input-3')
        chk_sale_ok.click()
        
# ================= Purchase OK  =============================
    purchase_ok=row[3].strip().lower() 
    if purchase_ok=="false":   
        chk_purchase_ok = fetchx('id', 'oe-field-input-4')
        chk_purchase_ok.click()

    
# ================= Unit of Measure  =============================
    mychar_old='$'
    mychar_new="'"
    uom=row[4].strip().replace(mychar_old,mychar_new)
    uom_ctrl = fetchx('id','oe-field-input-11')
    uom_ctrl.clear()
    uom_ctrl.send_keys(uom)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, uom))
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
#===================================================================

# ================= Price  =============================
    price=row[5].strip()
    txt_price=fetchx('id', 'oe-field-input-12')
    txt_price.clear()
    txt_price.send_keys(price)

# ================= product Internal Reference  =============================
    internal_reference=row[6].strip() 
    internal_reference_ctrl = fetchx('id','oe-field-input-15')
    internal_reference_ctrl.clear()
    internal_reference_ctrl.send_keys(internal_reference)
    driver.implicitly_wait(3)
#===================================================================

# Go to Sales
    if sale_ok=='true':
        _tab="href"
        element=fetchx('href', '#notebook_page_8')
        element.click()
        driver.implicitly_wait(3)
    
# ================= Pos cat @ sales  ==================================
        pos_cat_full_name=row[7].strip()
        if pos_cat_full_name:
            pos_cat = pos_cat_full_name.split('/')[-1].strip()
            pos_cat_ctrl = fetchx('id','oe-field-input-46')
            pos_cat_ctrl.send_keys(pos_cat)
            try:
                element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.LINK_TEXT, pos_cat_full_name))
                )
            finally:
                pass
            element.click()
            driver.implicitly_wait(3)
#===================================================================


# ================= internal category @ accounting  ==================================
    _tab="href"
    element=fetchx('href', '#notebook_page_9')
    element.click()
    driver.implicitly_wait(3)
#     
    internal_cat_full_name=row[8].strip()
    if internal_cat_full_name:
        internal_cat = internal_cat_full_name.split('/')[-1].strip()
        internal_cat_ctrl = fetchx('id','oe-field-input-51')
        internal_cat_ctrl.clear()
        internal_cat_ctrl.send_keys(internal_cat)
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.LINK_TEXT, internal_cat_full_name))
            )
        finally:
            pass
        element.click()
        driver.implicitly_wait(3)
#===================================================================
    
    btn_save=fetchx('button', 'oe_form_button_save btn btn-primary btn-sm')
    btn_save.click()

def create_products(menu_id,action):
#     driver.implicitly_wait(20)
    time.sleep(2)
    driver.get(navigate('',menu_id,action))
    time.sleep(2)
#     driver.implicitly_wait(20)
    with open('/home/ehab/secondtime/selenium/items/data/import_product.csv', 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            if myiterator>0:
                create_product(row,myiterator)
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

def create_infrastructure():
    
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
#             print (i)
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
#             print (product_category_id_)
    
    #=============================================
    #4. Insert POS Categories
    #=============================================
    
    
    # First delete the default two categories
    _model ='pos.category'
    
    # It's Empty by default
    # rpc_delete(_model , [[_ for _ in range(1,3)]])
    my_record=[]
    new_parents_null =[]
    new_parents_level_1=[]
    with open(os.getcwd() +'/data/data_pos_category.json') as json_data:
        d = json.load(json_data)
        for i in [_ for _ in d if not _["parent_id"]]:
#             print (i)
            my_record=[{"name":i["name"]}]
            pos_category_id = rpc_create('pos.category',my_record )
            new_parents_null.append({"new_id":pos_category_id,"old_id":i["id"]})
        for x in [_ for _ in d if _["parent_id"] in [n["old_id"] for n in new_parents_null]]:
            my_record=[
                {
                    "name":x["name"],
                    "parent_id":[_["new_id"] for _ in new_parents_null if _["old_id"]==x["parent_id"]][0]
                }]
#             print (my_record)
            pos_category_id_ = rpc_create(_model ,my_record )
            new_parents_level_1.append({"new_id":pos_category_id_,"old_id":x["id"]})

        for z in [_ for _ in d if _["parent_id"] in [n["old_id"] for n in new_parents_level_1]]:
            my_record=[
                {
                    "name":z["name"],
                    "parent_id":[_["new_id"] for _ in new_parents_level_1 if _["old_id"]==z["parent_id"]][0]
                }]
#             print (my_record)
            pos_category_id_ = rpc_create(_model ,my_record )

def go_selenium():
    driver.maximize_window()
    driver.get( navigate  (baseurl))
    login(username, password,db)
    print ('started at:', datetime.datetime.now())
    create_products('153','114')

login_rpc(username, password, db)
create_infrastructure()
go_selenium()


