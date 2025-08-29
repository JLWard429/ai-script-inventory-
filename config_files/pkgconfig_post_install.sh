#!/bin/sh
# shellcheck shell=sh


INSTALL_DIR="$1"
PKG_CONFIG_PATH_32="/opt/intel//oneapi//dal/2024.6/lib32/pkgconfig"
PKG_CONFIG_PATH_64="/opt/intel//oneapi//dal/2024.6/lib/pkgconfig"
PKG_SEARCH_PATH="/usr/local/share/pkgconfig"

for PKG_CONFIG_PATH in "$PKG_CONFIG_PATH_32" "$PKG_CONFIG_PATH_64"; do
    if [ -d "$PKG_CONFIG_PATH" ]; then
        if [ ! -d "$PKG_SEARCH_PATH" ]; then
            mkdir -pv -m 0775 "$PKG_SEARCH_PATH"
        fi
        # find all *pc files in PKG_SEARCH_PATH
        configs=`find "$PKG_CONFIG_PATH" -name "*.pc" -exec basename {} \;`
        for file in $configs; do
            FULL_PATH=${PKG_CONFIG_PATH}/${file}
            if [ -e "${FULL_PATH}" ]; then
                cp "${FULL_PATH}" "${FULL_PATH}.old"
                sed "s@\${pcfiledir}@${PKG_CONFIG_PATH}@g" "${FULL_PATH}.old" 2>/dev/null 1>"${FULL_PATH}"
                rm -rf "${FULL_PATH}.old"
                
                if [ ! -e "${PKG_SEARCH_PATH}/${file}" ]; then
                    ln -sv "${PKG_CONFIG_PATH}/${file}" "${PKG_SEARCH_PATH}/${file}"
                fi
            fi
        done
    fi
done

exit 0
