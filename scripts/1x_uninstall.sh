#!/usr/bin/env bash

GRAPEJUICE_ROOT=$HOME/.local/share/grapejuice
pushd "$GRAPEJUICE_ROOT" || exit 1

for file in $(ls -a | grep -v wineprefix); do
    rm -r "${GRAPEJUICE_ROOT:?}"/"${file:?}"
done

popd || exit 1

APPLICATIONS=$HOME/.local/share/applications
rm "$APPLICATIONS"/grapejuice.desktop
rm "$APPLICATIONS"/roblox-studio.desktop
rm "$APPLICATIONS"/roblox-player.desktop

find "$HOME"/.local/share/mime -iname \*roblox\* -exec rm "{}" \;
find "$HOME"/.local/share/mime -iname \*grapejuice\* -exec rm "{}" \;
find "$HOME"/.local/share/icons/hicolor -iname \*grapejuice\* -exec rm "{}" \;
