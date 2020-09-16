import asyncio
import concurrent
from asyncio import FIRST_COMPLETED
from itertools import cycle

import aiohttp
import async_timeout

_pool = concurrent.futures.ProcessPoolExecutor()


async def fetch(sem, session, url):
    """
    make async request
    """
    async with sem:
        with async_timeout.timeout(1):
            print(f"url: {url}")
            async with session.get(url) as response:
                return url, await response.text()



async def main():
    # https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html
    # Could be helpful
    # conn = aiohttp.TCPConnector(
    #     family=socket.AF_INET,
    #     ssl=False,
    #     use_dns_cache=False,
    #     limit=100
    # )

    #  limit the amount of concurrent calls
    sem = asyncio.Semaphore(500)
    chunk_size = 500
    async with aiohttp.ClientSession() as session:
        n = 0
        tasks = []

        for url in cycle(['http://0.0.0.0:8080']):
            n += 1
            task = fetch(sem, session, url)
            tasks.append(task)
            if n > chunk_size:
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                for r in responses:
                    print(f"r: {r}")
                n = 0
                tasks.clear()

        responses = await asyncio.gather(*tasks, return_exceptions=True)
        print(responses)


async def run():
    task_1 = asyncio.create_task(main())

    done, pending = await asyncio.wait({task_1}, return_when=FIRST_COMPLETED)
    print(done)
    print(pending)


if __name__ == '__main__':
    try:
        asyncio.run(run())
    except Exception as ex:
        print(ex)
