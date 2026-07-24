#!/usr/bin/env python3

from keyboard_layout import read_layout, get_available_layouts, default_layout
from argparse import ArgumentParser
import keyboard_physical
import sys
import logging

# TODO: More extensive commenting

if __name__ == "__main__":
    available_layouts: list[str] = get_available_layouts() or []
    if len(available_layouts) == 0:
        logging.error("No keyboard layouts found; will exit")
        sys.exit()

    # TODO: Add argument for logging
    parser = ArgumentParser()
    parser.add_argument("string", help="The text to type using the fake keyboard")
    parser.add_argument(
        "--layout",
        default=(
            default_layout
            if default_layout in available_layouts
            else available_layouts[0]
        ),
        help="The keyboard layout to use",
        choices=available_layouts,
    )
    parser.add_argument(
        "--debug",
        default="WARNING",
        choices=["DEBUG","INFO","WARNING","ERROR","CRITICAL"]
    )

    args = parser.parse_args()

    # Specific checks:
    #  - Running as root?
    #  - Gadget exists?

    logging.basicConfig(level=args.debug)

    layout = read_layout(args.layout)
    if not layout:
        sys.exit()

    string = bytes(args.string, "utf-8").decode("unicode_escape")
    keyboard_physical.type(string, layout, 0.01)
