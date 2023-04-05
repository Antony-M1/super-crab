import scrapy
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from crab.utils import constant


class YoutubeSpider(scrapy.Spider):
    name = "youtube"
    allowed_domains = ["youtube.com"]
    raw_url = "http://www.youtube.com"
    start_urls = [
        'https://www.youtube.com/results?search_query=',
    ]
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self):
        # self.driver = webdriver.Chrome(constant.DRIVER_PATH_AT_SPIDER)
        chrome_options = Options()
        # chrome_options.add_argument("--headless") # Run Selenium in headless mode
        self.driver = webdriver.Chrome(
            executable_path=constant.DRIVER_PATH_AT_SPIDER,
            chrome_options=chrome_options
        )

    def parse(self, response):
        # self.login()
        self.driver.get(response.url)

        # Search for a keyword (e.g., "live stream")
        search_input = self.driver.find_element(By.XPATH, '//*[@id="search"]//input[@id="search"]')
        search_input.send_keys('live stream')
        time.sleep(1)
        search_input.send_keys(Keys.ENTER)
        self.driver.implicitly_wait(5)
        time.sleep(5)
        # Scroll down to load more videos
        for i in range(20):
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            self.driver.implicitly_wait(5)
            time.sleep(3)

        # Extract metadata and live stream links
        html = self.driver.page_source
        sel = Selector(text=html)
        videos = sel.xpath('//*[@id="contents"]/ytd-video-renderer')
        for video in videos:
            if video.xpath(".//span[@class='style-scope ytd-badge-supported-renderer']/text()").get() != 'LIVE':
                continue

            title = video.xpath('.//a[@id="video-title"]/@title').extract()
            url = video.xpath('.//a[@id="video-title"]/@href').extract()
            self.driver.get(self.raw_url + url[0])
            # time.sleep(2)

            yield {
                'title': title,
                'url': self.raw_url + url[0],
            }

    def closed(self, reason):
        self.driver.quit()

    def login(self):
        self.driver.get(constant.YOUTUBE_SIGNIN_PAGE)
        # search = self.driver.find_element(By.XPATH, '//input[@id="input"]')
        # search = self.driver.find_element(By.XPATH, '//*[@id="APjFqb"]')
        # self.driver.implicitly_wait(5)
        # time.sleep(2)
        # search.send_keys('gmail signin')
        # search.send_keys(Keys.ENTER)

        # email = self.driver.find_element(By.XPATH, '//*[@id="identifierId"]')
        # email.send_keys(constant.GMAIL)
        # # next_btn = self.driver.find_element(By.XPATH, '//*[@id="identifierNext"]')
        # next_btn = self.driver.find_element(By.XPATH, '//div[@class="FliLIb FmFZVc"]')
        # next_btn.click()

        # time.sleep(2)

        # password = self.driver.find_element(By.NAME, "Passwd")
        # password.send_keys(constant.GMAIL_PASSWORD)
        # next_btn = self.driver.find_element(By.XPATH, '//*[@id="passwordNext"]')
        # next_btn.click()

        # time.sleep(5)
        


        # Create a new instance of the Chrome driver
        driver = webdriver.Chrome()

        # Navigate to the Gmail login page
        driver.get("https://accounts.google.com/signin")

        # Find the email input field and enter the email address
        email_input = driver.find_element(By.NAME, "identifier")
        email_input.send_keys(constant.GMAIL)
        email_input.send_keys(Keys.RETURN)

        # Wait for the password input field to appear
        time.sleep(3)

        # Find the password input field and enter the password
        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(constant.GMAIL_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        # Wait for the Gmail inbox to load
        time.sleep(5)

        # Navigate to the YouTube homepage
        driver.get("https://www.youtube.com/")

        # Find the search box and enter a query
        search_box = driver.find_element_by_name("search_query")
        search_box.send_keys("Python tutorial")
        search_box.send_keys(Keys.RETURN)

        # Find the search results and extract the titles and URLs
        results = driver.find_elements_by_css_selector("a#video-title")
        titles = [result.get_attribute("title") for result in results]
        urls = [result.get_attribute("href") for result in results]

        # Store the titles and URLs in a CSV file
        with open("youtube_results.csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["Title", "URL"])
            for title, url in zip(titles, urls):
                writer.writerow([title, url])

        # Close the browser window
        driver.quit()