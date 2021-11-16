## WORK IN PROGRESS

# Files

**Dashboard_main.py**  => main script contain everything 

**interface.ui** => XML file that contains the mainwindow graphical setup

**other/launcher.sh** => bash file to launch main script if it's not open, else it put the window in front

**ombre.py** => empty window that is supposed to open fullscreen and with transparency

**sound_level.py** => contain the class of the sound_level display script

**source_handler** => contain the needed functions to handle the data from the arduino

# TO DO
## Software
### UI
Add graph of consumption
### Info message notification
Change Icon
### Volume notification
Make it beautifuler ! I dont't like it...
Add volume level in text
## Hardware
### Screen
Handle the brightness control
Handle the power control
### Generale
lower the voltage of the 12V input of ignition


### Parsing State
```
VOLUME_FRAME         => OK
TEMPERATURE_FRAME    => OK
RADIO_SOURCE_FRAME   => OK
RADIO_NAME_FRAME     => OK
RADIO_FREQ_FRAME     => OK
RADIO_FMTYPE_FRAME   => OK
RADIO_DESC_FRAME     => Not working at all
INFO_MSG_FRAME       => OK
RADIO_STATIONS_FRAME => OK
INFO_TRIP_FRAME      => OK
INFO_INSTANT_FRAME   => OK
AUDIO_SETTINGS_FRAME => OK
REMOTE_COMMAND_FRAME => OK
OPEN_DOOR_FRAME      => working, but maybe useless (redundant info w/ INFO_MSG_FRAME)

```
# Dependancies
### To launch Picom window manager on startup
```
nano /etc/xdg/lxsession/LXDE-pi/autostart
or
nano/etc/xdg/LXDE-pi/autostart
```
Edit the file to add  :

> picom -b --config /home/pi/.../config-picom.conf

Ex :
```
    @lxpanel --profile LXDE-pi
    @pcmanfm --desktop --profile LXDE-pi
    @xscreensaver -no-splash
    @picom -b --config /home/pi/lucas/config-picom.conf
    point-rpi
    xset s off
    xset s noblank
    xset -dpm
    /usr/local/bin/openauto
    /usr/local/bin/controller_service_watchdog.sh
```
### Install pyqt5
```
sudo apt-get install python3-pyqt5
```

### Install Picom,  yshui'fork
```
sudo apt install cmake meson git pkg-config asciidoc libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libxcb-glx0-dev libpixman-1-dev libdbus-1-dev libconfig-dev libgl1-mesa-dev  libpcre2-dev  libevdev-dev uthash-dev libev-dev libx11-xcb-dev
git clone https://github.com/yshui/picom
cd picom
git submodule update --init --recursive
meson --buildtype=release . build
ninja -C build
sudo ninja -C build install
```
### Install tksvg is useless ?
```
sudo apt install cmake build-essential tcl-dev tk-dev python3-tk
python -m pip install scikit-build
python setup.py install
```
### install python 3 ? ...I don't think I need to...
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3
```
### humm...maybe useless too...
```
sudo apt-get install -y python-pil.imagetk
sudo pip3 install tksvg
```
