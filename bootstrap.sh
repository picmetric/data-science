sudo apt-get update && sudo apt-get upgrade -y

wget https://repo.continuum.io/archive/Anaconda3-2019.10-Linux-x86_64.sh
sh Anaconda3-2019.10-Linux-x86_64.sh > /dev/null
source .bashrc
rm Anaconda3-2019.10-Linux-x86_64.sh
conda activate
conda config --append channels conda-forge

pip install gdown

gdown -O picmetric/flaskapp/models/weights/yolo.h5 --id 1FlunJyoz6GAU5RL5E0k3qxJNRawE3dNq