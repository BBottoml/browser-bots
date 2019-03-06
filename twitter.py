from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep

class TwitterBot():

    def __init__(self, username, password):
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(options=self.browserProfile)
        self.username = username
        self.password = password
    
    def signIn(self):

        self.browser.get("https://twitter.com/login")
        
        fieldOne = self.browser.find_elements_by_class_name('js-username-field')[0]
        fieldTwo = self.browser.find_element_by_class_name('js-password-field')

        fieldOne.send_keys(self.username)
        fieldTwo.send_keys(self.password)
        fieldTwo.send_keys(Keys.ENTER)
        sleep(10)
    