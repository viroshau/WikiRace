from bs4 import BeautifulSoup
import requests
import time as time

PAGENAME = 'Arfaoui'
WIKIBASEURL = 'https://en.wikipedia.org'
PAGEURL = WIKIBASEURL + '/wiki/' + PAGENAME

def getAllLinksOnPage(url):
    #GetRequest to the wikipedia page
    allLinksOnPage = {}
    source = requests.get(url).text

    #Get all content on page before See Also, References and External links based on which section appears first
    seeAlsoSplit = '<span class="mw-headline" id="See_also">'
    referencesSplit = '<span class="mw-headline" id="References">'
    externalLinksSplit = '<span class="mw-headline" id="External_links">'

    searchableText = source.split(seeAlsoSplit)[0].split(referencesSplit)[0].split(externalLinksSplit)[0]
    soup = BeautifulSoup(searchableText,'lxml')

    # The maintext is a dic with id "mw-content-text"
    maintext = soup.find_all('div',id='mw-content-text')[0]
    for link in maintext.find_all('a'):
        if link.has_attr('href') and link['href'][0:6] == '/wiki/' and ':' not in link['href']:
            allLinksOnPage[link.text] = WIKIBASEURL + link['href']
    return allLinksOnPage

def linksOnPageBasedOnPTagsOnly(soup):
    linksOnPageInternal = {}
    paragraphs = soup.find_all("p")
    for paragraph in paragraphs:
        for anchor in paragraph.find_all('a'):
            if anchor.has_attr('href') and anchor['href'][0:6] == '/wiki/':
                linksOnPageInternal[anchor.text] = WIKIBASEURL + anchor['href']
    return linksOnPageInternal