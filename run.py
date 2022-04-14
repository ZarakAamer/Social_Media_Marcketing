import json
import random
import threading
from time import sleep
import smtplib
import requests
import os
import selenium
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium import webdriver

from tkinter import *
from tkinter import filedialog

from bs4 import BeautifulSoup

from telethon import TelegramClient, events, sync

import pandas as pd

# initializing from the tk gui
w = Tk()
w.geometry('600x600')
w.title('Send Messages On Instagram And Whatsapp')

# Report Procedure
Label(w, text='Enter Your Whatsapp Number in international formate\nTo recieve Completion Report', fg='black').pack(pady=20)
phone_number = Entry(w, bg='black', fg='white', width=40)
phone_number.pack()
def Reporter():
    global send_report
    send_report = phone_number.get()

Button(w, text='Submit This Number', bg='Pink', fg='Black', command=Reporter).pack(pady=5)



# Just a message
Label(w,).pack(pady=10)
lable = Label(w, text='Keep Whatsapp Numbers in "W_Numbers.txt"\nTelegram Numbers in numbers.txt')
lable.pack(pady=20)




#Just giving  a little margin
Label(w,).pack(pady=30)
Label(w,).pack(pady=10)
f = open('accounts.json', )
accounts = json.load(f)




#opening message file along with emojies etc inside it


try:
    with open('messages.txt', 'r', encoding='utf-8') as f:
        raw_messages = f.read()
        messages = raw_messages.replace('\n', ' ')
except Exception as e:
    print(e)
    with open('messages.txt', 'r', encoding='ISO-8859-1') as f:
        raw_messages = f.read()
        messages = raw_messages.replace('\n', ' ')
        
            



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from random import randint, uniform
from time import time, sleep
import logging
import sqlite3

DEFAULT_IMPLICIT_WAIT = 1

class InstaDM(object):

    def __init__(self, username, password, headless=True, instapy_workspace=None, profileDir=None):
        self.selectors = {
            "accept_cookies": "//button[text()='Accept']",
            "home_to_login_button": "//button[text()='Log In']",
            "username_field": "username",
            "password_field": "password",
            "button_login": "//button/*[text()='Log In']",
            "login_check": "//*[@aria-label='Home'] | //button[text()='Save Info'] | //button[text()='Not Now']",
            "search_user": "queryBox",
            "select_user": '//div[text()="{}"]',
            "name": "((//div[@aria-labelledby]/div/span//img[@data-testid='user-avatar'])[1]//..//..//..//div[2]/div[2]/div)[1]",
            "next_button": "//button/*[text()='Next']",
            "textarea": "//textarea[@placeholder]",
            "send": "//button[text()='Send']"
        }

        # Selenium config
        options = webdriver.ChromeOptions()

        if profileDir:
            options.add_argument("user-data-dir=profiles/" + profileDir)

        if headless:
            options.add_argument("--headless")

        mobile_emulation = {
            "userAgent": 'Mozilla/5.0 (Linux; Android 10.0; iPhone Xs Max Build/IML74K) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/91.0.4472.77 Mobile Safari/535.19'
        }
        options.add_experimental_option("mobileEmulation", mobile_emulation)
        options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(
            executable_path=CM().install(), options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(414, 936)

        # Instapy init DB
        self.instapy_workspace = instapy_workspace
        self.conn = None
        self.cursor = None
        if self.instapy_workspace is not None:
            self.conn = sqlite3.connect(
                self.instapy_workspace + "InstaPy/db/instapy.db")
            self.cursor = self.conn.cursor()

            cursor = self.conn.execute("""
                SELECT count(*)
                FROM sqlite_master
                WHERE type='table'
                AND name='message';
            """)
            count = cursor.fetchone()[0]

            if count == 0:
                self.conn.execute("""
                    CREATE TABLE "message" (
                        "username"    TEXT NOT NULL UNIQUE,
                        "message"    TEXT DEFAULT NULL,
                        "sent_message_at"    TIMESTAMP
                    );
                """)

        try:
            self.login(username, password)
        except Exception as e:
            logging.error(e)
            print(str(e))

    def login(self, username, password):
        # homepage
        self.driver.get('https://instagram.com/?hl=en')
        self.__random_sleep__(3, 5)
        if self.__wait_for_element__(self.selectors['accept_cookies'], 'xpath', 10):
            self.__get_element__(
                self.selectors['accept_cookies'], 'xpath').click()
            self.__random_sleep__(3, 5)
        if self.__wait_for_element__(self.selectors['home_to_login_button'], 'xpath', 10):
            self.__get_element__(
                self.selectors['home_to_login_button'], 'xpath').click()
            self.__random_sleep__(5, 7)

        # login
        logging.info(f'Login with {username}')
        self.__scrolldown__()
        if not self.__wait_for_element__(self.selectors['username_field'], 'name', 10):
            print('Login Failed: username field not visible')
        else:
            self.driver.find_element_by_name(
                self.selectors['username_field']).send_keys(username)
            self.driver.find_element_by_name(
                self.selectors['password_field']).send_keys(password)
            self.__get_element__(
                self.selectors['button_login'], 'xpath').click()
            self.__random_sleep__()
            if self.__wait_for_element__(self.selectors['login_check'], 'xpath', 10):
                print('Login Successful')
            else:
                print('Login Failed: Incorrect credentials')

    def createCustomGreeting(self, greeting):
        # Get username and add custom greeting
        if self.__wait_for_element__(self.selectors['name'], "xpath", 10):
            user_name = self.__get_element__(
                self.selectors['name'], "xpath").text
            if user_name:
                greeting = greeting + " " + user_name + ", \n\n"
        else:
            greeting = greeting + ", \n\n"
        return greeting

    def typeMessage(self, user, message):
        # Go to page and type message
        if self.__wait_for_element__(self.selectors['next_button'], "xpath"):
            self.__get_element__(
                self.selectors['next_button'], "xpath").click()
            self.__random_sleep__()

        if self.__wait_for_element__(self.selectors['textarea'], "xpath"):
            self.__type_slow__(self.selectors['textarea'], "xpath", message)
            self.__random_sleep__()

        if self.__wait_for_element__(self.selectors['send'], "xpath"):
            self.__get_element__(self.selectors['send'], "xpath").click()
            self.__random_sleep__(3, 5)
            print('Message sent successfully')

    def sendMessage(self, user, message, greeting=None):
        logging.info(f'Send message to {user}')
        print(f'Send message to {user}')
        self.driver.get('https://www.instagram.com/direct/new/?hl=en')
        self.__random_sleep__(2, 4)

        try:
            self.__wait_for_element__(self.selectors['search_user'], "name")
            self.__type_slow__(self.selectors['search_user'], "name", user)
            self.__random_sleep__(1, 2)

            if greeting != None:
                greeting = self.createCustomGreeting(greeting)

            # Select user from list
            elements = self.driver.find_elements_by_xpath(
                self.selectors['select_user'].format(user))
            if elements and len(elements) > 0:
                elements[0].click()
                self.__random_sleep__()

                if greeting != None:
                    self.typeMessage(user, greeting + message)
                else:
                    self.typeMessage(user, message)

                if self.conn is not None:
                    self.cursor.execute(
                        'INSERT INTO message (username, message) VALUES(?, ?)', (user, message))
                    self.conn.commit()
                self.__random_sleep__(5, 10)

                return True

            # In case user has changed his username or has a private account
            else:
                print(f'User {user} not found! Skipping.')
                return False

        except Exception as e:
            logging.error(e)
            return False

    def sendGroupMessage(self, users, message):
        logging.info(f'Send group message to {users}')
        print(f'Send group message to {users}')
        self.driver.get('https://www.instagram.com/direct/new/?hl=en')
        self.__random_sleep__(5, 7)

        try:
            usersAndMessages = []
            for user in users:
                if self.conn is not None:
                    usersAndMessages.append((user, message))

                self.__wait_for_element__(
                    self.selectors['search_user'], "name")
                self.__type_slow__(self.selectors['search_user'], "name", user)
                self.__random_sleep__()

                # Select user from list
                elements = self.driver.find_elements_by_xpath(
                    self.selectors['select_user'].format(user))
                if elements and len(elements) > 0:
                    elements[0].click()
                    self.__random_sleep__()
                else:
                    print(f'User {user} not found! Skipping.')

            self.typeMessage(user, message)

            if self.conn is not None:
                self.cursor.executemany("""
                    INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)
                """, usersAndMessages)
                self.conn.commit()
            self.__random_sleep__(50, 60)

            return True

        except Exception as e:
            logging.error(e)
            return False

    def sendGroupIDMessage(self, chatID, message):
        logging.info(f'Send group message to {chatID}')
        print(f'Send group message to {chatID}')
        self.driver.get('https://www.instagram.com/direct/inbox/')
        self.__random_sleep__(5, 7)

        # Definitely a better way to do this:
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.TAB*2 + Keys.ENTER).perform()
        actions.send_keys(Keys.TAB*4 + Keys.ENTER).perform()

        if self.__wait_for_element__(f"//a[@href='/direct/t/{chatID}']", 'xpath', 10):
            self.__get_element__(
                f"//a[@href='/direct/t/{chatID}']", 'xpath').click()
            self.__random_sleep__(3, 5)

        try:
            usersAndMessages = [chatID]

            if self.__wait_for_element__(self.selectors['textarea'], "xpath"):
                self.__type_slow__(
                    self.selectors['textarea'], "xpath", message)
                self.__random_sleep__()

            if self.__wait_for_element__(self.selectors['send'], "xpath"):
                self.__get_element__(self.selectors['send'], "xpath").click()
                self.__random_sleep__(3, 5)
                print('Message sent successfully')

            if self.conn is not None:
                self.cursor.executemany("""
                    INSERT OR IGNORE INTO message (username, message) VALUES(?, ?)
                """, usersAndMessages)
                self.conn.commit()
            self.__random_sleep__(50, 60)

            return True

        except Exception as e:
            logging.error(e)
            return False

    def __get_element__(self, element_tag, locator):
        """Wait for element and then return when it is available"""
        try:
            locator = locator.upper()
            dr = self.driver
            if locator == 'ID' and self.is_element_present(By.ID, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_id(element_tag))
            elif locator == 'NAME' and self.is_element_present(By.NAME, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_name(element_tag))
            elif locator == 'XPATH' and self.is_element_present(By.XPATH, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_xpath(element_tag))
            elif locator == 'CSS' and self.is_element_present(By.CSS_SELECTOR, element_tag):
                return WebDriverWait(dr, 15).until(lambda d: dr.find_element_by_css_selector(element_tag))
            else:
                logging.info(f"Error: Incorrect locator = {locator}")
        except Exception as e:
            logging.error(e)
        logging.info(f"Element not found with {locator} : {element_tag}")
        return None

    def is_element_present(self, how, what):
        """Check if an element is present"""
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException:
            return False
        return True

    def __wait_for_element__(self, element_tag, locator, timeout=30):
        """Wait till element present. Max 30 seconds"""
        result = False
        self.driver.implicitly_wait(0)
        locator = locator.upper()
        for i in range(timeout):
            initTime = time()
            try:
                if locator == 'ID' and self.is_element_present(By.ID, element_tag):
                    result = True
                    break
                elif locator == 'NAME' and self.is_element_present(By.NAME, element_tag):
                    result = True
                    break
                elif locator == 'XPATH' and self.is_element_present(By.XPATH, element_tag):
                    result = True
                    break
                elif locator == 'CSS' and self.is_element_present(By.CSS_SELECTORS, element_tag):
                    result = True
                    break
                else:
                    logging.info(f"Error: Incorrect locator = {locator}")
            except Exception as e:
                logging.error(e)
                print(f"Exception when __wait_for_element__ : {e}")

            sleep(1 - (time() - initTime))
        else:
            print(
                f"Timed out. Element not found with {locator} : {element_tag}")
        self.driver.implicitly_wait(DEFAULT_IMPLICIT_WAIT)
        return result

    def __type_slow__(self, element_tag, locator, input_text=''):
        """Type the given input text"""
        try:
            self.__wait_for_element__(element_tag, locator, 5)
            element = self.__get_element__(element_tag, locator)
            actions = ActionChains(self.driver)
            actions.click(element).perform()
            for s in input_text:
                element.send_keys(s)
                sleep(uniform(0.005, 0.02))

        except Exception as e:
            logging.error(e)
            print(f'Exception when __typeSlow__ : {e}')

    def __random_sleep__(self, minimum=2, maximum=7):
        t = randint(minimum, maximum)
        logging.info(f'Wait {t} seconds')
        sleep(t)

    def __scrolldown__(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

    def teardown(self):
        self.driver.close()
        self.driver.quit()















    # print(messages)





# sending messages on telegram
def send_message_telegram():
    # CHROME_PROFILE_PATH = "user-data-dir=C:\\Users\\mak\\AppData\\Local\\Google\\Chrome\\User Data\\wtsp"
    options = webdriver.ChromeOptions()
    # options.add_argument(CHROME_PROFILE_PATH)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  
    counter = 0
    filepath = filedialog.askopenfilename()
    with open('numbers.txt', 'r') as f:
        for user_details in f:
            api_id = '15776288'
            api_hash = '77980bcafc60f37b16887dcff9ac59b2'
            try:
                client = TelegramClient('session_name', api_id, api_hash)
                client.start()
                client.send_message(user_details, messages)
                client.send_file(user_details, filepath)
                counter+=1
   
            except:
                pass
    message = f'Messages were send on whatsapp to \n {counter} users.'
    driver.get(f'https://web.whatsapp.com/send?phone={send_report}')
    sleep(30)

    driver.find_element_by_xpath('//div[@title = "Type a message"]').send_keys(message)
    sleep(3)
    # send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
    # send_button.click()
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()








# sending message on whatsapp

def whatsa():
    counter = 0
    filepath = filedialog.askopenfilename()
    # CHROME_PROFILE_PATH = "user-data-dir=C:\\Users\\mak\\AppData\\Local\\Google\\Chrome\\User Data\\wtsp"
    options = webdriver.ChromeOptions()
    # options.add_argument(CHROME_PROFILE_PATH)
    # driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    # driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    with open('W_Numbers.txt', 'r') as f:
        for line in f:
            try:
                driver.get(f'https://web.whatsapp.com/send?phone={line}')
                sleep(15)

                attachment_box = driver.find_element_by_xpath(
                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span')
                attachment_box.click()
                sleep(3)
                image_box = driver.find_element_by_xpath(
                    '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input')
                image_box.send_keys(filepath)
                sleep(2)
                text_box = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[1]/div[3]/div/div/div[2]/div[1]/div[2]')
                for character in messages:
                    text_box.send_keys(character)
                    sleep(0.1)

                
                # time.sleep(3)
                # chngProf = driver.find_element_by_xpath('//*[@id="side"]/header/div[1]/div/div')
                # chngProf.click()
                # time.sleep(3)
                # slprof = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/div[1]/div/div')
                # slprof.click()
                # time.sleep(3)
                # prof_pic = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[1]/span/div[1]/span/div[1]/div/div[1]/div/input')
                # prof_pic.send_keys(filepath)
                # sleep(10)
                send_button = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')
                send_button.click()
                # send_button = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button')
                # send_button.click()
                counter+=1
            except Exception as e:
                print(e)
    message = f'Messages were send on whatsapp to \n {counter} users'
    driver.get(f'https://web.whatsapp.com/send?phone={send_report}')
    sleep(30)

    driver.find_element_by_xpath('//div[@title = "Type a message"]').send_keys(message)
    sleep(10)
    # send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
    # send_button.click()
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()


# with open('usernames.txt', 'r') as f:
#     usernames = [line.strip() for line in f]





# sending message on instagram
def start_it():
    # CHROME_PROFILE_PATH = "user-data-dir=C:\\Users\\mak\\AppData\\Local\\Google\\Chrome\\User Data\\wtsp"
    options = webdriver.ChromeOptions()
    # options.add_argument(CHROME_PROFILE_PATH)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
  
    counter = 0

    try:

        csvFile = filedialog.askopenfilename()
        df = pd.read_csv(csvFile, encoding="utf-8")
        usernames = df['username'].tolist()
        while True:
            if not usernames:
                print('    Finished Usernames  ................!!!!    ')
                break

            for account in accounts:
                if not usernames:
                    break

                # Auto Login 
                
                insta = InstaDM(username=account["username"],
                                password=account["password"], headless=False)

                for i in range(1000):

                    if not usernames:
                        break

                    username = usernames.pop()
                    # Send message
                    insta.sendMessage(
                        user=username, message=messages)
                    counter+=1

                insta.teardown()
                
                message = f'Messages were send on whatsapp to \n {counter} users.'
                driver.get(f'https://web.whatsapp.com/send?phone={send_report}')
                sleep(30)

                driver.find_element_by_xpath('//div[@title = "Type a message"]').send_keys(message)
                sleep(3)
                # send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
                # send_button.click()
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()



    except:
        df = pd.read_csv(csvFile, encoding="ISO-8859-1")
        usernames = df['username'].tolist()
        while True:
            if not usernames:
                print('    Finished Usernames  ................!!!!    ')
                break

            for account in accounts:
                if not usernames:
                    break

                # Auto Login 
                
                insta = InstaDM(username=account["username"],
                                password=account["password"], headless=False)

                for i in range(1000):

                    if not usernames:
                        break

                    username = usernames.pop()
                    # Send message
                    insta.sendMessage(
                        user=username, message=messages)
                    counter+=1

                insta.teardown()
                
                message = f'Messages were send on whatsapp to \n {counter} users.'
                driver.get(f'https://web.whatsapp.com/send?phone={send_report}')
                sleep(30)

                driver.find_element_by_xpath('//div[@title = "Type a message"]').send_keys(message)
                sleep(3)
                # send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
                # send_button.click()
                driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button').click()



# threading instagram process to prevent from not responding situation
def thred_instagram():
    threading.Thread(target=start_it).start()


# threading whatsapp process to prevent from not responding situation
def thred_whatsapp():
    # threading.Thread(target=whatsa).start()
    whatsa()

button_instagram = Button(w, text='Start The Process For Instagram', bg='#c90076', fg='white', command=thred_instagram)
button_instagram.pack(pady=20)

button_whatsapp = Button(w, text='Start The Process For whatsapp', bg='Green', fg='white', command=thred_whatsapp)
button_whatsapp.pack(pady=20)

send_button = Button(w, text="Start for Telegram", bg='Blue', fg='white', command=send_message_telegram)
send_button.pack(pady=20)

w.mainloop()