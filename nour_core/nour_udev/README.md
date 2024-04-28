# nour_udev

udev rule creator for nourrobot. 
## Creating udev rule
1. Run the udev creator:
```
$ rosrun nour_udev nour_udev.py
```

2. Copy the created udev rule to /etc/udev/rules.d/58-nour.rules:
```
$ sudo cp 58-nour.rules /etc/udev/rules.d/58-nour.rules
```


## Udev rules by building python-gudev from source (for Ubuntu 18.04)

This will install the python-gudev to your sytem so **nour_udev.py** can  ``` import gudev```
_tested on Ubuntu 18.04.3_


Build python-gudev from source:

```sh

$ sudo apt-get install python-gtk2
$ sudo apt-get install libgudev-1.0-dev
$ git clone https://github.com/nzjrs/python-gudev.git
$ cd python-gudev
$ sudo apt install libtool-bin
$ sudo apt install python-gobject-2-dev
$ ./autogen.sh 
$ make
$ sudo make install
```
[assigning-name-to-usb-device](https://askubuntu.com/questions/905115/assigning-name-to-usb-device/906206)

## [Beginners Guide to Udev in Linux](https://www.thegeekdiary.com/beginners-guide-to-udev-in-linux/)
