import random

from coocan import MiniSpider, Request, Response, IgnoreRequest


class TestReqErrSpider(MiniSpider):
    def start_requests(self):
        for i in range(5):
            url = "https://www.google.com/{}".format(i + 1)
            yield Request(url, callback=self.parse, timeout=1)

    def handle_request_excetpion(self, e: Exception, request: Request):
        v = random.randint(1, 3)
        if v == 1:
            raise IgnoreRequest("出验证码了")
        if v == 2:
            1 / 0
        if v == 3:
            new_url = "https://www.baidu.com/s?wd={}".format(random.randint(1, 100))
            return Request(new_url, callback=self.parse, timeout=1)

    def parse(self, response: Response):
        v = random.randint(1, 2)
        if v == 1:
            print("爬取成功", response.url, len(response.text))
            print(response.get_one("//title/text()"))
        aaa


if __name__ == '__main__':
    my_spider = TestReqErrSpider()
    my_spider.go()
