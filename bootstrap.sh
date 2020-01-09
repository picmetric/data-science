sudo apt-get update && sudo apt-get upgrade -y

sudo curl -L https://github.com/docker/compose/releases/download/1.25.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

git clone --single-branch --branch distortedlogic https://github.com/picmetric/data-science.git
cd data-science

pip install gdown
gdown -O picmetric/flaskapp/models/weights/yolo.h5 --id 1FlunJyoz6GAU5RL5E0k3qxJNRawE3dNq

sudo docker-compose up --build