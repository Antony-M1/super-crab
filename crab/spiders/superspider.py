import scrapy
from app import get_allowed_domains_and_start_urls, get_name_from_url
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from scrapy.selector import Selector
from selenium import webdriver
from crab.utils import constant


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

    def parse(self, response):

        # opening the page in chrome with respective url
        self.driver.get(response.url)

        # processing the data and store in dict for data handling
        self.process_data()

        name = get_name_from_url(response._get_url())
        site_data = self.data[name]
        if site_data.get('is_login_required'):
            self.login()

        search_box, xpath = self.find_search_box()
        if search_box:
            pass
        else:
            """
            if there is no search box checking any other
            video tag is there or not"""

    def process_data(self):
        temp = {}
        for value in self.data:
            temp[value.get('name')] = value
        self.data = temp

    def login(self):
        pass

    def find_search_box(self):
        """
        The search element should be a input tag
        and also there will be 'search' will present in the tag
        """
        for xpath in constant.SEARCH_BOX_XPATH:
            try:
                search_box = self.driver.find_element(By.XPATH, xpath)
                if search_box:
                    return True, xpath
            except NoSuchElementException:
                continue
        return False, None
