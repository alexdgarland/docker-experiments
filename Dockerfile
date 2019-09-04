FROM centos:7

ARG USER

RUN useradd -ms /bin/bash ${USER}

RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm && \
  yum update && \
  yum install -y python36u python36u-libs python36u-devel python36u-pip

COPY ./webserv.py webserv.py

EXPOSE 8000

USER ${USER}

CMD "./webserv.py"
