from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

class ebayBot():
    '''
    Bot object for eBay.
    Email parameter can be email or username.
    '''

    def __init__(self, email, password):

        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(options=self.browserProfile)
        self.email = email
        self.password = password
        self.signedIn = False

    def buyItem(self,someLink):
        '''
        Accepts a url to an eBay product for purchasing
        '''
        if not(self.signedIn):
            self.signIn()

        # Navigate to link
        self.browser.get(someLink)
        buyItemInput = self.browser.find_element_by_id('binBtn_btn')
        buyItemInput.click()
        sleep(2)

        # Check if navigated to checkout
        currentUrl = self.browser.current_url
        if (currentUrl[8:11] != 'pay'):
            self.browser.get('https://cart.ebay.com/')
            sleep(2)
            checkoutButton = self.browser.find_element_by_class_name('cartsummary-cta')
            checkoutAction = ActionChains(self.browser).move_to_element(checkoutButton).click().perform()
            sleep(1)

        # Buy item
        sleep(2)
        purchaseButton = self.browser.find_element_by_class_name('confirm-and-pay-wrapper')
        purchaseAction = ActionChains(self.browser).move_to_element(purchaseButton).click().perform()
        sleep(2)

    def buyItems(self,items):
        '''
        Takes a list of links
        for purcashing
        '''

        for item in items:
            self.buyItem(item)

    def processItems(self, document):
        '''
        Processes a document (e.g. 'Links.txt')
        containing one url link per line and
        returns a list of the links. buyItems()
        can accept the list if desired.
        '''

        items = []

        try:
            file = open(document, 'r')
            try:
                for line in file.readlines():
                    items.append(line.strip('\n'))
            except:
                print('Ensure the file is one link per line')
        except FileNotFoundError as fnf:
            print(fnf)


        return items

    def signIn(self):

        self.browser.get('https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&ru=https%3A%2F%2Fwww.ebay.com%2F')

        emailInput = self.browser.find_element_by_id('userid')
        passwordInput = self.browser.find_element_by_id('pass')

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        sleep(1)
        self.signedIn = True

    def logout(self):

        self.browser.get('https://signin.ebay.com/ws/eBayISAPI.dll?SignIn&lgout=1')
