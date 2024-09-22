
"""
Sources:
Selenium source: https://selenium-python.readthedocs.io/
Parsing of text: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ 

Extra (solved minor issues):
Solved issue with dotenv: https://www.reddit.com/r/flask/comments/116h0w4/having_issues_with_pythondotenv_for_my_flask/ 
Wrong target window: https://stackoverflow.com/questions/64580493/selenium-giving-message-no-such-window-target-window-already-closed-from-unkn 
Select standard search engine: https://stackoverflow.com/questions/78787332/selecting-default-search-engine-is-needed-for-chrome-version-127
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
# Source: https://www.reddit.com/r/flask/comments/116h0w4/having_issues_with_pythondotenv_for_my_flask/

chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument("--disable-search-engine-choice-screen")
# Source: https://stackoverflow.com/questions/78787332/selecting-default-search-engine-is-needed-for-chrome-version-127 

driver1 = webdriver.Chrome(options=chrome_options)
wait1 = WebDriverWait(driver1, 20)

driver2 = webdriver.Chrome(options=chrome_options)
wait2 = WebDriverWait(driver2, 20)

os.system("cls")

def clickElement(driver, wait, xpath):
    try:
        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        showmore_link.click()

    except Exception:
        driver.execute_script("arguments[0].click()", showmore_link)

def locateElement(wait, xpath):
    try:
        element = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
        element = element[0].get_attribute('innerHTML')
        element = BeautifulSoup(element, features="lxml")
        element = element.text
        return element
    except Exception: 
        print("\nCould not locate element\n")
        return ""

def send_keysElement(wait, xpath, keys):
    try:
        showmore_link = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        showmore_link.send_keys(keys)

    except Exception as e:
        print("Couldn't send keys")
        print(e)

def signInTwitter():
    driver1.get('https://x.com/home')

    # sign in
    clickElement(
        driver1,
        wait1,
        '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[3]/a/div'
    )

    send_keysElement(
        wait1,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[4]/label/div/div[2]/div/input', 
        os.getenv('EMAIL')
    )
    clickElement(
        driver1,
        wait1,
        '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]/div'
    )

    login_option = locateElement(
        wait1,
        '//*[@id="modal-header"]/span/span'
    )
    if "password" in login_option.lower():
        send_keysElement(
            wait1,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
            os.getenv('XPASSWORD')
        )
        clickElement(
            driver1,
            wait1,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div'
        )

    # due to "suspicious activity on your account", Twitter/X may ask questions:
    else:
        send_keysElement(
            wait1,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input',
            os.getenv('XUSERNAME')
        )
        clickElement(
            driver1,
            wait1,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/button/div'
        )

        send_keysElement(
            wait1,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input',
            os.getenv('XPASSWORD')
        )
        clickElement(
            driver1,
            wait1,
            '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/button/div'
        )

def signInOpenai():
    """
        Due to OpenAI having better anti-botting protection,
        you have to sign in manually.
    """
    driver2.get('https://www.google.com/')
    print("Please Sign into OpenAI ChatGPT manually...")
    input("Press Enter to proceed:")
    
    # solves error "target window already closed":
    driver2.switch_to.window(driver2.window_handles[-1])
    # Source: https://stackoverflow.com/questions/64580493/selenium-giving-message-no-such-window-target-window-already-closed-from-unkn 

    # send intital prompt
    send_keysElement(
        wait2,
        '//*[@id="prompt-textarea"]',
        """given an input sentence only return a few values: true/false if the sentence is political, "Democrat"/"Republican" depening on which side it favors. output format: true - "Democrat".can you do that yes or no?\n"""
    )

    res = ""
    while "yes" not in res.lower():
        res = locateElement(
            wait2,
            '/html/body/div[1]/div[2]/main/div[1]/div[1]/div/div/div/div/article[2]/div/div/div[2]/div/div[1]'
        )
        time.sleep(0.1)
    print(f"ChatGPT Response To Inital Message: {res}")
    print(time.sleep(0.5))

def run():
    signInTwitter()
    signInOpenai()
    #return
    
    # Scrapes all tweets on home page (not relevant)
    f = open("data.txt", "w")

    i = 0
    while True:
        for j in range(10):
            try:
                driver1.execute_script(f"window.scrollTo(0, {2000*i});")
                author = locateElement(
                    wait1,
                    f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[5]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div/div[1]/div/a/div/div[1]/span/span'
                )
                text = locateElement(
                    wait1,
                    f'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[1]/div/div[5]/section/div/div/div[{i}]/div/div/article/div/div/div[2]/div[2]/div[2]'
                )
                print(i)
                print(text)
                if text:
                    f.write("Author: " + author + "\n" + text +"\n\n")
            except Exception as e:
                print(e)
            i += 1

if __name__ == '__main__':
    run()
    #driver1.get('https://ChatGPT.com') # To show that we get blocked immediately



    input("Press Enter to Quit:")
