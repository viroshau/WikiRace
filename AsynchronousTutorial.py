import asyncio
import bs4 as beautifulsoup
import aiohttp

async def producer(queue):
    while True:
        await queue.put("https://www.google.com")
        await asyncio.sleep(1)

async def consumer(queue):
    while True:
        url = await queue.get()
        print('Start fetching: ' + url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                content = await response.read()
                try:
                    soup = beautifulsoup.BeautifulSoup(content, "html.parser")
                    print(str(soup))
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
                queue.task_done()

def main():
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()

    loop.create_task(producer(queue))
    loop.create_task(consumer(queue))
    loop.run_forever()

if __name__ == '__main__':
    main()