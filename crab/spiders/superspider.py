import scrapy
import time
from app import get_allowed_domains_and_start_urls, get_name_from_url
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import (
    NoSuchElementException, StaleElementReferenceException
)
from scrapy.selector import Selector
from selenium import webdriver
from crab.utils import constant

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SuperSpider(scrapy.Spider):
    name = "superspider"
    allowed_domains, start_urls, data = get_allowed_domains_and_start_urls()
    custom_settings = {
        'ROBOTSTXT_OBEY': False
    }

    def __init__(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(
            executable_path=constant.DRIVER_PATH_AT_SPIDER,
            chrome_options=chrome_options
        )
        self.is_data_processed = False

    def parse(self, response):
        # opening the page in chrome with respective url
        self.driver.get(response.url)
        time.sleep(3)

        # processing the data and store in dict for data handling
        self.process_data()

        name = get_name_from_url(response._get_url())
        site_data = self.data[name]
        if site_data.get('is_login_required'):
            self.login()

        search_box, xpath = self.find_search_box(response)
        if search_box:
            self.pass_search_query(response, xpath)
        else:
            pass
            """
            if there is no search box checking any other
            video tag is there or not"""

    def process_data(self):
        temp = {}
        if not self.is_data_processed:
            for value in self.data:
                temp[value.get('name')] = value
            self.data = temp
            self.is_data_processed = True
        return

    def login(self):
        pass

    def find_search_box(self, response):
        """
        The search element should be a input tag
        and also there will be 'search' will present in the tag

        Note: Sometimes we are not getting the fully loaded response page.
        for recommended to use the selenium
        """
        sel = Selector(text=self.driver.page_source)
        for xpath in constant.SEARCH_BOX_XPATH:
            try:
                search_box = sel.xpath(xpath)
                if search_box and (len(search_box) == 1):
                    return True, xpath
            except NoSuchElementException:
                continue
        return False, None

    def pass_search_query(self, response, xpath):
        search_box = self.driver.find_element(By.XPATH, xpath)
        recheck = False
        
        for key in constant.SEARCH_KEY:
            # Clear the existing value in the input element
            try:
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)
            except StaleElementReferenceException:
                """
                Some websites even though using the clear method,
                It's appended with the previous value. thats whey
                select all the text and delete.

                """
                search_box = self.driver.find_element(By.XPATH, xpath)
                search_box.send_keys(Keys.CONTROL + "a")
                search_box.send_keys(Keys.DELETE)

            # pass the key in the search box
            search_box.send_keys(key)
            self.driver.implicitly_wait(2)

            # Hit the enter Button
            search_box.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(5)

            # Load the page till the bottom of the page
            for i in range(constant.PAGE_LOAD_LOOP):
                self.driver.execute_script(
                    "window.scrollTo(0, document.documentElement.scrollHeight);"
                )
                time.sleep(3)
