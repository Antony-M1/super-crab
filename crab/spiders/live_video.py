import scrapy
from selenium import webdriver


class LiveVideoSpider(scrapy.Spider):
    name = 'live_video'
    allowed_domains = ['youtube.com']
    start_urls = [
        'https://www.youtube.com/watch?v=zblF-wBtnEU',
    ]

    def __init__(self, *args, **kwargs):
        super(LiveVideoSpider, self).__init__(*args, **kwargs)
        self.start_urls = [kwargs.get('start_url')]
        self.driver = webdriver.Chrome()

    def parse(self, response):
        self.driver.get(response.url)
        title = self.driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string')
        description = self.driver.find_element_by_xpath('//*[@id="description"]/yt-formatted-string')
        gps_coordinates = self.driver.find_element_by_xpath('//*[@id="info-text"]/div[1]/yt-formatted-string')
        video_url = self.driver.find_element_by_xpath('//*[@id="player-container-id"]/div[1]/video')
        thumbnail_url = self.driver.find_element_by_xpath('//*[@id="thumbnail"]/img')
        event_timestamp = self.driver.find_element_by_xpath('//*[@id="info-strings"]/yt-formatted-string[1]')

        yield {
            'title': title.text,
            'description': description.text,
            'gps_coordinates': gps_coordinates.get_attribute('data-lat') + ',' + gps_coordinates.get_attribute('data-lon'),
            'video_url': video_url.get_attribute('src'),
            'thumbnail_url': thumbnail_url.get_attribute('src'),
            'event_timestamp': event_timestamp.get_attribute('datetime')
        }

    def closed(self, reason):
        self.driver.quit()
