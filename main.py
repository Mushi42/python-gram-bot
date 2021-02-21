""" Imports """
from selenium import webdriver
import time
from bs4 import BeautifulSoup

# from schema import collection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

"""Driver Arguments """
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\hp\\AppData\\Local\\Google\\Chrome\\User Data")
"""To run in headless mode uncomment that argument"""
# options.add_argument('--headless')

"""Variables"""
pageNumber = 0
paginationNumber = 0
timeout = 25000

"""Initializing Webdriver"""
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
while pageNumber <= paginationNumber:
    try:
        URL = 'https://gramfree.today/free'
        """Opening URL"""
        driver.get(URL)
        """Getting page source"""
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#roll-button")))
        driver.find_element_by_css_selector('#roll-button').click()

    except:
        print('Something went wrong...')
        driver.close()
if driver:
    driver.close()
