from selenium import webdriver

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
password = "1"
db='db2010'


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

# Navigate to the Accounting > Accounts > Accounts. Menu=175 , Action = 173
driver.get(navigate('','175','173'))
driver.implicitly_wait(2)
# Get and the "Create" Button
btn_create= fetchx('button', 'oe_list_add btn btn-primary btn-sm')

# Create new Account
btn_create.click()

driver.implicitly_wait(3)
# //txt_account_name=fetchx('placeholder','Account name')

txt_account_code = fetchx('id', 'oe-field-input-4')
txt_account_code.send_keys('123456789')

txt_account_name=fetchx('placeholder', 'Account name')
txt_account_name.send_keys('Bitty Cash')

account_type="Asset"
account_type_ctrl = fetchx('id','oe-field-input-7')
account_type_ctrl.send_keys(account_type)


# This is for selecting items from Odoo's drop down lists which are not really dropdown
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Asset"))
    
    )
finally:
    pass
element.click()
driver.implicitly_wait(3)

txt_account_code.send_keys('0001')
btn_save=fetchx('button', 'oe_form_button_save btn btn-primary btn-sm')
btn_save.click()







