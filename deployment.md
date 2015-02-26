# How to develop and deploy foodpedia.tk
## Web applications
### How to deploy foodpedia localy
#### Prerequirements

You need to have [git](http://git-scm.com/book/en/v2/Getting-Started-Installing-Git), [docker](https://docs.docker.com/installation/#installation) and [fig](http://www.fig.sh/install.html) installed.
#### Deployment
```bash
#1. take the latest sources
git clone git@github.com:ailabitmo/foodpedia.git && cd ./foodpedia
#2. build .war for home page
export M2_REPO=~/.m2/repository/
sudo -E ./foodpedia-home/build.sh development
#3. up whole foodpedia
sudo fig -f fig_development.yml pull
sudo fig -f fig_development.yml up -d
#4. test foodpedia.tk
curl http://localhost
```

### Development cycle for the homepage application
[Deploy foodpedia localy](#how-to-deploy-foodpedia-localy)
```bash
#5. make changes in sources
#6. build .war for home page
sudo -E ./foodpedia-home/build.sh development
#7. rebuild the home image
sudo fig -f fig_development.yml build
#8. restart only home and pathrouther services
sudo fig -f fig_development.yml up -d --no-deps home pathrouter
#9. test changes
curl http://localhost
#10. repeat steps 5 -- 9
#11. commit changes localy
git commit -a -m "some changes"
#12. wait until jobs foodpedia_home_build_war, foodpedia_home_build_testing_docker_image and foodpedia_home_deploy_on_test_server will be finished
#13. test changes on the test server
curl http://109.234.34.200/
#14. if test passed -- deploy to production
```

### How to deploy foodpedia on production server
#### How to deploy from scratch
```bash
# get fig.yml and ./upload directory from sources
git clone https://github.com/ailabitmo/foodpedia.git
cd ./foodpedia
# put the latest data dump to the ./upload directory e.g. with the command
wget --directory-prefix=upload \
http://109.234.34.200:8080/job/foodpedia_parser_run/lastSuccessfulBuild/artifact/upload/Foodstuffs.ttl
# pull latest docker images from dockerhub
sudo fig pull
# up whole application
sudo fig up -d
sudo fig logs
# test foodpedia.tk
curl http://foodpedia.tk
```
#### How to update one service
```bash
# update fig.yml
cd ./foodpedia && git pull
# pull latest containers:
sudo fig pull
# build containers which are not pulled from docker hub
sudo fig build
# up only needed service
# e.g. for home:
sudo fig up -d --no-deps home pathrouter
sudo fig logs
```

### How to upload a data dump to endpoint
#### via docker (on container's start):
place the dump to the directory ./foodpedia/upload/ before running the endpoint service

#### via docker:
after running the endpoint container place the dump to the directory ./foodpedia/upload/
then execute:
```bash
sudo docker exec \
"$(sudo fig -f fig_development.yml ps -q endpoint)" \
sh ./upload_dump.sh
```

#### via web virtuoso's web interface:
go ot http://localhost/conductor
use the [Conductor "Quad Store Upload" tab](http://docs.openlinksw.com/virtuoso/htmlconductorbar.html#rdfadm) feature

## Parser
### Parser for www.goodsmatrix.ru
#### How to run parser
```bash
touch "$(pwd)"/result.ttl
sudo docker run --rm \
-v "$(pwd)"/result.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser <category>
```
Use category's name from goodsmatrix's URL.
##### example: how to parse the Milk category
Milk products category's URL: http://goodsmatrix.ru/goods-catalogue/Milk.html
```bash
touch milk.ttl
sudo docker run --rm \
-v "$(pwd)"/milk.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser Milk
```
#### Development cycle for parser
```bash
#1. Take the latest sources
git clone git@github.com:ailabitmo/foodpedia.git && cd ./foodpedia
#2. Make your changes
#3. Run unit tests:
sudo docker run --rm \
-v "$(pwd)"/foodpedia-parser-v2/:/usr/local/src/foodpedia-parser-v2/ \
chistyakov/foodpedia_goodsmatrix_parser -u
#4. Run manual integration test
touch integration_test_result.ttl
sudo docker run --rm \
-v "$(pwd)"/foodpedia-parser-v2/:/usr/local/src/foodpedia-parser-v2/ \
-v "$(pwd)"/integration_test_result.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser <category>
#Check the integration_test_result.ttl`
#5. If tests passed, commit changes
#6. Check that the Jenkins job [foodpedia_parser_build_docker_image](http://109.234.34.200:8080/job/foodpedia_parser_build_docker_image/) finished successfully
#7. Take the latest image from docker hub
sudo docker pull chistyakov/foodpedia_goodsmatrix_parser
```
