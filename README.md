# SuperFetcher Performance Testing for Fetching Mechanisms in Python

This repository contains Python code for testing the performance of different methods of fetching data from URLs. The tests compare asynchronous fetching using `aiohttp`, multiprocessing using `requests` and `pool system`, and synchronous fetching with `requests`.

## Overview

The code includes:
- **Fetching Class**: Uses asynchronous methods with `aiohttp` to fetch data from multiple URLs concurrently.
- **MultiProcessingPoolFetching Class**: Uses multiprocessing to fetch data from URLs concurrently with `requests`.
- **Unit Tests**: Performance tests to measure and compare the execution time of each fetching method.

## Requirements

To run the tests, you need:
- Python 3.7 or later
- Required Python packages (install using `pip`):

  ```bash
  pip install aiohttp requests
