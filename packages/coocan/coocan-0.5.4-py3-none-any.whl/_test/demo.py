from loguru import logger

import coocan


class DemoSpider(coocan.MiniSpider):
    start_urls = ["https://cn.bing.com/"]
    max_requests = 5

    def parse(self, response):
        print(response.request.headers.get("User-Agent"))
        logger.debug('{} {}'.format(response.status_code, len(response.text)))
        for i in range(5):
            yield coocan.Request('https://cn.bing.com/', self.parse2)

    def parse2(self, response):
        logger.info('{} {}'.format(response.status_code, len(response.text)))
        for i in range(3):
            yield coocan.Request('https://cn.bing.com/', self.parse3)

        for i in range(4):
            yield coocan.Request('https://cn.bing.com/', self.parse4)

    def parse3(self, response):
        logger.warning('{} {}'.format(response.status_code, len(response.text)))

    def parse4(self, response):
        logger.error('{} {}'.format(response.status_code, len(response.text)))


if __name__ == '__main__':
    my_spider = DemoSpider()
    my_spider.go()
