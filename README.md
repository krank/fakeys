# Fakeys - Fake keys, get it?

This is meant to be the same kind of thing as [KeyMime](https://github.com/mtlynch/key-mime-pi); a project to allow (primarily) a Raspberry Pi Zero W to act as a keyboard, controlled by a simple web interface of some kind. It borrows ideas from the [Rpi-remote-keyboard](https://github.com/n0rc/rpi-remote-keyboard) project.

It also uses keyboard layout files from [Keyboard Layout Info](https://kbdlayout.info/) because I am way too lazy to make my own keyboard layouts. Those use ISO scancodes though, so Fakeys translates (or will translate) between scancodes (which describe physical keys) and HID usage codes (which also describe physical keys).

## References
- https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
- https://www.toptal.com/developers/keycode
- https://developer.mozilla.org/en-US/docs/Web/API/KeyboardEvent/keyCode