from coocan import MiniSpider, Request, Response


class TestPrioritySpider(MiniSpider):
    headers_extra_field = {"Name": "Coocan"}

    def start_requests(self):
        for i in range(100):
            url = 'https://www.baidu.com/s?w={}'.format(i)
            yield Request(url, callback=self.parse, priority=100 - i)

    def parse(self, response: Response):
        print(response.request.url)
        print(response.request.headers["User-Agent"])
        print(response.request.headers)
        print()


if __name__ == '__main__':
    s = TestPrioritySpider()
    s.go()
