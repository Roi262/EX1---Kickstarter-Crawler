from bs4 import BeautifulSoup
import requests
import json
import itemPageScrape

source = requests.get('https://www.kickstarter.com/discover/categories/technology').text

soup = BeautifulSoup(source, 'lxml')

# print(soup.prettify())

cards = soup.find_all(class_='js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg')

for card in cards:
    data_project = json.loads(card['data-project'])
    project_url = data_project['urls']['web']['project']

    itemPageScrape.crawlPage(project_url, True)






# print(cards.prettify().split("\"project\":\"")[1].split("\"")[0])
# s = cards.split(',"rewards":')[0].split('"urls":{"web":{"project":')

# k1 = cards.split('data-project=')

# data_project = cards.split('data-project=\'')[1].split(' data-ref=')[0]
# print(data_project)

# cards = soup.find_all('div', {'class': 'js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg'})
# print(cards.prettify())








# print(cards[0])
# for card in cards:
#     links = card.findChildren("a" , recursive=True)
#     print(links)

# print(cards)

# infoText = soup.findAll("table", {"class": "the class"})
