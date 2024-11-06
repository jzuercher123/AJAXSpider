import asyncio
import aiohttp
import logging
import json
from urllib.parse import urljoin, urldefrag, urlparse
from bs4 import BeautifulSoup

class AJAXSpider:
    """
    AJAXSpider is an advanced asynchronous web crawler that supports all major HTTP methods.
    It features comprehensive logging, concurrent requests, and outputs results to a JSON file.
    """
    
    def __init__(self, start_url, max_depth=2, concurrency=10, output_file='output.json', log_file='spider.log'):
        """
        Initializes the AJAXSpider instance.
        
        Args:
            start_url (str): The starting URL for the spider.
            max_depth (int): Maximum depth to crawl.
            concurrency (int): Number of concurrent HTTP requests.
            output_file (str): File name for saving crawl results.
            log_file (str): File name for logging activities.
        """
        self.start_url = start_url
        self.max_depth = max_depth
        self.concurrency = concurrency
        self.output_file = output_file
        self.log_file = log_file
        self.visited = set()
        self.results = []
        self.queue = asyncio.Queue()
        self.queue.put_nowait((self.start_url, 0))
        self.session = None
        
        self._configure_logging()
    
    def _configure_logging(self):
        """
        Configures the logging for the spider.
        Logs are written to both the console and a log file.
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def fetch(self, url, method='GET', **kwargs):
        """
        Performs an HTTP request using the specified method.
        
        Args:
            url (str): The URL to request.
            method (str): HTTP method to use.
            **kwargs: Additional arguments for the request.
        
        Returns:
            tuple: A tuple containing (status_code, content, headers) or (None, None, None) on failure.
        """
        try:
            async with self.session.request(method, url, **kwargs) as response:
                content_type = response.headers.get('Content-Type', '')
                if 'text/html' in content_type:
                    text = await response.text()
                else:
                    text = await response.read()
                self.logger.info(f"{method} {url} - Status: {response.status}")
                return response.status, text, response.headers
        except Exception as e:
            self.logger.error(f"Error fetching {url} with method {method}: {e}")
            return None, None, None
    
    def extract_links(self, html, base_url):
        """
        Extracts and resolves links from HTML content.
        
        Args:
            html (str): HTML content to parse.
            base_url (str): Base URL to resolve relative links.
        
        Returns:
            set: A set of absolute, valid URLs extracted from the HTML.
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for tag in soup.find_all(['a', 'link', 'script', 'img']):
            attr = 'href' if tag.name in ['a', 'link'] else 'src'
            link = tag.get(attr)
            if link:
                full_url = urljoin(base_url, link)
                parsed, _ = urldefrag(full_url)
                if self.is_valid(parsed):
                    links.add(parsed)
        return links
    
    def is_valid(self, url):
        """
        Validates whether a URL has an acceptable scheme.
        
        Args:
            url (str): URL to validate.
        
        Returns:
            bool: True if the URL scheme is HTTP or HTTPS, False otherwise.
        """
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https')
    
    async def process_url(self, url, depth):
        """
        Processes a single URL by performing HTTP requests with various methods.
        Extracts new links from GET responses and queues them for further crawling.
        
        Args:
            url (str): The URL to process.
            depth (int): Current depth level of crawling.
        """
        if url in self.visited or depth > self.max_depth:
            return
        self.visited.add(url)
        methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
        for method in methods:
            status, content, headers = await self.fetch(url, method=method)
            if status is not None:
                self.results.append({
                    'url': url,
                    'method': method,
                    'status': status,
                    'headers': dict(headers)
                })
                # For GET requests, attempt to extract further links
                if method == 'GET' and 'text/html' in headers.get('Content-Type', '') and content:
                    links = self.extract_links(content, url)
                    for link in links:
                        await self.queue.put((link, depth + 1))
    
    async def worker(self):
        """
        Worker coroutine that continuously processes URLs from the queue.
        """
        while True:
            try:
                url, depth = await self.queue.get()
                await self.process_url(url, depth)
                self.queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                self.logger.error(f"Unexpected error: {e}")
                self.queue.task_done()
    
    async def run(self):
        """
        Starts the crawling process by initializing the HTTP session and workers.
        Saves the results to a JSON file upon completion.
        """
        connector = aiohttp.TCPConnector(limit_per_host=self.concurrency)
        timeout = aiohttp.ClientTimeout(total=60)
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            self.session = session
            workers = [asyncio.create_task(self.worker()) for _ in range(self.concurrency)]
            await self.queue.join()
            for w in workers:
                w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)
        self.save_results()
    
    def save_results(self):
        """
        Saves the crawl results to a JSON file.
        """
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=4)
            self.logger.info(f"Results saved to {self.output_file}")
        except Exception as e:
            self.logger.error(f"Error saving results: {e}")
