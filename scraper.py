from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import pickle
from datetime import datetime
import sys
import chromedriver_autoinstaller
from dotenv import find_dotenv, load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless') # ensure GUI is off
chrome_options.add_argument("--disable-search-engine-choice-screen")
chrome_options.add_argument("--disable-blink-features")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

chromedriver_autoinstaller.install()

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 20)

os.system("cls")

def clickElement(xpath):
    try:
        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        showmore_link.click()

    except Exception:
        print("Trying to click on the button again")
        driver.execute_script("arguments[0].click()", showmore_link)

def locateElement(xpath):
    try:
        element = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        element = element[0].get_attribute('innerHTML')
        element = BeautifulSoup(element, features="lxml")
        element = element.text
        return element
    except Exception: 
        print("\nCould not locate element\n")
        return ""

def send_keysElement(xpath, keys):
    try:
        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        showmore_link.send_keys(keys)

    except Exception:
        print("Couldn't send keys")

def run():
    driver.get('https://x.com/home')

    
    # sign in
    clickElement('//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[3]/a/div')

    send_keysElement(
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input', 
        os.getenv('EMAIL')
    )
    clickElement('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div')

    send_keysElement(
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input',
        os.getenv('XUSERNAME')
    )
    clickElement('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div')

    send_keysElement(
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
        os.getenv('PASSWORD')
    )
    clickElement('//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div')
    
    #input("Login... \nPress enter to continue...")

    for i in range(5):
        text = locateElement(f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[2]')
        print(text)



if __name__ == '__main__':
    run()
    input()
