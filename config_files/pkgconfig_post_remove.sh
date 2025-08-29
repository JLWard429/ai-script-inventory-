#!/bin/sh
# shellcheck shell=sh

PKG_SEARCH_PATH="/usr/local/share/pkgconfig"

if [ -d "$PKG_SEARCH_PATH" ]; then
    # find and remove all broken symlinks
    find -L "$PKG_SEARCH_PATH" -type l -exec rm -fv {} \;
fi

# remove the PKG_SEARCH_PATH folder if empty
rmdir --parents --ignore-fail-on-non-empty "$PKG_SEARCH_PATH" 

exit 0