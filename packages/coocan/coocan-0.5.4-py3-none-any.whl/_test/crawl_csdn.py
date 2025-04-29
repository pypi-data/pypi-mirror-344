import json

from loguru import logger

import coocan
from coocan import Request, MiniSpider

api = "https://blog.csdn.net/community/home-api/v1/get-business-list"
params = {
    "page": "1",
    "size": "20",
    "businessType": "lately",
    "noMore": "false",
    "username": "markadc"
}


class CsdnAirAsyncSpider(MiniSpider):
    start_urls = ['http://www.csdn.net']
    max_requests = 10

    def parse(self, response):
        yield coocan.Request(api, self.parse_page, params=params)

    def middleware(self, request: Request):
        request.headers["Referer"] = "http://www.csdn.net/"

    def parse_page(self, response):
        current_page = params["page"]
        data = json.loads(response.text)
        some = data["data"]["list"]
        if not some:
            logger.warning("没有第 {} 页".format(current_page))
            return
        for one in some:
            date = one["formatTime"]
            name = one["title"]
            detail_url = one["url"]
            yield coocan.Request(detail_url, self.parse_detail)
            print(date, detail_url, name)
        logger.info("第 {} 页抓取成功".format(params["page"]))

        next_page = int(current_page) + 1
        params["page"] = str(next_page)
        yield coocan.Request(api, self.parse_page, params=params)

    def parse_detail(self, response):
        logger.success("{} {}".format(response.status_code, response.request.url))


if __name__ == '__main__':
    s = CsdnAirAsyncSpider()
    s.go()
