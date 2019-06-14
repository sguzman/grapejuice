# Installation on Arch Linux

## Install dependencies
```bash
sudo pacman -S python-pip python-virtualenv cairo gtk3 gobject-introspection gobject-introspection-runtime xdg-user-dirs lib32-gnutls
```

## Install Grapejuice

**01.** Download Grapejuice
You can acquire the Grapejuice source code through two methods

1) Download a [pre-packaged zip file from GitLab](https://gitlab.com/brinkervii/grapejuice/-/archive/master/grapejuice-master.zip)
2) Clone the source code (`git clone https://gitlab.com/brinkervii/grapejuice`) 

**02.** Navigate to the source code with your terminal

**03.** Run the Grapejuice installer `./install.py`

**Sidenote:** You can doubleclick on `install.py` in your file manager, but you will not get any output regarding the installation progress

