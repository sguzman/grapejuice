# Grapejuice
Since recent releases of Wine, Roblox Studio has started being able to run under it once again.
Installing an managing Roblox under Wine can be quite the hassle as Wine itself can create a mess and binding protocol
uri's are not supported by default. Grapejuice aims to address these problems and make Roblox easy to get setup op Linux.

Please note that this project is highly experimental, not everything will work perfectly.

## Installation

Installation differs per distributions, please follow the appropriate installation guide for yours.
All the installation guides can be found in the [Grapejuice Wiki](https://gitlab.com/brinkervii/grapejuice/wikis/home)

I recommend that after installing roblox, you change the rendering method to OpenGL instead of the default. You can find
this setting under Settings -> Rendering in the Roblox Studio menu.

## Troubleshooting

Are you experiencing some trouble running Roblox Studio with Grapejuice? Please check out the [Troubleshooting Guide](https://gitlab.com/brinkervii/grapejuice/wikis/Troubleshooting)

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
