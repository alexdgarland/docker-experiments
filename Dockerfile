FROM centos:7

ARG USER
RUN useradd -ms /bin/bash ${USER}

ARG PACKAGE_FULLNAME

ENV WEBSERVER_PORT=8000
EXPOSE ${WEBSERVER_PORT}

COPY dist/${PACKAGE_FULLNAME}.tar.gz webserver.tar.gz

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm && \
    yum update && \
    yum install -y python36u python36u-libs python36u-devel python36u-pip && \
    python3.6 -m pip install webserver.tar.gz && \
    rm webserver.tar.gz

USER ${USER}
CMD "webserver"
