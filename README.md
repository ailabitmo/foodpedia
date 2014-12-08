# [FOODpedia](foodpedia.tk) - a [DBpedia](http://dbpedia.org/) of Food Products
##Data distribution
###Web interface
Search by food page: [http://foodpedia.tk/#/]
###SPARQL protocol endpoint
[http://foodpedia.tk/sparql]
###Mobile application
The idea is to provide to users ability to get data about a product by barcode

##Data gathering
###Parsing of an existing websites
####www.goodsmatrix.ru
*Prerequirements to run parser*
`pip install scrapy`
`pip install rdflib`

*How to run parser*
`cd foodpedia-parser-v2`
`python -m goodsmatrix.main <category> <outputfile>`
Take category name from URL.
e.g.
Milk products category's URL: http://goodsmatrix.ru/goods-catalogue/Milk.html
`python -m goodsmatrix.main Milk milk.ttl`

*How to run unit tests for parser*
Prerequirements:
`pip install mock` (python 2.7)

`cd foodpedia-parser-v2`
`python -m unittest discover -s ./goodsmatrix/test/ -t ./goodsmatrix`

To measure test coverage:
`pip install coverage`
`coverage run -m unittest discover`
`coverage html`

###Crowdsourcing collaboration tool
The idea is to provide to users a simple interface to fill in a data about food
