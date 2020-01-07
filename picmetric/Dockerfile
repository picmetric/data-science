FROM nvidia/cuda:10.2-runtime-ubuntu18.04

RUN apt-get update -q && \
    apt-get upgrade -q -y && \
    apt-get install -q -y emacs wget bzip2 sudo \
    build-essential

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

RUN conda install -q -y libiconv PyYAML tensorflow-gpu==1.15
RUN python3 -m pip install pyuwsgi Flask==1.1.1 \
    Keras==2.3.1 Pillow==7.0.0 mtcnn == 0.1.0 \
    matplotlib==3.1.2 numpy==1.17.4 python_decouple==3.3 \
    python_dotenv==0.10.3 tensorflow-gpu==1.15.0 \

COPY . /home/ubuntu/

CMD [ "uwsgi", "app.ini" ]