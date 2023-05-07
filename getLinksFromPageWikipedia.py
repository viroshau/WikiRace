from __future__ import annotations
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import requests
import time as time
import cchardet as chardet
from dataclasses import dataclass
from queue import Queue, LifoQueue
from typing import List

PAGENAME = 'MissingNo.'
WIKIBASEURL = 'https://en.wikipedia.org'
PAGEURL = WIKIBASEURL + '/wiki/' + PAGENAME
GOALPAGE = "Japanese people"

@dataclass
class Page:
    title: str
    link: str
    parent: str
    history: List[str] #See if we can use this to track the history rather than doing a final traversal backwards

def getAllLinksOnPageInitialVersion(url):
    #GetRequest to the wikipedia page
    allLinksOnPage = {}
    startTime = time.time()
    source = requests.get(url).text
    requestTime = time.time()

    #Get all content on page before See Also, References and External links based on which section appears first
    searchableText = removeSeeAlsoAndReferences(source)
    textSplittingTime = time.time()
    soup = BeautifulSoup(searchableText,'lxml')
    # The maintext is a dic with id "mw-content-text"
    maintext = soup.find_all('div',id='mw-content-text')[0]
    soupTime = time.time()
    for link in maintext.find_all('a'):
        if link.has_attr('href') and link['href'][0:6] == '/wiki/' and ':' not in link['href']:
            allLinksOnPage[link.text] = WIKIBASEURL + link['href']
    afterLoopTime = time.time()
    #print(f'Timing of GET-request: {requestTime - startTime}') 
    #print(f'Timing of textSplitting {textSplittingTime-requestTime}')
    #print(f'Timing of generating soup {soupTime - textSplittingTime}')
    #print(f'Timing of the looping: {afterLoopTime - soupTime}')
    return allLinksOnPage

def getALlLinksOnPage(fromPage, source):
    #Get all content on page before See Also, References and External links based on which section appears first
    searchableText = removeSeeAlsoAndReferences(source)

    allLinksOnPage = []
    soup = BeautifulSoup(searchableText,'lxml')

    # The maintext is a dic with id "mw-content-text"
    maintext = soup.find_all('div',id='mw-content-text')[0]
    for link in maintext.find_all('a'):
        if link.has_attr('href') and link['href'][0:6] == '/wiki/' and ':' not in link['href']:
            allLinksOnPage.append(Page(title = link.text, 
                                              link = WIKIBASEURL + link['href'], 
                                              parent = fromPage.title, 
                                              history= fromPage.history + [link.text]))
    return allLinksOnPage

def getAllLinksOnPageAsDataClasses(fromPage: Page):
    #GetRequest to the wikipedia page
    source = requests.get(fromPage.link).text
    return getALlLinksOnPage(fromPage, source)

async def asyncVersionOfGetAllLinks(fromPage: Page):
    return await asyncio.to_thread(getAllLinksOnPageAsDataClasses, fromPage)

def removeSeeAlsoAndReferences(source):
    seeAlsoSplit = '<span class="mw-headline" id="See_also">'
    referencesSplit = '<span class="mw-headline" id="References">'
    externalLinksSplit = '<span class="mw-headline" id="External_links">'
    
    searchableText = source.split(seeAlsoSplit)[0].split(referencesSplit)[0].split(externalLinksSplit)[0]
    return searchableText

async def asyncrunning(pages):
    return await asyncio.gather(*[asyncVersionOfGetAllLinks(page) for page in pages])

def processForASingleElement(queueOfPages, visitedPages, found, foundPage):
    currentPage = queueOfPages.get() # Deques the first element in the queue. 
    if(currentPage.title not in visitedPages):
        linksOnPage = getAllLinksOnPageAsDataClasses(currentPage) # TODO: This needs to be done asynchronously/ in parallell
        for subPage in linksOnPage: 
            if subPage.title == GOALPAGE:
                print("Completed!")
                found = True
                foundPage = subPage
                break
            queueOfPages.put(subPage)
        visitedPages.add(currentPage.title)
    return found, foundPage


def entireProcedure(PAGENAME, PAGEURL, Page):
    startpage = Page(PAGENAME, PAGEURL, None, history=[PAGENAME])
    
    queueOfPages = Queue()
    queueOfPages.put(startpage)

    visitedPages = set()
    found = False
    foundPage = startpage
    while(queueOfPages.empty()== False and found == False):
        found, foundPage = processForASingleElement(queueOfPages, visitedPages, found, foundPage)
        if found:
            break
    return found, foundPage



async def main(pages, queue):
    for page in pages: 
        await queue.put(page)

if __name__ == "__main__":
    startpage = Page(PAGENAME, PAGEURL, None, history=[PAGENAME])
    f,c = entireProcedure(PAGENAME, PAGEURL, startpage)
    print(f,c)