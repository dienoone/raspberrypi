#!/bin/bash

# Append environment variables to .bashrc
echo 'export PKG_CONFIG_PATH=/home/pi/Downloads/libcamera/build/meson-uninstalled:$PKG_CONFIG_PATH' >> ~/.bashrc
echo 'export GST_REGISTRY=/home/pi/Downloads/libcamera/build/src/gstreamer/registry.data' >> ~/.bashrc
echo 'export GST_PLUGIN_PATH=/home/pi/Downloads/libcamera/build/src/gstreamer:$GST_PLUGIN_PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/home/pi/Downloads/libcamera/build/src/libcamera/base:/home/pi/Downloads/libcamera/build/src/libcamera:/home/pi/Downloads/libcamera/build/subprojects/libpisp/src:$LD_LIBRARY_PATH' >> ~/.bashrc

# Reload .bashrc to apply changes
source ~/.bashrc

echo "Environment variables for libcamera have been added to .bashrc and applied."
