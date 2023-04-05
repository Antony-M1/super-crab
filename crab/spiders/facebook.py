import scrapy
from crab.utils import constant
from selenium import webdriver
from scrapy.selector import Selector


class FacebookSpider(scrapy.Spider):
    name = "facebook"
    allowed_domains = ["facebook.com"]
    start_urls = ["https://www.facebook.com/login/"]

    def __init__(self):
        self.driver = webdriver.Chrome('./chromedriver_linux64/chromedriver')

    def start_requests(self):
        login_url = 'https://www.facebook.com/login.php'
        yield scrapy.FormRequest(login_url, formdata={
            'email': constant.FACEBOOK_EMAIL,
            'password': constant.FACEBOOK_PASSWORD
        }, callback=self.after_login)

    def after_login(self, response):
        page_url = 'https://www.facebook.com/'
        yield scrapy.Request(page_url, callback=self.parse)

    def parse(self, response):
        # live_stream_url = response.xpath(
        #                     "//script[contains(.,'hd_src')]/text()"
        #                 ).re_first(r'hd_src:"([^"]+)"')
        # yield {'live_stream_url': live_stream_url}
        self.driver.get(response.url)
        self.driver.find_element_by_id('email').send_keys('your_email')
        self.driver.find_element_by_id('pass').send_keys('your_password')
        self.driver.find_element_by_id('loginbutton').click()
        sel = Selector(text=self.driver.page_source)
