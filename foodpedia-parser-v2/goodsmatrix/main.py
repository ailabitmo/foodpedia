from twisted.internet import reactor
import argparse

from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher

import goodsmatrix.parser


def stop_reactor():
    reactor.stop()

def main():
    command_line_args = parse_arguments()
    dispatcher.connect(stop_reactor, signal=signals.spider_closed)
    spider = goodsmatrix.parser.GoodsMatrixSpider(command_line_args.category)
    settings = get_project_settings()
    settings.set("ITEM_PIPELINES", {
        "goodsmatrix.pipelines.RDFPipeline": 0
    })
    settings.set("OUTPUT_FILENAME", command_line_args.output_filename)
    settings.set("COOKIES_ENABLED", False)
    settings.set("REDIRECT_ENABLED", False)
    crawler = Crawler(settings)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()
    log.start(loglevel='INFO')
    reactor.run() # the script will block here

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('category', help=('goods category name from goodsmatrix.ru.'
                                          'See html filename in URL for needed category'))
    parser.add_argument('output_filename')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
