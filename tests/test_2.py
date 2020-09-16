import asyncio
import concurrent
from asyncio import FIRST_COMPLETED

from timeit import default_timer as timer__
import aiohttp
import async_timeout

_pool = concurrent.futures.ProcessPoolExecutor()


async def fetch(sem, session, url):
    """
    make async request
    """
    async with sem:
        with async_timeout.timeout(15):
            print(f"url: {url}")
            async with session.get(url) as response:
                return url, await response.text()



async def main():
    # https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

    #  limit the amount of concurrent calls
    sem = asyncio.Semaphore(10000)
    chunk_size = 10000
    async with aiohttp.ClientSession() as session:
        n = 0
        tasks = []

        for _ in range(10000):

            n += 1
            task = fetch(sem, session, 'http://0.0.0.0:8080')
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
    start = timer__()


    task_1 = asyncio.create_task(main())

    done, pending = await asyncio.wait({task_1}, return_when=FIRST_COMPLETED)
    print(done)
    print(pending)

    end = timer__()
    print(f"time: {round(end - start, 4)}s")



if __name__ == '__main__':
    try:
        asyncio.run(run())
    except Exception as ex:
        print(ex)
