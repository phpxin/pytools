# -*- coding: utf-8 -*-

from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path='')
driver.get("http://localhost/Demos/test2.php") 

print driver.