from coocan import MiniSpider, Request, Response


class TestReqDelaySpider(MiniSpider):
    max_requests = 5
    delay = 3

    def start_requests(self):
        for i in range(100):
            url = 'https://www.baidu.com/s?w={}'.format(i)
            yield Request(url, callback=self.parse, priority=100 - i)

    def parse(self, response: Response):
        print(response.request.url)


if __name__ == '__main__':
    s = TestReqDelaySpider()
    s.go()
