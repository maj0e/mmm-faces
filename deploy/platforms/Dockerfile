FROM dockcross/linux-x64

ENV DEFAULT_DOCKCROSS_IMAGE crosscompileenv

RUN apt-get update -y && apt-get upgrade -y

RUN apt-get install -y build-essential cmake pkg-config wget unzip
# 
# Input libraries
RUN apt-get install -y libjpeg-dev libpng-dev libtiff-dev
RUN apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
RUN apt-get install -y libxvidcore-dev libx264-dev

RUN apt-get install -y libgtk-3-dev libcanberra-gtk*


RUN apt-get install -y build-essential cmake unzip pkg-config curl
#RUN apt-get install -y libatlas-base-dev gfortran

RUN apt-get install -y python3-dev

RUN apt-get install -y libeigen3-dev libopenblas-dev

#RUN apt-get install -y libopencv-core4.2 libopencv-dnn4.2

Run pip install pyinstaller
# Dlib dependencies
#RUN apt-get install -y libboost-all-dev
#RUN apt-get install -y libopenblas-dev liblapack-dev

 
