#!/usr/bin/env bash

apt update
apt install build-essential appstream libcairo2-dev libgirepository1.0-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev zlib1g-dev zlibc libgtk-3-0 gir1.2-gtk-3.0 libgdk-pixbuf2.0-dev libpangox-1.0-dev libgtk-3-0 libgtk-3-dev gnome-shell -y

systemctl disable display-manager
systemctl disable gdm3


wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
tar xvf Python-3.7.3.tgz

OLD_CWD=`pwd`

cd Python-3.7.3
./configure --enable-shared
make
make install

cd ${OLD_CWD}