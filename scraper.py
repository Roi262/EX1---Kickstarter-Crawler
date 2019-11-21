from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import json
import time
import itemPageScrape

from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

MAIN_URL = 'https://www.kickstarter.com/discover/categories/technology'

driver = webdriver.Safari()
driver.get(MAIN_URL)


button_class = driver.find_element_by_class_name('load_more.mt3').click()
# load_more_button = driver.find_element_by_xpath('//*[@id="text"]')
# load_more_button.click()
# load_more_button.click()
# kkk = driver.page_source

# source = requests.get(MAIN_URL).text
soup = BeautifulSoup(driver.page_source, 'lxml')

cards = soup.find_all(
    class_='js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg')

for card in cards:
    data_project = json.loads(card['data-project'])
    project_url = data_project['urls']['web']['project']

    itemPageScrape.crawlPage(project_url, True)


# infoText = soup.findAll("table", {"class": "the class"})
