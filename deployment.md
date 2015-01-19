# How to develop foodpedia.tk
## Web applications
### How to run homepage localy
#### Run with production backend
```
git clone git@github.com:ailabitmo/foodpedia.git && cd ./foodpedia

sudo docker pull chistyakov/foodpedia_home_production
sudo docker run --name home \
-d -p 9090:8080 chistyakov/foodpedia_home_production

#go to http://localhost:9090/
```
#### Run with testing backend 
```
git clone git@github.com:ailabitmo/foodpedia.git && cd ./foodpedia

sudo docker pull chistyakov/foodpedia_home_testing
sudo docker run --name home \
-d -p 9090:8080 chistyakov/foodpedia_home_testing

#go to http://localhost:9090/
```
#### Run with local backend
```
git clone git@github.com:ailabitmo/foodpedia.git && cd ./foodpedia

#run virtuoso endpoint
sudo docker pull chistyakov/foodpedia_virtuoso_ontowiki
sudo docker run --name endpoint -d -p 8008:80 -p 8890:8890 \
-v "$(pwd)"/upload/:/upload/ chistyakov/foodpedia_virtuoso_ontowiki
#check http://localhost:8890/sparql

#upload a data dump to the endpoint
##first way via docker:
###place it to the "$(pwd)"/upload/ directory before runing the endpoint container
#
##second way via docker:
###after running the endpoint container place the dump to "$(pwd)"/upload/ directory
###then execute: sudo docker exec endpoint sh ./upload_dump.sh
#
##third way via web virtuoso's web interface:
###go ot http://localhost:8890/conductor
###use [Conductor "Quad Store Upload" tab](http://docs.openlinksw.com/virtuoso/htmlconductorbar.html#rdfadm) 

#run pubby
sudo docker pull chistyakov/foodpedia_pubby
sudo docker run --name pubby -p 8090:8080 -d --link endpoint:endpoint chistyakov/foodpedia_pubby http://localhost:8090
#check http://localhost:8090. Note, it will return 404 not found if there aren't uploaded to endpoint data.

#build war file for the home application with 'development' maven profile.
sudo ./foodpedia-home/build.sh development
#or
cd ./foodpedia-home/
mvn clean install -P development
cp ./target/foodpedia-home-1.0-SNAPSHOT.war ../foodpedia-home/foodpedia-home-development.war
cd ../

mv ./foodpedia-home/foodpedia-home-development.war ./foodpedia-home/ROOT.war
sudo docker build -t foodpedia_home_development ./foodpedia-home/

sudo docker run --name home \
-d -p 9090:8080 foodpedia_home_development

#go to http://localhost:9090/
```

## Parser
### Parse www.goodsmatrix.ru
#### How to run parser

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

#### How to develop the parser

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
