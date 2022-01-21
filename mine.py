from time import sleep
from random import randint
import os
import pprint
import platform
import json
from argparse import ArgumentParser
import warnings

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent

system = platform.system()

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Global variables
conf = []
firefox_path = ""
geckodriver_path = ""
args = ""


def parseArgs():
    parser = ArgumentParser()
    parser.add_argument("--headless", help="Run headless", action='store_true')
    parser.add_argument("-v", "--verbose", help="Verbose mode", action='store_true')

    return parser.parse_args()


def debugPrint(data):
    if args.verbose:
        print("[DEBUG] " + str(data))


def loadConf():
    print("- Loading configuration -")

    f = open('conf.json')
    data = json.load(f)
    f.close()

    print("== Initializing firefox and geckodriver ==")

    firefox_path = data["firefox_path"]

    if firefox_path == "":
        if system == "Windows":
            data["firefox_path"] = "C:/Program Files/Mozilla Firefox/firefox.exe"
        elif system == "Linux":
            data["firefox_path"] = "/usr/bin/firefox"
        else:
            print("Error, system don't match")

    if system == "Windows":
        data["geckodriver_path"] = os.path.abspath(os.getcwd()).replace('\\',
                                                                        '/') + "/bin/geckodriver/windows/geckodriver.exe"
    elif system == "Linux":
        data["geckodriver_path"] = os.path.abspath(os.getcwd()).replace('\\',
                                                                        '/') + "/bin/geckodriver/linux/geckodriver"
    else:
        print("Error, system don't match")

    debugPrint("Current system : " + str(system))

    return data


def checkExistsByXpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def waitForElement(xpath, refreshCount=30, refreshOnTimeout=False):
    count = 0
    while checkExistsByXpath(xpath) == False:
        debugPrint("Element not found, retrying")
        sleep(1)
        count += 1
        if (count == refreshCount):
            if refreshOnTimeout:
                debugPrint("Element not found after " + str(count) + " tries, reloading website\n---" + str(xpath))
                driver.refresh()
            else:
                debugPrint("Element not found after " + str(count) + " tries, exiting\n---" + str(xpath))
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

    if (waitForElement('/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[1]/input', 10,
                       True) == True):
        driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[1]/input').send_keys(
            conf["username"])
        driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[2]/input').send_keys(
            conf["password"])

        driver.find_element_by_xpath(
            '/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[4]/button').click()
    else:
        print("Error, can't login")
        debugPrint("Can't loggin with wax")
        return False


def connectWaxWithReddit():
    print("- Login with Reddit -")
    while (driver.current_url == "https://all-access.wax.io/"):
        sleep(5)
        if (waitForElement('//*[@id="reddit-social-btn"]', 30, True) == True):
            # Click on reddit button | https://all-access.wax.io/
            driver.find_element_by_xpath('//*[@id="reddit-social-btn"]').click()
            sleep(5)

    if (waitForElement('//*[@id="loginUsername"]', 5) == True):
        driver.find_element_by_xpath('//*[@id="loginUsername"]').send_keys(conf["username"])
        driver.find_element_by_xpath('//*[@id="loginPassword"]').send_keys(conf["password"])

        driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()

    # Click on allow button | allow wax to access to reddit
    if (waitForElement('/html/body/div[3]/div/div[2]/form/div/input[1]') == True):
        driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/form/div/input[1]').click()

    else:
        print("Error, can't find Reddit login button")
        return False


def startAlienWorld():
    while (driver.current_url != "https://wallet.wax.io/dashboard"):
        sleep(1)

    print("- Starting AlienWorlds -")
    driver.get("https://play.alienworlds.io/")
    sleep(5)

    # Click on play now
    if (waitForElement('/html/body/div/div[3]/div/div[1]/div/div/div/div/span') == True):
        driver.find_element_by_xpath('/html/body/div/div[3]/div/div[1]/div/div/div/div/span').click()


def mine():
    print("- Start mining -")
    mainPage = driver.current_window_handle

    while True:

        if (
        waitForElement('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div/span', 5, False)):
            # Mine button
            if (driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/div/span').text == "Mine"):
                driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div').click()
                sleep(5)

        if (waitForElement('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/span', 5, False)):
            # Claim mine button
            if (driver.find_element_by_xpath(
                    '/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div/div/div/div/span').text == "Claim Mine"):
                driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div[3]/div[3]/div[2]/div/div').click()
                sleep(5)

                while (len(driver.window_handles) == 1):
                    sleep(1)

                for handle in driver.window_handles:
                    if handle != mainPage:
                        confirmPage = handle

                driver.switch_to.window(confirmPage)
                sleep(2)
                if waitForElement('/html/body/div/div/section/div[2]/div/div[5]/button', 30, False):
                    driver.find_element_by_xpath('/html/body/div/div/section/div[2]/div/div[5]/button').click()
                    sleep(5)

                    driver.switch_to.window(mainPage)

                    if (checkExistsByXpath('/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]')):
                        balance = driver.find_element_by_xpath(
                            '/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]').text
                        print("== Current balance : " + str(balance) + " Trilium ==")
                else:
                    driver.switch_to.window(mainPage)
                    confirmPage.close()
                    debugPrint("Stuck on confirmation popup, closing popup and retrying")

        sleep(randint(5, 15))

    return False


if __name__ == '__main__':
    args = parseArgs()
    conf = loadConf()

    ############ Initialize webdriver ############
    profile = webdriver.FirefoxProfile()

    options = Options()
    options.headless = args.headless
    options.binary_location = conf["firefox_path"]

    debugPrint("firefox_binary=" + conf["firefox_path"])
    debugPrint("executable_path=" + conf["geckodriver_path"])
    driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=conf["geckodriver_path"])
    driver.set_window_size(1280, 1280)
    ############ Initialize webdriver ############

    if (loginWax() == False):
        print("Error, can't loggin")
        exit()
    elif (startAlienWorld() == False):
        print("Error while starting Alienworld")
        exit()

    elif (mine() == False):
        print("Error while mining")
        exit()
