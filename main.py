import time
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get('https://www.reddit.com/top/?t=month');
time.sleep(5) # Let the user actually see something!
driver.quit()
