# -*- coding: utf-8 -*-

from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='D:/Program Files/phantomjs-2.1.1-windows/bin/phantomjs.exe')
#http://localhost/demos/test2/index.php
driver.get("https://www.baidu.com/") 

print driver.find_element_by_tag_name('body').text
print driver.find_element_by_tag_name('body').tag_name


driver.save_screenshot('screenshot.png')


driver.quit()