#!/bin/bash
dlib_version=19.17 #Set version of opencv you wish to download
number_of_cores = 4 #The number of cores you want to use for compiling

# Download source for dlib
wget -O dlib.tar.bz2 http://dlib.net/files/dlib-$dlib_version.tar.bz2
tar xjf dlib.tar.bz2
mkdir release
rm *.tar.bz2

cd dlib-$dlib_version
mkdir build && cd build

# Configure System to detect gtk+
#export PKG_CONFIG_PATH=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig
#export PKG_CONFIG_LIBDIR=/usr/lib/arm-linux-gnueabihf/pkgconfig:/usr/share/pkgconfig
 

# Start Cmake, you can configure the flags as needed
cmake ..
cmake -DCMAKE_C_FLAGS=”-O3 -mfpu=neon -fprofile-use -DENABLE_NEON” -DNEON=ON -DCMAKE_CXX_FLAGS=”-std=c++11″ –build –config Release ..


# Start Compiling
make -j$number_of_cores

#Install Opencv and tar it
make install

tar -cjvf dlib-rpi3-$dlib_version.tar.bz2 dlib-$dlib_version
 

 
