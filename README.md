# Fakeys - Fake keys, get it?

This is meant to be the same kind of thing as [KeyMime](https://github.com/mtlynch/key-mime-pi); a project to allow (primarily) a Raspberry Pi Zero W to act as a keyboard, controlled by a simple web interface of some kind. It borrows ideas from the [Rpi-remote-keyboard](https://github.com/n0rc/rpi-remote-keyboard) project.

It also uses keyboard layout files from [Keyboard Layout Info](https://kbdlayout.info/) because I am way too lazy to make my own keyboard layouts. Those use ISO scancodes though, so Fakeys translates between scancodes (which describe physical keys) and HID usage codes (which also describe physical keys).

Someone should make a new standard for referencing hardware keys that covers everyone's use case, so we won't need to deal with this translation business.

## Installation and prep

This is primarily for use with a Raspberry Pi Zero W 1.3, and that's the only device I've tested it on.

I use a normal Raspbian Lite setup; I find the [Raspberry Pi Imager](https://www.raspberrypi.com/software/) to be the easiest way to get started. I usually keep it headless, with a pre-setup wireless connection and SSH.

When you're in the raspbian install, just clone this repo to the device.

### DWC2 & Libcomposite

DWC2 is a driver that allows the Raspberry Pi to act as a USB host. LibComposite lets it present itself as a composite device, for example a keyboard =)

1. Add ```dtoverlay=dwc2``` to the /boot/firmware/config.txt file, under the ```[all]``` heading.
   - This is the same file that used to be /boot/config.txt
2. Create a .conf file in the /etc/modules-load.d folder. Name doesn't matter, I usually go with "usbstuff.conf". The contents should just be ```dwc2``` on the first line and ```libcomposite``` on the second.

### Python libs

Run ```pip -r requirements.txt``` to install the python libraries needed.

Or you can just add them manually; ```pip install lxml flask```.

### Device config & activation

The file ```gadgetsetup.sh``` in this repo sets up the keyboard. Just run it =). With sudo!

I borrowed it wholesale from [Rpi-remote-keyboard](https://github.com/n0rc/rpi-remote-keyboard); I just removed one line (the modprobe of libcomposite).

I might do a simple rewrite of it into Python at some point. For now, it… works, and that's the important thing.

### Autostarting the server

If you want the fakeys server to start automatically on boot, add its absolute path to the file /etc/local.d; so for example:

```/home/myusername/fakeys/fakeys_server.py```

### Auto-connecting to new networks

Way, way outside the scope of this project. Stick to the networks you know =)

## Usage

### Supported text
Pretty much any text supported by the selected keyboard layout should work.

For special characters like ENTER and TAB, use the standard escape sequences like \n and \t.

### Commandline
This part is just basically a recreation of the Rpi-remote-keyboard functionality.

```bash
sudo ./fakeys.py "Hello, world!"
```

Specify a keyboard layout using the --layout option:

```bash
sudo ./fakeys.py "Hello, world!" --layout USX
```

The argument is case sensitive, but keyboard layout files (see below) are expected to be in uppercase except for the .xml suffix.

If you try to specify a layout that isn't in the system, you'll get an error.

### Server
Start the server by running ```sudo fakeys_server.py```.

#### Web frontend
Just go to the base URL (your rpi host name/ip, port 5000, so for instance "http://fakeys:5000") and you should see a simple web interface with a text field, a dropdown, a button and a log area. I'm sure you can figure it out.

I'll add a keyboard layout selector at some point. For now you'll just have to live with the swedish default =)

#### API endpoint
The ```/type_string``` endpoint accepts simple JSON in this format via POST:

```
{
  "string": "Hello, world!"
}
```

You can specify a keyboard layout:

```
{
  "string": "Hello, world!",
  "layout": "usx"
}
```

### Default keyboard layout: Swedish!

Right now the default layout is Swedish, because I'm swedish and this is my program. You can change this in keyboard_layout.py if you want.

At some point I might possibly try to check your OS keyboard layout or something. That sounds like work, though. Again: lazy.

### Adding a keyboard layout
Download your favorite keyboard layout from [kbdlayout.info](https://kbdlayout.info/), use the "XML for processing" file. Put it in the data folder. Use the default file name (so the US keyboard is KBDUS.xml or KBDUSX.xml if it's the international version).

## Plans
### v1.0
- Simple, clear and updated instructions for installation & setup
### Future
- Complete interactive keyboard on the frontend; sending keys directly one at a time as they are typed

## References
- https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
- https://www.toptal.com/developers/keycode
- https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode