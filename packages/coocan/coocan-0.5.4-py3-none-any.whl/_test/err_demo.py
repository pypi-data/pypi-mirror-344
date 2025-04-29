from loguru import logger

import coocan
from coocan.spider import MiniSpider


class ErrDemoSpider(MiniSpider):
    start_urls = ["https://cn.bing.com/"]
    max_requests = 5

    def parse(self, response):
        print(response.request.headers.get("User-Agent"))
        logger.debug('{} {}'.format(response.status_code, len(response.text)))
        yield coocan.Request('https://cn.bing.com/', self.parse2, cb_kwargs={"name": "CLOS"})

    def parse2(self, response, name):
        print(name)
        logger.debug('{} {}'.format(response.status_code, len(response.text)))
        yield coocan.Request('https://cn.bing.com/', self.parse3, cb_kwargs={"a1": 1, "a2": 2})

    def parse3(self, response, a1, a22):
        print(a1, a22)


if __name__ == '__main__':
    my_spider = ErrDemoSpider()
    my_spider.go()
