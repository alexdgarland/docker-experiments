FROM centos:7

ARG USER
RUN useradd -ms /bin/bash ${USER}

ENV WEBSERVER_PORT=8000
EXPOSE ${WEBSERVER_PORT}

COPY ./requirements.txt requirements.txt
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm && \
    yum update && \
    yum install -y python36u python36u-libs python36u-devel python36u-pip && \
    python3.6 -m pip install -r requirements.txt && \
    rm requirements.txt

COPY pages pages
COPY webserver.py webserver.py

USER ${USER}
CMD "./webserver.py"
