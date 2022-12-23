import asyncio
import aiohttp
import time

PAGENAME = 'Classical_Hollywood_cinema'
WIKIBASEURL = 'https://en.wikipedia.org'
PAGEURL = WIKIBASEURL + '/wiki/' + PAGENAME

urls = [PAGEURL]*300

async def processForLink(session, url):
    async with session.get(url) as response:
         return response.text

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(processForLink(session, url))
            tasks.append(task)
        results = await asyncio.gather(*tasks)

time1 = time.time()
asyncio.run(main())
tome2 = time.time()

print(f'This took {tome2 - time1} amount of seconds')