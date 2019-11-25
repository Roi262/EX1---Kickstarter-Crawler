from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import math
import time
import itemPageScrape

CARDS_PER_PAGE = 12
TOTAL_CARDS_TO_COUNT = 300
LOAD_MORE_COUNT = math.ceil(TOTAL_CARDS_TO_COUNT/CARDS_PER_PAGE)

# Initializing Google Chrome Webdriver
chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path='chromedriver')

# Instatiating driver with kickstarter url
url = 'https://www.kickstarter.com/discover/categories/technology'
driver.get(url)
time.sleep(2)


# Pressing load more to load at least 300 cards
load_more_button = driver.find_element_by_css_selector('.bttn-medium')
for i in range(LOAD_MORE_COUNT):
    load_more_button.click()
    time.sleep(5)

project_cards = driver.find_elements_by_css_selector(".grid-col-4-lg")

# for project in project_cards:
#     print(json.dumps(itemPageScrape.crawlPage(project_url)))
#     time.sleep(5)


