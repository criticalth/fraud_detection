# dockerfile

FROM ubuntu:bionic

RUN \
	apt update && \
	apt-get install -y python3-pip

RUN mkdir opt/project

COPY . opt/project/

RUN pip3 install -r opt/project/requirements.txt

ENV PYTHONPATH opt/project

CMD ["python3"]
