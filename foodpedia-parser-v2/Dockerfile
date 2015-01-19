FROM python:2

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /usr/local/src/foodpedia-parser-v2/
RUN mkdir -p /upload
RUN touch /upload/dump.ttl
VOLUME /upload

ADD . /usr/local/src/foodpedia-parser-v2/
ENTRYPOINT [ "sh", "./start.sh" ]
CMD [ "Foodstuffs" ]
#CMD [ "Frozen-meat-natural-convenience-foods" ]
