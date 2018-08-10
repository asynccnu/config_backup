FROM ubuntu:16.04

RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4 \
	&& echo "deb [ arch=amd64,arm64 ] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.0.list \
	&& apt-get update \
	&& apt-get -y install apt-transport-https \
	&& apt-get -y install -y python3-pip python3-dev \
	&& cd /usr/local/bin \
	&& ln -s /usr/bin/python3 python \
	&& pip3 install --upgrade pip \
	&& apt-get -y install mongodb-org-tools=4.0.1 \
	&& apt-get -y install mongodb-org-shell=4.0.1

ENV DEPLOY_PATH /backup
RUN mkdir -p $DEPLOY_PATH
WORKDIR $DEPLOY_PATH
ADD requirements.txt requirements.txt
RUN pip install --index-url http://pypi.doubanio.com/simple/ -r requirements.txt --trusted-host=pypi.doubanio.com
ADD . .
