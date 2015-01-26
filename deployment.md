# How to develop and deploy foodpedia.tk
## Web applications
### How to run the home application
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
[Run endpoint](### How to run virtuoso endpoint)

[Upload a data to the endpoint](#### How to upload data dump to the local endpoint)

[Run pubby](### How to run pubby localy)
##### Build .war file for the home application
```
# use the 'development' maven profile.
sudo ./foodpedia-home/build.sh development
```
##### Prepare context for the foodpedia-home image
```
mv ./foodpedia-home/foodpedia-home-development.war ./foodpedia-home/ROOT.war
```

##### Build image and run the homepage container
```
sudo docker build -t foodpedia_home_development ./foodpedia-home/

sudo docker run --name home \
-d -p 9090:8080 foodpedia_home_development

#go to http://localhost:9090/
```

### Development cycle for the homepage application
```
#1. take the latest sources
git clone git@github.com:ailabitmo/foodpedia.git && cd ./foodpedia
#2. build foodpedia-home with maven
sudo docker run -i -t --rm \
  -v "$(pwd)"/foodpedia-home:/usr/src/mymaven \
  -v $M2_REPO:/root/.m2/repository/ \
  -w /usr/src/mymaven \
  maven:3.2-jdk-7 \
  mvn clean package -P development
#3. run foodpedia-home from the image
#mount the /usr/local/tomcat/webapps/ROOT/ directory to the built project's target directory
sudo docker run -d \
  -v "$(pwd)"/foodpedia-home/target/foodpedia-home-1.0-SNAPSHOT/:/usr/local/tomcat/webapps/ROOT/ --name home \
  -p 9090:8080  chistyakov/foodpedia_home_testing
#4. test application
curl -i http://localhost:9090
#5. make changes in sources
#6. repeat the step 3 (build foodpedia-home with maven).
#7. restart the home container
sudo docker restart home
#8. repeat steps 4 -- 7
#9. commit changes
git commit -a -m "some changes"
#10. wait until the build and deploy jobs for testing environment will be finished
#11. test changes on the testing environment
#12. if test passed -- deploy to production
```


### How to run virtuoso endpoint
```
sudo docker pull chistyakov/foodpedia_virtuoso_ontowiki
sudo docker run --name endpoint -d -p 8008:80 -p 8890:8890 \
-v "$(pwd)"/upload/:/upload/ chistyakov/foodpedia_virtuoso_ontowiki
#go to http://localhost:8890/sparql for sparql endpoint
#go to http://localhost:8890/conductor for virtuoso web interface
#go to http://localhost:80 for ontowiki
```
#### How to upload data dump to the local endpoint
##### via docker (on container's start):
place the dump to the "$(pwd)"/upload/ directory before runing the endpoint container
##### via docker:
after running the endpoint container place the dump to "$(pwd)"/upload/ directory
then execute:
```
sudo docker exec endpoint sh ./upload_dump.sh
```
##### via web virtuoso's web interface:
go ot http://localhost:8890/conductor
use the [Conductor "Quad Store Upload" tab](http://docs.openlinksw.com/virtuoso/htmlconductorbar.html#rdfadm) feature

### How to run pubby localy
```
sudo docker pull chistyakov/foodpedia_pubby
sudo docker run --name pubby -p 8090:8080 -d --link endpoint:endpoint chistyakov/foodpedia_pubby http://localhost:8090
#check http://localhost:8090. Note, it will return 404 not found if there aren't uploaded to endpoint data.
#the passed parameter (http://localhost:8090) will be used as homepage and webbase uri
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
##### example: how to parse the Milk category
Milk products category's URL: http://goodsmatrix.ru/goods-catalogue/Milk.html
```
touch milk.ttl
sudo docker run --rm \
-v "$(pwd)"/milk.ttl:/upload/dump.ttl \
chistyakov/foodpedia_goodsmatrix_parser Milk
```
#### Development cycle for parser
```
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
