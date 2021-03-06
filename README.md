# Grapejuice

⚠️ A lot of people assume that the Roblox game client will work. To be extremely clear, **Roblox player does NOT work**
 Only Roblox Studio Works.

---

Since recent releases of Wine, Roblox Studio has started being able to run under it once again.
Installing an managing Roblox under Wine can be quite the hassle as Wine itself can create a mess and binding protocol
uri's are not supported by default. Grapejuice aims to address these problems and make Roblox easy to get setup on Linux.

Please note that this project is highly experimental, not everything will work perfectly.

## Installing Grapejuice from source

Installing from source differs per distributions, please follow the appropriate installation guide for yours.
All the installation guides can be found in the [Grapejuice Wiki](https://gitlab.com/brinkervii/grapejuice/wikis/home)

## Note for upgrading from 1.x to 2.x
The builtin Grapejuice updater behaves a bit wonkily upgrading from 1.x to 2.x. Upgrading *does* work.
However, the upgrade button might not indicate such until you relaunch Grapejuice manually.

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

What doesn't work:
- The Roblox game client
- Test server
- Plugin gui's may cause seizures with some rendering methods. More about this issue is discussed in the [Troubleshooting Guide](https://gitlab.com/brinkervii/grapejuice/wikis/Troubleshooting)
