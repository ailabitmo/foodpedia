# [FOODpedia](foodpedia.tk) - a [DBpedia](http://dbpedia.org/) of Food Products
## Data providing
### Web interface
Search food by name or barcode: [http://foodpedia.tk/#/](http://foodpedia.tk/#/)
### SPARQL protocol endpoint
[http://foodpedia.tk/sparql](http://foodpedia.tk/sparql)
### Mobile application
The idea is to provide to users ability to get data about a product by scanned barcode

## Data gathering
### Parsing of an existing websites
#### www.goodsmatrix.ru
**How to run parser**

```
touch "$(pwd)"/result.ttl
sudo docker run --rm \
-v "$(pwd)"/result.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser <category>
```

Use category's name from goodsmatrix's URL.
> e.g. Milk products category's URL: http://goodsmatrix.ru/goods-catalogue/Milk.html

> ```
touch milk.ttl
sudo docker run --rm \
-v "$(pwd)"/milk.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser Milk
```

**How to develop the parser**

* `git clone git@github.com:ailabitmo/foodpedia.git`
* `cd foodpedia`
* `#Make your changes`
* `#Run unit tests:`
```
sudo docker run --rm \
-v "$(pwd)"/foodpedia-parser-v2/:/usr/local/src/foodpedia-parser-v2/ \
chistyakov/foodpedia_goodsmatrix_parser -u
```

* `#Run manual integration test:`
```
touch integration_test_result.ttl
sudo docker run --rm \
-v "$(pwd)"/foodpedia-parser-v2/:/usr/local/src/foodpedia-parser-v2/ \
-v "$(pwd)"/integration_test_result.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser <category>
```
`#Check the integration_test_result.ttl`
* `#If ok, commit changes`
* `#Check that the Jenkins job` [`foodpedia_parser_build_docker_image`](http://109.234.34.200:8080/job/foodpedia_parser_build_docker_image/) `finished successfully`
* `sudo docker pull chistyakov/foodpedia_goodsmatrix_parser`


### Crowdsourcing collaboration tool
The idea is to provide to users a simple interface to fill in a data about food
