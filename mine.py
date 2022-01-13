from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent

from time import sleep
from random import randint

import pprint

import json

from argparse import ArgumentParser


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("--headless", help="Run headless", action='store_true')

    return parser.parse_args()






args = parseArgs()
############ Initialize webdriver ############
profile = webdriver.FirefoxProfile()

useragent = UserAgent()
profile.set_preference("general.useragent.override", useragent.random)
profile.update_preferences()


options = Options()
options.headless = args.headless

driver = webdriver.Firefox(options=options, firefox_profile=profile)
driver.set_window_size(1280, 1280)

conf = []
############ Initialize webdriver ############






def loadConf():
    print("- Loading configuration -")

    f = open('conf.json')
    data = json.load(f)
    f.close()

    return data

def checkExistsByXpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True
def waitForElement(xpath, refreshCount = 30, refreshOnTimeout = False):
    count = 0
    while checkExistsByXpath(xpath) == False:
        sleep(1)
        count += 1
        if(count == refreshCount):
            if refreshOnTimeout:
                driver.refresh()
            else:  
                return False
    return True


def loginWax():
    print("- Loggin in -")
    driver.get("https://all-access.wax.io/")

    
    if conf["login_method"] == 'wax':
        connectWax()
    elif conf["login_method"] == 'reddit':
        connectWaxWithReddit()

def connectWax():
    print("- Login -")
    
    sleep(5)

    

    if(waitForElement('/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[1]/input', 10, True) == True):
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[1]/input').send_keys(conf["username"])
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[2]/input').send_keys(conf["password"])

        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[4]/button').click()
    else:
        print("Error, can't login")
        return False
        

def connectWaxWithReddit():
    print("- Login with Reddit -")
    while(driver.current_url == "https://all-access.wax.io/"):
        sleep(5)
        if(waitForElement('//*[@id="reddit-social-btn"]', 30, True) == True):

            # Click on reddit button | https://all-access.wax.io/
            driver.find_element_by_xpath('//*[@id="reddit-social-btn"]').click()
            sleep(5)

        
    if(waitForElement('//*[@id="loginUsername"]', 5) == True):
        driver.find_element_by_xpath('//*[@id="loginUsername"]').send_keys(conf["username"])
        driver.find_element_by_xpath('//*[@id="loginPassword"]').send_keys(conf["password"])

        driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()

    # Click on allow button | allow wax to access to reddit
    if(waitForElement('/html/body/div[3]/div/div[2]/form/div/input[1]') == True):
        driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/form/div/input[1]').click()

    else:
        print("Error, can't find Reddit login button")
        return False

def startAlienWorld():
    while(driver.current_url != "https://wallet.wax.io/dashboard"):
        sleep(1)
    
    print("- Starting AlienWorlds -")
    driver.get("https://play.alienworlds.io/")
    sleep(5)
    
    # Click on play now
    if(waitForElement('/html/body/div/div[3]/div/div[1]/div[2]') == True):
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div[2]').click()


def mine():
    print("- Start mining -")
    mainPage = driver.current_window_handle

    while True:


        if(waitForElement('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div/span', 5, False)):
            
        #    if(checkExistsByXpath('/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]')):
        #        balance = driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]').text
        #        print("== Current balance : " + str(balance) + " Trilium ==")

            # Mine button
            if(driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div/span').text == "Mine"):
                driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div').click()
                sleep(5)
        
        if(waitForElement('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/span', 5, False)):
            # Claim mine button
            if(driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/span').text == "Claim Mine"):
                driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div').click()
                sleep(5)
    
                while(len(driver.window_handles) == 1):
                    sleep(1)

                for handle in driver.window_handles:
                    if handle != mainPage:
                        confirmPage = handle

                driver.switch_to.window(confirmPage)
                sleep(2)
                while(waitForElement('/html/body/div/div/section/div[2]/div/div[5]/button', 30, False) == False):
                    sleep(2)


                driver.find_element_by_xpath('/html/body/div/div/section/div[2]/div/div[5]/button').click()
                sleep(5)

                driver.switch_to.window(mainPage)

                if(checkExistsByXpath('/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]')):
                    balance = driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]').text
                    print("== Current balance : " + str(balance) + " Trilium ==")


        sleep(randint(5, 15))
    
    return False

if __name__ == '__main__':
    conf = loadConf()

    if(loginWax() == False):
        print("Error, can't loggin")
        exit()
    elif(startAlienWorld() == False):
        print("Error while starting Alienworld")
        exit()

    elif(mine() == False):
        print("Error while mining")
        exit()
