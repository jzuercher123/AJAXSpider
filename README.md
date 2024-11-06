# AJAXSpider Documentation

**Version:** 1.0  
**Last Updated:** 2024-04-27

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Class Reference](#class-reference)
    - [AJAXSpider](#ajaxspider)
        - [Initialization](#initialization)
        - [Methods](#methods)
            - [`_configure_logging()`](#_configure_logging)
            - [`fetch(url, method='GET', **kwargs)`](#fetchurl-method-get-kwargs)
            - [`extract_links(html, base_url)`](#extract_linkshtml-base_url)
            - [`is_valid(url)`](#is_validurl)
            - [`process_url(url, depth)`](#process_urlurl-depth)
            - [`worker()`](#worker)
            - [`run()`](#run)
            - [`save_results()`](#save_results)
6. [Logging](#logging)
7. [Example](#example)
8. [Dependencies](#dependencies)
9. [License](#license)

---

## Overview

**AJAXSpider** is an advanced asynchronous web crawler designed to efficiently traverse websites using all major HTTP methods. Built on Python's `asyncio` and `aiohttp` libraries, AJAXSpider supports concurrent requests, comprehensive logging, and outputs crawl results in JSON format.

## Features

- **Asynchronous Crawling:** Utilizes `asyncio` for non-blocking operations, enabling high-performance crawling.
- **HTTP Method Support:** Handles `GET`, `POST`, `PUT`, `DELETE`, `HEAD`, and `OPTIONS` requests.
- **Concurrency Control:** Configurable number of concurrent HTTP requests to optimize performance and resource usage.
- **Depth-Limited Crawling:** Restricts crawling to a specified depth to prevent excessive traversal.
- **Link Extraction:** Parses HTML content to extract and resolve links for further crawling.
- **Logging:** Comprehensive logging to both console and log files for monitoring and debugging.
- **Result Storage:** Outputs crawl results, including URLs, HTTP methods, status codes, and headers, to a JSON file.

## Installation

Ensure you have Python 3.7 or higher installed.

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/ajaxspider.git
    cd ajaxspider
    ```

2. **Install Dependencies:**

    It's recommended to use a virtual environment.

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

    *Alternatively, install dependencies manually:*

    ```bash
    pip install aiohttp beautifulsoup4
    ```

## Usage

```python
import asyncio
from ajaxspider import AJAXSpider

async def main():
    spider = AJAXSpider(
        start_url='https://example.com',
        max_depth=3,
        concurrency=20,
        output_file='results.json',
        log_file='spider.log'
    )
    await spider.run()

if __name__ == '__main__':
    asyncio.run(main())
```

## Class Reference

### `AJAXSpider`

`AJAXSpider` is the core class responsible for managing the web crawling process.

#### Initialization

```python
AJAXSpider(
    start_url: str,
    max_depth: int = 2,
    concurrency: int = 10,
    output_file: str = 'output.json',
    log_file: str = 'spider.log'
)
```

**Parameters:**

- `start_url` (`str`): The initial URL from which the spider begins crawling.
- `max_depth` (`int`, optional): The maximum depth to which the spider should crawl. Defaults to `2`.
- `concurrency` (`int`, optional): The number of concurrent HTTP requests. Defaults to `10`.
- `output_file` (`str`, optional): The filename for saving crawl results in JSON format. Defaults to `'output.json'`.
- `log_file` (`str`, optional): The filename for logging spider activities. Defaults to `'spider.log'`.

#### Methods

##### `_configure_logging()`

```python
def _configure_logging(self):
    ...
```

**Description:**  
Configures the logging mechanism for the spider. Logs are output to both the console and the specified log file with a predefined format and INFO level.

##### `fetch(url, method='GET', **kwargs)`

```python
async def fetch(self, url: str, method: str = 'GET', **kwargs) -> tuple:
    ...
```

**Description:**  
Performs an asynchronous HTTP request using the specified method.

**Parameters:**

- `url` (`str`): The URL to send the request to.
- `method` (`str`, optional): The HTTP method to use (`'GET'`, `'POST'`, `'PUT'`, `'DELETE'`, `'HEAD'`, `'OPTIONS'`). Defaults to `'GET'`.
- `**kwargs`: Additional arguments to pass to the request (e.g., headers, data).

**Returns:**  
A tuple containing `(status_code, content, headers)` on success, or `(None, None, None)` on failure.

##### `extract_links(html, base_url)`

```python
def extract_links(self, html: str, base_url: str) -> set:
    ...
```

**Description:**  
Parses HTML content to extract and resolve all valid links.

**Parameters:**

- `html` (`str`): The HTML content to parse.
- `base_url` (`str`): The base URL to resolve relative links.

**Returns:**  
A set of absolute, validated URLs extracted from the HTML content.

##### `is_valid(url)`

```python
def is_valid(self, url: str) -> bool:
    ...
```

**Description:**  
Validates the URL to ensure it uses an acceptable scheme (`http` or `https`).

**Parameters:**

- `url` (`str`): The URL to validate.

**Returns:**  
`True` if the URL scheme is `http` or `https`, `False` otherwise.

##### `process_url(url, depth)`

```python
async def process_url(self, url: str, depth: int):
    ...
```

**Description:**  
Processes a single URL by performing HTTP requests using various methods. For successful `GET` requests with HTML content, it extracts new links and adds them to the queue for further crawling.

**Parameters:**

- `url` (`str`): The URL to process.
- `depth` (`int`): The current depth level of crawling.

##### `worker()`

```python
async def worker(self):
    ...
```

**Description:**  
A worker coroutine that continuously retrieves URLs from the queue and processes them. Multiple workers run concurrently based on the `concurrency` level.

##### `run()`

```python
async def run(self):
    ...
```

**Description:**  
Initiates the crawling process by setting up the HTTP session and worker tasks. It waits for the queue to be exhausted, cancels worker tasks, and saves the crawl results to a JSON file upon completion.

##### `save_results()`

```python
def save_results(self):
    ...
```

**Description:**  
Writes the collected crawl results to the specified JSON output file. Each result includes the URL, HTTP method used, status code, and response headers.

## Logging

AJAXSpider utilizes Python's built-in `logging` module to record its activities. Logs include informational messages about HTTP requests and errors encountered during the crawling process.

- **Log Levels:**
  - `INFO`: General information about the crawling progress (e.g., request statuses).
  - `ERROR`: Issues encountered during HTTP requests or file operations.

- **Log Outputs:**
  - **Console:** Real-time logging output for immediate monitoring.
  - **Log File:** Persistent logging stored in the specified `log_file` (default: `spider.log`).

**Log Format:**

```
%(asctime)s [%(levelname)s] %(message)s
```

*Example:*

```
2024-04-27 12:00:00 [INFO] GET https://example.com - Status: 200
2024-04-27 12:00:05 [ERROR] Error fetching https://example.com/api with method POST: TimeoutError
```

## Example

Below is a comprehensive example demonstrating how to use AJAXSpider to crawl a website:

```python
import asyncio
from ajaxspider import AJAXSpider

async def main():
    # Initialize the spider with desired parameters
    spider = AJAXSpider(
        start_url='https://www.python.org',
        max_depth=3,
        concurrency=15,
        output_file='python_org_results.json',
        log_file='python_org_spider.log'
    )
    
    # Run the spider
    await spider.run()
    
    print(f"Crawling completed. Results saved to {spider.output_file}")

if __name__ == '__main__':
    asyncio.run(main())
```

**Explanation:**

1. **Initialization:**
    - `start_url`: Begins crawling at Python's official website.
    - `max_depth`: Crawls up to 3 levels deep.
    - `concurrency`: Allows up to 15 concurrent HTTP requests.
    - `output_file`: Saves results to `python_org_results.json`.
    - `log_file`: Logs activities to `python_org_spider.log`.

2. **Running the Spider:**
    - Executes the asynchronous `run` method to start crawling.
    - Upon completion, prints a confirmation message with the output file location.

## Dependencies

AJAXSpider relies on the following Python packages:

- **aiohttp:** Asynchronous HTTP client/server framework.

    ```bash
    pip install aiohttp
    ```

- **beautifulsoup4:** Library for parsing HTML and XML documents.

    ```bash
    pip install beautifulsoup4
    ```

- **asyncio:** Standard Python library for writing concurrent code using the async/await syntax. *(Included in Python 3.7+)*
- **logging:** Standard Python library for logging. *(Included in Python 3.7+)*
- **json:** Standard Python library for JSON operations. *(Included in Python 3.7+)*
- **urllib.parse:** Standard Python library for URL parsing. *(Included in Python 3.7+)*

*Ensure all dependencies are installed, preferably within a virtual environment to avoid conflicts.*

## License

This project is licensed under the [MIT License](LICENSE).

---

**Author:** Your Name  
**Contact:** your.email@example.com  
**Repository:** [https://github.com/yourusername/ajaxspider](https://github.com/yourusername/ajaxspider)
