#!/usr/bin/env python3

from keyboard_layout import read_layout, get_available_layouts
from argparse import ArgumentParser
import keyboard_physical
import sys

# logging.basicConfig(level="INFO")

if __name__ == '__main__':
    available_layouts:list[str] = get_available_layouts() or []

    parser = ArgumentParser()
    parser.add_argument("string", help="The text to type using the fake keyboard")
    parser.add_argument("--layout", default="SW", help="The keyboard layout to use", choices=available_layouts)

    args = parser.parse_args()

    # Specific checks:
    #  - Running as root?
    #  - Gadget exists?

    layout = read_layout(args.layout)
    if not layout:
        sys.exit()


    keyboard_physical.type(args.string, layout, 0.01)