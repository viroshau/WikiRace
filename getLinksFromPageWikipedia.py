from bs4 import BeautifulSoup
import requests

WIKIBASEURL = 'https://en.wikipedia.org'
PAGEURL = 'https://en.wikipedia.org/wiki/MissingNo.'
source = requests.get(PAGEURL).text

soup = BeautifulSoup(source,'lxml')

k = 0
linksOnPage = {}
paragraphs = soup.find_all("p")
for paragraph in paragraphs:
    for anchor in paragraph.find_all('a'):
        if anchor.has_attr('href'):
            if anchor['href'][0:6] == '/wiki/':
                linksOnPage[anchor.text] = anchor['href']
                k +=1
print(linksOnPage)