from selenium import webdriver
import csv
import time,os
#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

baseurl = "http://localhost:8069"
username = "admin"
password = "1"
db='db_final_01'


driver = webdriver.Chrome()
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
    
driver.get( navigate  (baseurl))
login(username, password,db)


def create_account(row,myiterator):
    time.sleep(0.7)   
    driver.implicitly_wait(10)
#     row.replace(',')
    print (row)

        # Create new Account
    try:
        btn_create= fetchx('button', 'oe_list_add btn btn-primary btn-sm')
        btn_create.click()
    except:
        btn_create= fetchx('button', 'oe_form_button_create btn btn-default btn-sm')
        btn_create.click()
   
    
    driver.implicitly_wait(3)
# ================= Account Company  ==================================
    account_company=row[6].strip() 
    company_ctrl = fetchx('id','oe-field-input-7')
    time.sleep(0.2)
    company_ctrl.clear()
    time.sleep(0.3)
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
    print ("'" + internal_type + "'")
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
    
    try:
        btn_ok=fetchx('button', 'oe_button oe_form_button')
        btn_ok.click()
        
    
        element_discard = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Discard')))
        
        element_discard.click()   
        alert = driver.switch_to_alert()
        alert.accept()
        with open('/home/ehab/secondtime/output.txt', 'a') as f:
            f.write(str(row) + '\n')

        
#         time.sleep(1)
#         btn_ok=fetchx('button', 'oe_button oe_form_button')
#         btn_ok.click()
    except:
        pass
    

def create_company(company_name,company_parent,myiterator):

    time.sleep(1)    

        # Create new Account
    if myiterator==1:
        btn_create= fetchx('button', 'oe_list_add btn btn-primary btn-sm')
    else:
        btn_create= fetchx('button', 'oe_form_button_create btn btn-default btn-sm')
                            

    btn_create.click()
    
    driver.implicitly_wait(3)
    # //txt_account_name=fetchx('placeholder','Account name')
    
    txt_company_name = fetchx('id', 'oe-field-input-2')
    txt_company_name.send_keys(company_name)
    
    company_parent_ctrl = fetchx('id','oe-field-input-3')
    company_parent_ctrl.send_keys(company_parent)
    
    # This is for selecting items from Odoo's drop down lists which are not really dropdown
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, company_parent))
        
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
    
    btn_save=fetchx('button', 'oe_form_button_save btn btn-primary btn-sm')
    btn_save.click()

def create_companies(menu_id,action):
    time.sleep(2)
    driver.get(navigate('',menu_id,action))
    os.chdir('../data/')
    myfile = os.getcwd() +'/import_companies.csv'
    print (myfile)
    with open(myfile, 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            if myiterator>0:
                create_company(row[1],row[2],myiterator)
            myiterator+=1

def create_accounts(menu_id,action):
#     driver.implicitly_wait(20)
    time.sleep(1)
    driver.get(navigate('',menu_id,action))
    time.sleep(0.8)
#     driver.implicitly_wait(20)
    with open('../data/import_accounts.csv', 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            if myiterator>0:
                create_account(row,myiterator)
            myiterator+=1


# create_companies('62','51')
create_accounts('175','173')

    


