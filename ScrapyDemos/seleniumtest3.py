# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()
driver.get("http://localhost/demos/htmldemo/index.html") 

try:
    #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "main")))
    # 这里注意，如果页面没有载入完成，调用js函数会报错，解决方法是给对应script标签一个ID，程序中监听当该script段被载入则可以执行对应js
    # 也可以判断该js后面的标签被载入
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "script_main")))
finally:
    #driver.execute_script("document.getElementById('main').style.backgroundColor = 'red';")
    driver.execute_script("changeColor();")

