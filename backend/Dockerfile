FROM centos:centos7

WORKDIR /code

ADD ./requirements.txt /code

RUN \
yum install epel-release -y &&\
yum clean all && yum update -y

RUN \
yum install portaudio-devel python34-pip mlocate bash-completion git wget sox libtool autoconf bison swig python34-devel python34-numpy python34-scipy python-devel doxygen alsa-lib-devel pulseaudio-libs-devel make -y

RUN yum install python34-setuptools
RUN easy_install-3.4 pip

RUN \
pip3 install --upgrade pip


RUN pip3 install -r requirements.txt

RUN python3.4 -m textblob.download_corpora


RUN \
updatedb

EXPOSE "4500"

ADD ./app.py /code

CMD ["python3.4", "app.py"]