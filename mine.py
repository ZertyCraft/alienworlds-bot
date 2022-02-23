import pickle
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

# Constant
WAX_USER_NAME_INPUT_XPATH = '/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[1]/input'
WAX_PASSWORD_INPUT_XPATH = '/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[1]/div[2]/input'
WAX_LOG_IN_BUTTON_XPATH = '/html/body/div[1]/div/div/div/div[1]/div/div[4]/div/div/div/div[4]/button'
WAX_APPROVE_TX_BUTTON_XPATH = '/html/body/div/div/section/div[2]/div/div[5]/button'

AW_PLAY_NOW_BUTTON_XPATH = '/html/body/div/div[3]/div/div[1]/div/div/div/div/span'
AW_MINE_BUTTON_XPATH = '/html/body/div/div[3]/div[1]/div/div[3]/div[5]/div[2]/div/div/div/div/div/div'
AW_MINE_BUTTON_TEXT_XPATH = AW_MINE_BUTTON_XPATH + '/span'
AW_CLAIM_MINE_BUTTON_XPATH = '/html/body/div/div[3]/div[1]/div/div[3]/div[5]/div[2]/div/div/div/div/div'
AW_CLAIM_MINE_BUTTON_TEXT_XPATH = AW_CLAIM_MINE_BUTTON_XPATH + '/span'
AW_TLM_BALANCE_TEXT_XPATH = '/html/body/div/div[3]/div[1]/div/div[3]/div[1]/div/div[2]/p[1]'

# Global variables
conf = []
firefox_path = ""
geckodriver_path = ""
args = ""


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--headless", help="Run headless", action='store_true')
    parser.add_argument("-v", "--verbose", help="Verbose mode", action='store_true')

    return parser.parse_args()


def debug_print(data):
    if args.verbose:
        print("[DEBUG] " + data)


def random_sleep(min_sec=5, max_sec=10):
    sec = randint(min_sec, max_sec)
    debug_print('random sleep for {} seconds'.format(sec))
    sleep(sec)


def load_conf():
    print("- Loading configuration -")

    f = open('conf.json')
    data = json.load(f)
    f.close()

    print("== Initializing firefox and geckodriver ==")

    firefox_path = data["firefox_path"]

    debug_print("Current system : " + str(system))

    if firefox_path == "":
        if system == "Windows":
            data["firefox_path"] = "C:/Program Files/Mozilla Firefox/firefox.exe"
        elif system == "Linux":
            data["firefox_path"] = "/usr/bin/firefox"
        elif system == 'Darwin':
            data["firefox_path"] = '/Applications/Firefox.app/Contents/MacOS/firefox'
        else:
            print("Error, system don't match")

    if system == "Windows":
        data["geckodriver_path"] = os.path.abspath(os.getcwd()).replace('\\',
                                                                        '/') + "/bin/geckodriver/windows/geckodriver.exe"
    elif system == "Linux":
        data["geckodriver_path"] = os.path.abspath(os.getcwd()).replace('\\',
                                                                        '/') + "/bin/geckodriver/linux/geckodriver"
    elif system == 'Darwin':
        data["geckodriver_path"] = os.path.abspath(os.getcwd()).replace('\\',
                                                                        '/') + "/bin/geckodriver/darwin/geckodriver"
    else:
        print("Error, system don't match")

    return data


def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True


def wait_for_element(xpath, refresh_count=30, refresh_on_timeout=False):
    count = 0
    while not check_exists_by_xpath(xpath):
        debug_print("Element not found, retrying")
        sleep(1)
        count += 1
        if count == refresh_count:
            if refresh_on_timeout:
                debug_print("Element not found after " + str(count) + " tries, reloading website\n---" + str(xpath))
                driver.refresh()
            else:
                debug_print("Element not found after " + str(count) + " tries, exiting\n---" + str(xpath))
                return False
    return True


def login_wax() -> bool:
    print("- Loggin in -")
    driver.get("https://all-access.wax.io/")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        cookie.pop('domain')
        cookie.pop('httpOnly')
        # cookie.pop('expiry')
        print(cookie)
        driver.add_cookie(cookie)
    driver.get("https://all-access.wax.io/")
    i = 0
    while driver.current_url != "https://wallet.wax.io/dashboard":
        i = i + 1
        if i == 9:
            break
        sleep(1)
    if driver.current_url == "https://wallet.wax.io/dashboard":
        return True
    if conf["login_method"] == 'wax':
        return connect_wax()
    elif conf["login_method"] == 'reddit':
        return connect_wax_with_reddit()


def connect_wax() -> bool:
    print("- Login -")

    random_sleep()

    debug_print('Waiting for wax user login')
    if wait_for_element(WAX_USER_NAME_INPUT_XPATH, 10, True):
        debug_print('Typing wax user name')
        random_sleep(min_sec=2, max_sec=5)
        driver.find_element_by_xpath(WAX_USER_NAME_INPUT_XPATH).send_keys(
            conf["username"])

        debug_print('Typing wax user password')
        random_sleep(min_sec=2, max_sec=5)
        driver.find_element_by_xpath(WAX_PASSWORD_INPUT_XPATH).send_keys(
            conf["password"])
        debug_print('Login wax user')
        random_sleep(min_sec=1, max_sec=2)
        driver.find_element_by_xpath(WAX_LOG_IN_BUTTON_XPATH).click()
        return True
    else:
        debug_print("Can't login with wax")
        return False


def connect_wax_with_reddit() -> bool:
    print("- Login with Reddit -")
    while driver.current_url == "https://all-access.wax.io/":
        random_sleep()
        if wait_for_element('//*[@id="reddit-social-btn"]', 30, True):
            # Click on reddit button | https://all-access.wax.io/
            driver.find_element_by_xpath('//*[@id="reddit-social-btn"]').click()
            random_sleep()

    if wait_for_element('//*[@id="loginUsername"]', 5):
        driver.find_element_by_xpath('//*[@id="loginUsername"]').send_keys(conf["username"])
        driver.find_element_by_xpath('//*[@id="loginPassword"]').send_keys(conf["password"])

        driver.find_element_by_xpath('/html/body/div/main/div[1]/div/div[2]/form/fieldset[5]/button').click()

    # Click on allow button | allow wax to access to reddit
    if wait_for_element('/html/body/div[3]/div/div[2]/form/div/input[1]'):
        driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/form/div/input[1]').click()

    else:
        print("Error, can't find Reddit login button")
        return False


def start_alien_world() -> bool:
    while driver.current_url != "https://wallet.wax.io/dashboard":
        sleep(1)

    print("- Starting AlienWorlds -")
    pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
    driver.get("https://play.alienworlds.io/")
    random_sleep()

    # Click on play now
    if wait_for_element(AW_PLAY_NOW_BUTTON_XPATH):
        driver.find_element_by_xpath(AW_PLAY_NOW_BUTTON_XPATH).click()
        random_sleep(min_sec=10)

        return True

    return False


def mine():
    print("- Start mining -")
    main_page = driver.current_window_handle

    while True:
        debug_print('Waiting for mine button')
        if (
                wait_for_element(AW_MINE_BUTTON_TEXT_XPATH,
                                 5, False)):
            # Mine button
            if driver.find_element_by_xpath(AW_MINE_BUTTON_TEXT_XPATH).text == "Mine":
                debug_print('Click on mine button')
                driver.find_element_by_xpath(AW_MINE_BUTTON_XPATH).click()
                random_sleep()

        debug_print('Waiting for claim mine button')
        if (
        wait_for_element(AW_CLAIM_MINE_BUTTON_TEXT_XPATH, 5, False)):
            # Claim mine button
            if driver.find_element_by_xpath(AW_CLAIM_MINE_BUTTON_TEXT_XPATH).text == "Claim Mine":
                debug_print('Click on claim mine button')
                driver.find_element_by_xpath(AW_CLAIM_MINE_BUTTON_XPATH).click()
                random_sleep()

                debug_print('Switch to approve transaction page')
                while len(driver.window_handles) == 1:
                    sleep(1)

                # Approve transaction
                for handle in driver.window_handles:
                    if handle != main_page:
                        confirm_page = handle

                driver.switch_to.window(confirm_page)
                random_sleep(min_sec=3)

                debug_print('Waiting for wax approve tx button')
                if wait_for_element(WAX_APPROVE_TX_BUTTON_XPATH, 30, False):
                    debug_print('Click on wax approve tx button')
                    driver.find_element_by_xpath(WAX_APPROVE_TX_BUTTON_XPATH).click()
                    random_sleep()

                    driver.switch_to.window(main_page)

                    if check_exists_by_xpath(AW_TLM_BALANCE_TEXT_XPATH):
                        balance = driver.find_element_by_xpath(AW_TLM_BALANCE_TEXT_XPATH).text
                        print("== Current balance : " + str(balance) + " Trilium ==")
                else:
                    driver.switch_to.window(main_page)
                    try:
                        confirm_page.close()
                        debug_print("Stuck on confirmation popup, closing popup and retrying")
                    except:
                        pass

        random_sleep()


if __name__ == '__main__':
    args = parse_args()
    conf = load_conf()

    # Initialize webdriver
    profile = webdriver.FirefoxProfile()
    myProxy = "127.0.0.1:3920"
    ip, port = myProxy.split(':')
    profile.set_preference('network.proxy.type', 1)
    profile.set_preference('network.proxy.socks', ip)
    profile.set_preference('network.proxy.socks_port', int(port))

    options = Options()
    options.headless = args.headless
    options.binary_location = conf["firefox_path"]

    debug_print("firefox_binary=" + conf["firefox_path"])
    debug_print("executable_path=" + conf["geckodriver_path"])

    driver = webdriver.Firefox(options=options, firefox_profile=profile, executable_path=conf["geckodriver_path"])
    driver.set_window_size(1280, 1280)
    # Initialize webdriver

    if not login_wax():
        print("Error, can't log in")
        exit()
    if not start_alien_world():
        print("Error while starting Alien Worlds")
        exit()

    mine()
