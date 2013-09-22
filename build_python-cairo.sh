#!/bin/bash

# Stop this script if an error occurs:
set -o errexit
set -o nounset
set -x # Trace

MY_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
INSTALL_DIR="$MY_DIR/python-cairo"
SRC_DIR="$INSTALL_DIR/.src"
mkdir -p "$SRC_DIR"

PY_VERSION=$(python -c 'import sys; print "%d.%d"%sys.version_info[:2]')

export LD_LIBRARY_PATH="$INSTALL_DIR/lib${LD_LIBRARY_PATH+:${LD_LIBRARY_PATH:-}}"
export PYTHONPATH="$INSTALL_DIR/lib/python$PY_VERSION/site-packages${PYTHONPATH+:${PYTHONPATH:-}}"


if [ ! -f "$INSTALL_DIR/lib/pkgconfig/pixman-1.pc" ]; then
    echo "Building Pixman... (a prerequisite of Cairo)"
    cd $SRC_DIR
    [ -f pixman-0.20.2.tar.gz ] || wget http://cairographics.org/releases/pixman-0.20.2.tar.gz
    [ -d pixman-0.20.2 ] || tar xf pixman-0.20.2.tar.gz
    cd pixman-0.20.2
    ./configure --prefix="$INSTALL_DIR"
    make
    make install
fi


if [ ! -f "$INSTALL_DIR/lib/cairo/libcairo-trace.a" ]; then
    echo "Building Cairo... (a prerequisite of PyCairo)"
    cd $SRC_DIR
    [ -f cairo-1.10.2.tar.gz ] || wget http://www.cairographics.org/releases/cairo-1.10.2.tar.gz
    [ -d cairo-1.10.2 ] ||  tar xf cairo-1.10.2.tar.gz
    cd cairo-1.10.2
    PKG_CONFIG_PATH="$INSTALL_DIR/lib/pkgconfig" CPPFLAGS="-I$INSTALL_DIR/include/pixman-1" LDFLAGS="-L$INSTALL_DIR/lib" ./configure --prefix="$INSTALL_DIR"
    make
    make install
fi


if [ ! -f cairo/__init__.py ]; then
    echo "Building python-cairo..."
    cd $SRC_DIR
    [ -f py2cairo-1.10.0.tar.bz2 ] || wget http://cairographics.org/releases/py2cairo-1.10.0.tar.bz2
    [ -d py2cairo-1.10.0 ] || tar xf py2cairo-1.10.0.tar.bz2
    cd py2cairo-1.10.0
    #PKG_CONFIG_PATH="$INSTALL_DIR/lib/pkgconfig" CPPFLAGS="-I$INSTALL_DIR/include" LDFLAGS="-L$INSTALL_DIR/lib" python setup.py install --install-base="$INSTALL_DIR" --install-lib='$base/lib' --install-scripts='$base/bin' --install-data='$base/data' --install-headers='$base/include'
    # Need to patch waf on WebFaction because we are unable to "ls /home":
    ./waf --help || true   # The first run generates Scripting.py.
    sed -i "s/lst=os.listdir(cur)/lst=['$USER'] if cur=='\\/home' else os.listdir(cur)/g" .waf-*/waflib/Scripting.py
    PKG_CONFIG_PATH="$INSTALL_DIR/lib/pkgconfig" CPPFLAGS="-I$INSTALL_DIR/include/pixman-1" LDFLAGS="-L$INSTALL_DIR/lib" ./waf configure --prefix="$INSTALL_DIR"
    PKG_CONFIG_PATH="$INSTALL_DIR/lib/pkgconfig" CPPFLAGS="-I$INSTALL_DIR/include/pixman-1" LDFLAGS="-L$INSTALL_DIR/lib" ./waf build
    PKG_CONFIG_PATH="$INSTALL_DIR/lib/pkgconfig" CPPFLAGS="-I$INSTALL_DIR/include/pixman-1" LDFLAGS="-L$INSTALL_DIR/lib" ./waf install
fi


cat << EOF >> ~/.bashrc
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH"
export PYTHONPATH="$PYTHONPATH"
EOF


echo 'Done  :)'
echo "You must log out and log back in for changes to take effect.  (Or just run 'bash'.)"

