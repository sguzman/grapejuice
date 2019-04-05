# Grapejuice
Since recent releases of Wine, Roblox Studio has started being able to run under it once again.
Installing an managing Roblox under Wine can be quite the hassle as Wine itself can create a mess and binding protocol
uri's are not supported by default. Grapejuice aims to address these problems and make Roblox easy to get setup op Linux.

## Requirements
You need a recent version of `wine` in order to run Roblox. A Wine version in the 4.x series or higher is recommended.
The [WineHQ website](https://wiki.winehq.org/Ubuntu) has a guide on getting a newer version of Wine installed on Ubuntu.

Grapejuice is written using Python 3. The only two requirements for running Grapejuice are `python-pip`
and `python-virtualenv`. Depending on your Linux distribution you might have to install `python3-pip` and
`python3-virtualenv` instead.

`gtk3` is required for the graphical user interface, but this should already be installed on most modern Linux
distributions.

## Installation
- Clone this repository
- `cd` into it
- Run `./install.py`
- Open Grapejuice
- Click "Install Roblox" under the Maintenance tab

That's all!

I recommend that after installing roblox, you change the rendering method to OpenGL instead of the default. You can find
this setting under Settings -> Rendering in the Roblox Studio menu.

## Features
- Contain and automate a Wine prefix
- Expose utility functions
- Edit Roblox games from the website

## Roblox and Wine compatibility
What works:
- Roblox Studio
- Team Create
- Play Solo

Bugs:
- With a dual monitor setup, context menus and dialogs may appear on the wrong monitor

What doesn't work:
- The Roblox game client
- Test server
- Plugin gui's may cause seizures