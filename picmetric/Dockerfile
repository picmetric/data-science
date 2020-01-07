FROM nvidia/cuda:10.2-runtime-ubuntu18.04

RUN apt-get update -q && \
    apt-get upgrade -q -y && \
    apt-get install -q -y emacs wget bzip2 sudo \
    build-essential python3-psycopg2

RUN cp /etc/apt/sources.list /etc/apt/sources.list~ && \
    sed -Ei 's/^# deb-src /deb-src /' /etc/apt/sources.list && \
    apt-get update -q && \
    DEBIAN_FRONTEND=noninteractive apt-get build-dep python3-psycopg2 -y -q

RUN apt-get update -q && \
    adduser --disabled-password --gecos '' ubuntu && adduser ubuntu sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu
WORKDIR /home/ubuntu/
RUN chmod 777 /home/ubuntu/ && mkdir app

RUN wget https://repo.continuum.io/archive/Anaconda3-2019.10-Linux-x86_64.sh -q && \
    bash Anaconda3-2019.10-Linux-x86_64.sh -b > /dev/null && \
    rm Anaconda3-2019.10-Linux-x86_64.sh

ENV PATH /home/ubuntu/anaconda3/bin:$PATH

RUN conda init bash && \
    /bin/bash -c ". activate" && \
    conda config -q --append channels conda-forge

RUN conda install -q -y libiconv PyYAML tensorflow==1.15
RUN python3 -m pip install --no-binary :all: psycopg2 && \
    python3 -m pip install pyuwsgi Flask==1.1.1 Flask_SQLAlchemy==2.4.1 \
    Keras==2.3.1 Pillow==6.2.1 beautifulsoup4==4.8.1 google_images_download==2.8.0 \
    matplotlib==3.1.2 numpy==1.17.4 opencv_python==4.1.2.30 python_decouple==3.3 \
    python_dotenv==0.10.3 requests==2.22.0 tensorflow==1.15.0 psycopg2-binary==2.8.4 \
    lxml==4.4.2 praw==6.4.0 pandas==0.25.3

COPY . /home/ubuntu/

CMD [ "uwsgi", "app.ini" ]