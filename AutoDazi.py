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

# 参数获取
with open("./conf.yaml", encoding="utf8") as f:
    conf = yaml.safe_load(f)
    print(conf)
    back_pro = conf["back_pro"]
    target_wpm = conf["target_wpm"]
    wpm_change = conf["wpm_change"]
    normal_delay = conf["normal_delay"]
    speed_up = conf["speed_up"]
    speed_down = conf["speed_down"]
    target_change_time = conf["target_change_time"]
    time_change = conf["time_change"]
    max_lines = conf["max_lines"]
    webdriver_setting = conf["webdriver_setting"]
    wait_time = conf["wait_time"]

if webdriver_setting == "Edge":
    driver = webdriver.Edge()
elif webdriver_setting == "Firefox":
    driver = webdriver.Firefox()
elif webdriver_setting == "Chrome":
    driver = webdriver.Chrome()
else:
    logging.error("Driver Name? (Edge or Firefox or Chrome)")

start_flag = 0
def CallBackStartFunc():
    global start_flag
    start_flag = 1

exit_flag = 0
def CallBackExitFunc():
    global exit_flag
    exit_flag = 1

keyboard.add_hotkey("alt+shift+f1",CallBackStartFunc)
keyboard.add_hotkey("alt+shift+esc",CallBackExitFunc)

logging.warning("Start......")
driver.get('https://dazi.kukuw.com/')

logging.warning("Alt+Shift+F1 to Start......")

while start_flag == 0:
    time.sleep(1)


# 获取文章所有文字
logging.warning("Get Article......")

page_source =  driver.page_source
list = []
start = 0
# 最大300行
for id in range(max_lines):
    div_s = page_source.find("<div id=\"i_"+str(id)+"\"",start)
    if div_s == -1:
        break
    # 寻找文字
    wordStart = page_source.find("<span>",div_s) + 6
    wordEnd = page_source.find("</span>",div_s)
    word = page_source[wordStart:wordEnd]
    start = wordEnd
    list.append(word)

print(len(list))
print(list)

# 开始打字

st = time.time()
lt = time.time()
wpm = target_wpm

for num_lines in range(len(list)):
    logging.warning("line %d", num_lines)
    line = list[num_lines]
    print(line)
    for word in line:
        if exit_flag == 1:
            break
        # 速度控制
        if time.time() - st > (target_change_time + 2*time_change*np.random.random()-time_change):
            wpm_random = np.random.normal(0,1)
            if wpm_random < 0:
                wpm = target_wpm + speed_down * wpm_random
            else:
                wpm = target_wpm + speed_up * wpm_random
            print("New TgWPM: " + str(wpm) + " | Practical WPM: " + str(practical_wpm))
            st = time.time()
        time.sleep(60/(wpm+2*wpm_change*np.random.random()-wpm_change))
        driver.switch_to.active_element.send_keys(word)
        # 信息显示
        practical_wpm = 60/(time.time() - lt)
        lt = time.time()
        # 随机退格
        if random.uniform(0,100) <= back_pro and word != line[len(line)-1]:
            time.sleep(normal_delay)
            driver.switch_to.active_element.send_keys(Keys.BACKSPACE)
            time.sleep(normal_delay)
            driver.switch_to.active_element.send_keys(word)
    if exit_flag == 1:
        break

logging.warning("Finish!")
time.sleep(1)
input("Exit?")
