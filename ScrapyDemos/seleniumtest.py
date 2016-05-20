# -*- coding: utf-8 -*-

from selenium import webdriver
import time

#driver = webdriver.PhantomJS()
driver = webdriver.Firefox()
driver.get("http://localhost/Demos/test2.php") 

#获取正文
print driver.find_element_by_tag_name('body').text