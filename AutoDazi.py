from numpy.linalg import norm
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import numpy as np
import keyboard
from selenium.webdriver.ie.webdriver import WebDriver
import yaml

import time
import random
import logging

with open("./conf.yaml", encoding="utf8") as f:
    conf = yaml.safe_load(f)
    print(conf)
    BackPro = conf["BackPro"]
    TgWpm = conf["TgWpm"]
    WpmChange = conf["WpmChange"]
    normalDelay = conf["normalDelay"]
    speedUp = conf["speedUp"]
    speedDown = conf["speedDown"]
    TgChangeTime = conf["TgChangeTime"]
    TimeChange = conf["TimeChange"]
    MaxLines = conf["MaxLines"]
    WD = conf["WebDriver"]
    WaitTime = conf["WaitTime"]

if WD == "Edge":
    driver = webdriver.Edge()
elif WD == "Firefox":
    driver = webdriver.Firefox()
elif WD == "Chrome":
    driver = webdriver.Chrome()
else:
    logging.error("Driver Name? (Edge or Firefox or Chrome)")


logging.warning("Start......")
driver.get('https://dazi.kukuw.com/')
logging.warning("Wait " + str(WaitTime) + "s")
time.sleep(WaitTime)
logging.warning("Get Article......")

page_source =  driver.page_source
list = []
start = 0
# 最大300行
for id in range(MaxLines):
    div_s = page_source.find("<div id=\"i_"+str(id)+"\"",start)
    if div_s == -1:
        break
    # 寻找文字
    wordStart = page_source.find("<span>",div_s) + 6
    wordEnd = page_source.find("</span>",div_s)
    word = page_source[wordStart:wordEnd]
    start = wordEnd
    list.append(word)

exit_flag = 0
def callbackfunc():
    global exit_flag
    exit_flag = 1

keyboard.add_hotkey("alt+shift+esc",callbackfunc)

st = time.time()
lt = time.time()
wpm = TgWpm
for numLines in range(len(list)):
    logging.warning("line %d",numLines)
    line = list[numLines]
    for word in line:
        if exit_flag == 1:
            break
        if time.time() - st > (TgChangeTime+TimeChange*np.random.random()-(TimeChange/2)):
            wpm_random = np.random.normal(0,1)
            if wpm_random < 0:
                wpm = TgWpm + speedDown * wpm_random
            else:
                wpm = TgWpm + speedUp * wpm_random
            print("New TgWPM: " + str(wpm) + " | Practical WPM: " + str(exWPM))
            st = time.time()
        time.sleep(60/(wpm+WpmChange*np.random.random()-(WpmChange/2)))
        driver.switch_to.active_element.send_keys(word)
        exWPM = 60/(time.time()-lt)
        lt = time.time()
        if random.uniform(0,100) <= BackPro and word != line[len(line)-1]:
            time.sleep(normalDelay)
            driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
            time.sleep(normalDelay)
            driver.switch_to.active_element.send_keys(word)
    if exit_flag == 1:
        break
logging.warning("Finish!")
time.sleep(1)
input("Exit?")
