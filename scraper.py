from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import time
# from time import sleep
import itemPageScrape

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

MAIN_URL = 'https://www.kickstarter.com/discover/categories/technology'

driver = webdriver.Safari()
driver.get(MAIN_URL)
for i in range(10):
    driver.find_element_by_class_name('load_more.mt3').click()
soup = BeautifulSoup(driver.page_source, 'lxml')


# load_more_button = driver.find_element_by_xpath('//*[@id="text"]')
# load_more_button.click()
# load_more_button.click()
# k = driver.page_source

# source = requests.get(MAIN_URL).text

cards = soup.find_all(
    class_='js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg')

for card in cards:
    data_project = json.loads(card['data-project'])
    project_url = data_project['urls']['web']['project']
    print(json.dumps(itemPageScrape.crawlPage(project_url)))
    time.sleep(5)



# infoText = soup.findAll("table", {"class": "the class"})
