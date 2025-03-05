from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import os
import browser_cookie3


class MFP_Logger():

    def __init__(self, username, end_date, start_date = None):
        self.username = username
        self.end_date = end_date
        if start_date == None:  self.start_date = self.end_date 
        else:   self.start_date = start_date
    
       
        self.default_url = 'https://www.myfitnesspal.com/reports/printable-diary/'+username
        self.working_url = self.default_url
        self.set_dates(self.start_date,self.end_date)
        #setting up driver options and path: (1) shows browser window, 0 hides browser.
        self.set_driver_options()
        

    def set_driver_options(self,maximised = 0):
        self.firefox_options = Options()
        self.firefox_options.add_argument('--no-sandbox')
        self.firefox_options.add_argument('--disable-dev-shm-usage')
        if maximised == 1:
            self.firefox_options.add_argument('--start-maximized')
        else: self.firefox_options.add_argument('--headless')

        driver_path = (os.getcwd())+'\geckodriver.exe' #Make sure your firefox driver is uptodate and compatable with your firefox browser and that geckodriver.exe is in same folder as this file
        self.service = Service(executable_path=driver_path)
        

    #Using browser_cookie3 to grab session token and login status from myfitnesspal
    def get_cookies(self): #Should probably learn how this actually works
        cookies = browser_cookie3.firefox(domain_name = "myfitnesspal.com")
        cookie_list = []
        for cookie in cookies:
            cookie_dict = {
                'name': cookie.name,
                'value': cookie.value,
                'domain': cookie.domain,
                'path': cookie.path,
                'secure': bool(cookie.secure),
                'httpOnly': bool(getattr(cookie, 'rest', {}).get('httpOnly', False))
            }

            cookie_list.append(cookie_dict)
        return cookie_list #returns a list of cookies in a format selenium accepts
    
    def manage_cookie_query(self,driver):
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#sp_message_iframe_1164399")) )
        driver.switch_to.frame(iframe)
        cookie_button = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".button-close")))
        cookie_button.click()

    

    def load_all_tables(self,driver):#scrolls to bottom of webpage, otherwise selenium reads the elements as ''
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)
            new_height = driver.execute_script("return document.body.scrollHeight")
            #print(f"Old height: {last_height}, New height: {new_height}")
            if new_height == last_height:
                break
            last_height = new_height
    
    def get_nutrition(self,driver):
        webElement_calories = driver.find_elements(By.CSS_SELECTOR,"th.css-1pxpb76:nth-child(2)")
        webElement_Carbs = driver.find_elements(By.CSS_SELECTOR,"th.css-1pxpb76:nth-child(3)")
        webElement_Protein = driver.find_elements(By.CSS_SELECTOR,"th.css-1pxpb76:nth-child(4)")
        webElement_Fat = driver.find_elements(By.CSS_SELECTOR,"th.css-1pxpb76:nth-child(5)")
        webElement_dates = driver.find_elements(By.CSS_SELECTOR,'p.MuiTypography-root:nth-child(1)')
        food_Diary = {}
        for i in range(len(webElement_dates)):
            date = datetime.strptime(webElement_dates[i].text, "%b %d, %Y").strftime('%d/%m/%Y')
            food_Diary['%s'%date] = {
                "Calories":webElement_calories[i].text,
                "Carbohydrates": webElement_Carbs[i].text,
                'Protein':webElement_Protein[i].text,
                'Fats': webElement_Fat[i].text
            }
          
        return food_Diary
    
    def set_dates(self,start_date, end_date):
        if start_date != self.start_date:
            self.start_date = start_date
        if end_date != self.end_date:
            self.end_date = end_date

        start_date_string = datetime.strftime(start_date, "%Y-%m-%d")
        end_date_string = datetime.strftime(end_date, "%Y-%m-%d")
        self.working_url = self.default_url + "?from=%s&to=%s" % (start_date_string,end_date_string)
    def login_check(self,driver):

        private_diary = WebDriverWait(driver,3).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,"p.css-9xqzco"),"This user maintains a private diary."))
        if private_diary == 1:
            raise Exception("Diary is private. Login to myfitnesspal on firefox, or deprivate printable diary")
    
    def run(self):
        cookie_list = self.get_cookies()
        #print(self.driver_path)
        driver = webdriver.Firefox(service=self.service,options=self.firefox_options )
        driver.get(self.working_url)
        try:
            for cookie in cookie_list:
                try:
                    driver.add_cookie(cookie)
                except Exception as e:
                    print(f"Failed to add cookie{cookie['name']}",e)
            time.sleep(2)
            driver.refresh()
            
            
    
            try: self.login_check(driver) 
            except Exception as e: print(e,"\n",self.working_url)
            
            try:#handles the cookie pop up when accessing the diary
                self.manage_cookie_query(driver)
                
            except Exception as e:
                print(f'Cookie button not found or not clickable:',e,"\n", self.working_url)

            
            driver.switch_to.default_content()  
            self.load_all_tables(driver)
            
            diary = self.get_nutrition(driver)
            driver.quit()
        except Exception as e:
            driver.quit()
            print("ERROR:", e,"\n")
            return "ERROR"
        return diary