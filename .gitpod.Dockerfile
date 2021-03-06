FROM gitpod/workspace-full-vnc

RUN sudo apt-get update \ 
    && sudo apt-get install -y \
    mesa-utils \
    libgl1 \ 
    libxkbcommon-x11-0 \
    x11-xserver-utils \
    && sudo rm -rf /var/lib/apt/lists/*

ENV QT_DEBUG_PLUGINS=1
# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/


# Maybe need:
# libx11-xcb1 \
# libxkbcommon-x11-0 \  # needed for qt's xcb 
# x11-xserver-utils   # gets xrandr, used for setting/determining screen resolution
# x11-apps  # provides xeyes, a nice test for if graphics are working at all on x11
# libgtk-3-dev 
# mesa-utils freeglut3-dev   # gl funcs and glu funcs
# libsdl2-dev