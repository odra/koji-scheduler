FROM centos:8

RUN yum install python38 python38-devel python38-pip krb5-devel '@Development Tools' -y

RUN mkdir -p /opt/koji-builder-kube/src
COPY . /opt/koji-builder-kube/src
RUN (cd /opt/koji-builder-kube/src; python3 setup.py install)

USER 1001

ENTRYPOINT ["kojid"]
CMD ["--config", "/etc/kojid/kojid.conf"]
