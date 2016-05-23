# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://localhost/demos/test2/index.php") 

try:
    # WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.TAG_NAME, "a")))
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "login")))
finally:
    elem = driver.find_element_by_tag_name('a')
    elem.click()

try:
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, "uname")))
finally:
    elem_name = driver.find_element_by_name('uname')
    elem_pwd = driver.find_element_by_name('pwd')
    elem_name.send_keys('123123')
    elem_pwd.send_keys('aaaaa')  
    driver.find_element_by_id('sub').click()

driver.save_screenshot('screenshot.png')        #保存屏幕快照
#driver.quit()        #退出浏览器
