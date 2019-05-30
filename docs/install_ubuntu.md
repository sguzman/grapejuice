# Installation on Ubuntu
Ubuntu comes with older software and therefore requires additional steps to get Grapejuice set up properly

## Upgrade Wine (Ubuntu 18.09 and older)
Ubuntu 18.09 and older come with Wine 3.0 **THIS WILL NOT WORK**. At least WIne 4.0 is required to run Roblox


**01.** Enable 32 bit architecture in dpkg
```bash
sudo dpkg --add-architecture i386 
```

**02.** Download and add the Wine repository key
```bash
wget -nc https://dl.winehq.org/wine-builds/winehq.key -O /tmp/winehq.key
sudo apt-key add /tmp/winehq.key
```

**03.** Add the wine repository

Look up your distribution version below and enter the correct command into your terminal.

| Version                      | Command                                                                             |
|------------------------------|-------------------------------------------------------------------------------------|
| Ubuntu 19.04                 | sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ disco main'  |
| Ubuntu 18.10                 | sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ cosmic main' |
| Ubuntu 18.04 Linux Mint 19.x | sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ bionic main' |
| Ubuntu 16.04 Linux Mint 18.x | sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ xenial main' |
| Ubuntu 14.04 Linux Mint 17.x | sudo apt-add-repository 'deb https://dl.winehq.org/wine-builds/ubuntu/ trusty main' |

**04.** Install Wine
```bash
sudo apt update
sudo apt install --install-recommends wine-stable
```

## Upgrade Python (Ubuntu 18.09 and older)
The Grapejuice source code is structured so it can be packaged as an AppImage. The side effect of this structure is that
it will not work with versions of Python older than 3.7. Unfortunately, Ubuntu 18.09 and older only ship with Python 3.6.

**01.** Install the prerequisites
```bash
sudo apt update
sudo apt install software-properties-common
```

**02.** Add the deadsnakes PPA, when you are prompted, press `Enter`
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
```

**03.** Once the repository is added, you can install Python 3.7
```bash
sudo apt install python3.7 python3.7-dev python3.7-venv
```

**04.** Additionally, check if the upgrade was successful
```bash
python3.7 --version
```

## Installing the python development packages (Ubuntu 19.04 and newer)
Grapejuice requires python development headers to be present in order for it to be installed, these are not installed
on Ubuntu by default. You will need to follow this step using a terminal.

The process is extremely simple, just run the following:
```bash
sudo apt update
sudo apt install python3-dev
```

## Install Grapejuice dependencies
```bash
sudo apt update
sudo apt install python3-pip virtualenv libcairo2-dev libgirepository1.0-dev libgtk-3-0 libgtk-3-bin
```

## Install Grapejuice

**01.** Download Grapejuice
You can acquire the Grapejuice source code through two methods

1) Download a [pre-packaged zip file from GitLab](https://gitlab.com/brinkervii/grapejuice/-/archive/master/grapejuice-master.zip)
2) Clone the source code (`git clone https://gitlab.com/brinkervii/grapejuice`) 

**02.** Navigate to the source code with your terminal

**03.**
Depending on the earlier steps, you have to run the install script with the appropriate python interpreter

**If you installed Python 3.7 manually:** `python3.7 ./install.py`

**else**: `./install.py` 

**Sidenote:** You can doubleclick on `install.py` in your file manager, but you will not get any output regarding the installation progress

## References
WineHQ Ubuntu installation guide | [https://wiki.winehq.org/Ubuntu](https://wiki.winehq.org/Ubuntu)

Linuxize: How to install Python 3.7 on Ubuntu 18.04 | [https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/](https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/)
