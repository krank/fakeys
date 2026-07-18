#!/usr/bin/env python3

from keyboard_layout import make_instructions_dict
from argparse import ArgumentParser
import keyboard_physical

# logging.basicConfig(level="INFO")

#TODO: Next subproject: simple api endpoints for sending strings / keys

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("string")

    args = parser.parse_args()

    #TODO: Add checking for superuser, linux os

    #TODO: Allow choosing keyboard layout by argument
    se_instructions = make_instructions_dict("./data/KBDSW.xml")
    en_instructions = make_instructions_dict("./data/KBDUSX.xml")


    keyboard_physical.type(args.string, se_instructions, 0.01)