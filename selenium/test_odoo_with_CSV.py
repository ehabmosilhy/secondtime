from selenium import webdriver
import csv
import time
#Following are optional required
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

baseurl = "http://localhost:8069"
username = "admin"
password = "z"
db='demo_02'


driver = webdriver.Chrome()
driver.maximize_window()

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
    
driver.get( navigate  (baseurl))
login(username, password,db)


def create_account(row,myiterator):

    driver.implicitly_wait(10)


        # Create new Account
    if myiterator==0:
        btn_create= fetchx('button', 'oe_list_add btn btn-primary btn-sm')
    else:
        btn_create= fetchx('button', 'oe_form_button_create btn btn-default btn-sm')
                            

    btn_create.click()
    
    driver.implicitly_wait(3)

# ================= Account Code  =============================
    account_code=row[0]    
    txt_account_code = fetchx('id', 'oe-field-input-2')
    txt_account_code.send_keys(account_code)

# ================= Account Name  =============================
    account_name=row[1]
    txt_account_name=fetchx('placeholder', 'Account name')
    txt_account_name.send_keys(account_name)
    
# ================= Account Parent  =============================
    account_parent=row[2]+' '+row[3]
    parent_ctrl = fetchx('id','oe-field-input-3')
    parent_ctrl.send_keys(account_parent)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, account_parent))
        
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
#===================================================================


# ================= Account Internal Type  =============================
    account_internal_type=row[4] 
    parent_ctrl = fetchx('id','oe-field-input-4')
    parent_ctrl.send_keys(account_internal_type)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, account_internal_type))
        
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
#===================================================================

# ================= Account Type  ==================================
    account_type=row[5] 
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

# ================= Account Company  ==================================
    account_company=row[5] 
    parent_ctrl = fetchx('id','oe-field-input-7')
    parent_ctrl.send_keys(account_company)
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.LINK_TEXT, account_company))
        
        )
    finally:
        pass
    element.click()
    driver.implicitly_wait(3)
#===================================================================

    
    btn_save=fetchx('button', 'oe_form_button_save btn btn-primary btn-sm')
    btn_save.click()

def create_company(company_name,company_parent,myiterator):

    time.sleep(1)    

        # Create new Account
    if myiterator==0:
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
    driver.get(navigate('',menu_id,action))
    driver.implicitly_wait(2)
    
    with open('/home/ehab/exported_data/companies.csv', 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            create_company(row[1],row[2],myiterator)
            myiterator+=1

def create_accounts(menu_id,action):
#     driver.implicitly_wait(20)
    time.sleep(3)
    driver.get(navigate('',menu_id,action))
    time.sleep(3)
#     driver.implicitly_wait(20)
    with open('/home/ehab/exported_data/accounts.csv', 'rb') as csvfile:
        myrows = csv.reader(csvfile, delimiter=',', quotechar='|')
        myiterator=0
        for row in myrows:
            create_account(row,myiterator)
            myiterator+=1


# create_companies('62','51')
create_accounts('175','173')

    


