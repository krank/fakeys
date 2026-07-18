# Fakeys - Fake keys, get it?

This is meant to be the same kind of thing as [KeyMime](https://github.com/mtlynch/key-mime-pi); a project to allow (primarily) a Raspberry Pi Zero W to act as a keyboard, controlled by a simple web interface of some kind. It borrows ideas from the [Rpi-remote-keyboard](https://github.com/n0rc/rpi-remote-keyboard) project.

It also uses keyboard layout files from [Keyboard Layout Info](https://kbdlayout.info/) because I am way too lazy to make my own keyboard layouts. Those use ISO scancodes though, so Fakeys translates between scancodes (which describe physical keys) and HID usage codes (which also describe physical keys).

Someone should make a new standard for referencing hardware keys that covers everyone's use case, so we won't need to deal with this translation business.

## Installation and prep

[Coming soon]

## Usage
Currently there's no web api/interface part, just basically a recreation of the Rpi-remote-keyboard functionality.

```bash
sudo ./fakeys.py "Hello, world!"
```

Specify a keyboard layout using the --layout option:

```bash
sudo ./fakeys.py "Hello, world!" --layout USX
```

The argument is case sensitive, but keyboard layout files (see below) are expected to be in uppercase except for the .xml suffix.

If you try to specify a layout that isn't in the system, you'll get an error.

Right now the default layout is Swedish, because I'm swedish and this is my program. At some point I might add a config file or possibly try to check your OS keyboard layout or something. That sounds like work, though. Again: lazy.


### Adding a keyboard layout
Download your favorite keyboard layout from [kbdlayout.info](https://kbdlayout.info/), use the "XML for processing" file. Put it in the data folder. Use the default file name (so the US keyboard is KBDUS.xml or KBDUSX.xml if it's the international version).

## References
- https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
- https://www.toptal.com/developers/keycode
- https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode