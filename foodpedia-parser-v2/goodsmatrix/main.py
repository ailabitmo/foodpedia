from twisted.internet import reactor

from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher

import goodsmatrix.parser


def stop_reactor():
    reactor.stop()

def main():
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    spider = goodsmatrix.parser.GoodsMatrixSpider()
    settings = get_project_settings()
    #settings.set("FEED_FORMAT", "json")
    #settings.set("FEED_URI", "result.json")
    settings.set("ITEM_PIPELINES", {
        "goodsmatrix.pipelines.JsonWithEncodingPipeline": 0
    })

    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start()
    reactor.run() # the script will block here


if __name__ == "__main__":
    main()
