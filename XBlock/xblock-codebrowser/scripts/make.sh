#!/bin/bash
id=$1
lab=$2

dir=/edx/var/edxapp/staticfiles/ucore/$id/ucore_lab/labcodes/$lab
echo $dir
cd $dir
##make command

#ucore_plus make commands
#make -B ARCH=i386 defconfig
#make -B
#make -B sfsimg

#ucore_lab make commands
make -B
