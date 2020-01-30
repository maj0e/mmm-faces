#!/bin/bash
ocv_version=4.1.0 #Set version of opencv you wish to download
number_of_cores=4 #The number of cores you want to use for compiling

# Download source for opencv and contrib modules
mkdir /work/opencv-$ocv_version && cd /work/opencv-$ocv_version
wget -O opencv.tar.gz https://github.com/opencv/opencv/archive/$ocv_version.tar.gz
tar xf opencv.tar.gz
mv opencv-$ocv_version opencv
wget -O opencv_contrib.tar.gz https://github.com/opencv/opencv_contrib/archive/$ocv_version.tar.gz
tar xf opencv_contrib.tar.gz
mv opencv_contrib-$ocv_version opencv_contrib
mkdir release
rm *.tar.gz

cd opencv
mkdir build && cd build

# Configure System to detect gtk+
export PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig
export PKG_CONFIG_LIBDIR=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/work/opencv-$ocv_version/release \
    -D OPENCV_EXTRA_MODULES_PATH=/work/opencv-$ocv_version/opencv_contrib/modules \
    -D ENABLE_NEON=ON \
    -D ENABLE_VFPV3=ON \
    -D WITH_GTK=ON \
    -D BUILD_TESTS=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D INSTALL_PYTHON_EXAMPLES=OFF \
    -D BUILD_DOCS=OFF \
    -D BUILD_EXAMPLES=OFF ..
      
# Start Compiling
make -j$number_of_cores

#Install Opencv and tar it
sudo make install/strip

cd /work/
tar -cjvf opencv-rpi3-$ocv_version.tar.bz2 opencv-$ocv_version
 

 
