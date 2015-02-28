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
    pipelines_order_dict = {
            "goodsmatrix.pipelines.postprocessors.ExtractEslPipeline": 1,
            "goodsmatrix.pipelines.postprocessors.ExtractEAdditives": 2,
            "goodsmatrix.pipelines.postprocessors.StripMultilineStringProperties": 3
        }
    if command_line_args.persistence:
        pipelines_order_dict["goodsmatrix.pipelines.writers.PersistentRDFPipeline"] = 10
    else:
        pipelines_order_dict["goodsmatrix.pipelines.writers.InMemoryRDFPipeline"] = 10
    settings.set("ITEM_PIPELINES", pipelines_order_dict)

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
    parser.add_argument('-p', '--persistence', help='use persistence store (SleepyCat) for parsed items', action='store_true')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
