from twisted.internet import reactor
import argparse

from scrapy.crawler import Crawler
from scrapy import log, signals
from scrapy.utils.project import get_project_settings
from scrapy.xlib.pydispatch import dispatcher

import goodsmatrix.spider


def stop_reactor():
    reactor.stop()

def main():
    command_line_args = parse_arguments()

    dispatcher.connect(stop_reactor, signal=signals.spider_closed)

    spider = goodsmatrix.spider.GoodsMatrixSpider(command_line_args.category)

    settings = get_project_settings()
    pipelines_order_dict = {
            "goodsmatrix.pipelines.postprocessors.UnescapeSpecialHTMLEntities": 2,
            "goodsmatrix.pipelines.postprocessors.ExtractEsl": 3,
            "goodsmatrix.pipelines.postprocessors.ExtractEAdditives": 4,
            "goodsmatrix.pipelines.postprocessors.StripMultilineStringProperties": 5,
            "goodsmatrix.pipelines.postprocessors.ExtractIngredients": 6,
        }
    if command_line_args.persistence:
        pipelines_order_dict["goodsmatrix.pipelines.writers.PersistentRDFPipeline"] = 10
    else:
        pipelines_order_dict["goodsmatrix.pipelines.writers.InMemoryRDFPipeline"] = 10

    if command_line_args.agrovoc_endpoint:
        settings.set("AGROVOC_ENDPOINT", command_line_args.agrovoc_endpoint)

    if command_line_args.api_key:
        pipelines_order_dict["goodsmatrix.pipelines.postprocessors.Translator"] = 7
        settings.set("YANDEX_TRANSLATE_API_URI", command_line_args.api_key)
    settings.set("ITEM_PIPELINES", pipelines_order_dict)

    if command_line_args.old_endpoint:
        pipelines_order_dict["goodsmatrix.pipelines.postprocessors.SkipIfExistsInOldGraph"] = 1
        settings.set("OLD_ENDPOINT_URI", command_line_args.old_endpoint)

    settings.set("OUTPUT_FILENAME", command_line_args.output_filename)
    settings.set("COOKIES_ENABLED", False)
    settings.set("REDIRECT_ENABLED", False)
    settings.set("LOG_FORMATTER", "goodsmatrix.spider.PoliteLogFormatter")

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
    parser.add_argument('-k', '--api_key', help='yandex translator api key')
    parser.add_argument('-p', '--persistence', help='use persistence store (SleepyCat) for parsed items', action='store_true')
    parser.add_argument('-a', '--agrovoc_endpoint', help='URI of agrovoc endpoint')
    parser.add_argument('-o', '--old_endpoint', help='URI of an endpoint with old graph')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
