from python:3

WORKDIR /usr/src/

CMD ["python", "-u", "updater-server.py"]

ADD ./updater-server.py /usr/src/updater-server.py
EXPOSE 80
ADD ./.gitconfig /root/.gitconfig
