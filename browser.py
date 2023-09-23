from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def search(something):
    browser = webdriver.Edge(executable_path='C:\\Edgedriver\\msedgedriver.exe')
    browser.maximize_window()
    browser.get('https://www.google.com/')
    findElem = browser.find_element_by_name('q')
    findElem.send_keys(something)
    findElem.send_keys(Keys.RETURN)