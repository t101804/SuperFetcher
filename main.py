import asyncio
from multiprocessing import Pool
import re
import aiohttp
import time
import unittest
import requests
from unittest.mock import patch

class Fetching:
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def fetch(self, url):
        async with self.session.get(url) as response:
            return await response.text()

    async def fetch_multiple(self, urls):
        tasks = [self.fetch(url) for url in urls]
        return await asyncio.gather(*tasks)

    async def run(self, urls:list, chunk:int=2):
        chunk_size = len(urls) // chunk
        chunks = [urls[:chunk_size], urls[chunk_size:]]

        tasks = [self.fetch_multiple(chunk) for chunk in chunks]
        results = await asyncio.gather(*tasks)
        total = 0
        for result in results:
            for response in result:
                title = re.findall(r'<title>(.*)</title>', response)
                if title:
                    total += 1
        print(f"Fetched {total} titles")

class MultiProcessingPoolFetching:
    def __init__(self, urls):
        self.urls = urls

    def fetch(self, url):
        return requests.get(url).status_code

    def run(self):
        with Pool(processes=2) as pool:
            for status in pool.map(self.fetch, self.urls):
                print(status)

class TestFetchingPerformance(unittest.TestCase):
    
    def setUp(self):
        self.web_list = [
            'https://www.google.com',
            'https://www.youtube.com',
            'https://www.wikipedia.org',
            'https://www.github.com',
            'https://www.reddit.com',
            'https://www.stackoverflow.com'
        ] * 100  # Testing with 600 URLs

    def test_fetch_performance(self):
        start_time = time.time()
        print("Starting async fetch test...")
        try:
            async def run_fetching():
                async with Fetching() as fetcher:
                    await fetcher.run(self.web_list)
            asyncio.run(run_fetching())
        except Exception as e:
            print(f"An error occurred: {e}")
        
        elapsed_time = time.time() - start_time
        print(f"Elapsed time for async fetching: {elapsed_time:.2f} seconds")
        self.assertLess(elapsed_time, 10, "Async fetching took too long!")

    def test_multiprocessing_pool_fetch_performance(self):
        start_time = time.time()
        print("Starting multiprocessing pool fetch test...")
        mp = MultiProcessingPoolFetching(self.web_list)
        mp.run()
        elapsed_time = time.time() - start_time
        print(f"Elapsed time for multiprocessing pool fetching: {elapsed_time:.2f} seconds")
        self.assertLess(elapsed_time, 10, "Multiprocessing pool fetching took too long!")

    def test_normal_fetch_performance(self):
        start_time = time.time()
        print("Starting normal fetch test...")
        for url in self.web_list:
            requests.get(url)
        elapsed_time = time.time() - start_time
        print(f"Elapsed time for normal fetching: {elapsed_time:.2f} seconds")
        self.assertLess(elapsed_time, 10, "Normal fetching took too long!")

if __name__ == "__main__":
    unittest.main()
