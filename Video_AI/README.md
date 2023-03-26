# Building OpenCV for GStreamer on Raspberry Pi
---

### Make sure you have gcc & g++ on RPi (if note then install it)
- `gcc --version`

- `g++ --version`
---
### Installing GStreamer & packages before building

- Make sure the system is up-to-date

    `sudo apt update && sudo apt upgrade`

- Installing different libraries:

```
sudo apt install libtiff-dev libjpeg-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev crossbuild-essential-armhf libgtk-3-dev 
```

- Installing packages required to build:

    `sudo apt install cmake git pkg-config wget`

- Install GStreamer
```
sudo apt-get install libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-bad1.0-dev \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-tools \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3

# if you have Qt5 install this plugin
sudo apt-get install gstreamer1.0-qt5

# install if you want to work with audio
sudo apt-get install gstreamer1.0-pulseaudio
```

- Test if GStreamer has been installed successfully

    `gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink`

---

### Fetching the OpenCV for RPi from their GitHub Repo
```
cd ~

mkdir opencv_all && cd opencv_all

wget -O opencv-4.7.0.tar.gz https://github.com/opencv/opencv/archive/4.7.0.tar.gz

wget -O opencv_contrib-4.7.0.tar.gz https://github.com/opencv/opencv_contrib/archive/4.7.0.tar.gz

tar xf opencv-4.7.0.tar.gz

tar xf opencv_contrib-4.7.0.tar.gz

rm -r *.tar.gz
```
---
### Building OpenCV for GStreamer
```
cd opencv-4.7.0
mkdir build && cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/home/pi/opencv_all/opencv_contrib-4.7.0/modules \
    -D PYTHON_EXECUTABLE=$(which python) \
    -D BUILD_opencv_python2=OFF \
    -D CMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
    -D PYTHON3_EXECUTABLE=$(which python) \
    -D PYTHON3_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
    -D PYTHON3_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
    -D WITH_GSTREAMER=ON \
    -D BUILD_EXAMPLES=ON ..

# Run the below commands inside the 'opencv_all/opencv-4.7.0/build/' directory
# This can take upto 2 hours (depends on the configuration of the RPi)
sudo make -j$(nproc)

sudo make install

sudo ldconfig
```