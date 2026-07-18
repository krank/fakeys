#!/usr/bin/env python3

from key_instructions import make_instructions_dict, key_instruction
from translations import get_translation_dicts
import logging
import time

# logging.basicConfig(level="INFO")

# Preparations


scancode_hids, scancode_js = get_translation_dicts("./data/scancode-hid.csv")
keypress_release = bytes(8)

def make_hidbytearray(instruction: key_instruction):
    keypress = bytearray(8)
    keycode = "0x" + instruction.keycode.lower()

    if keycode not in scancode_hids:
        print(f"{keycode} not found")
        return None

    hidbyte = scancode_hids[keycode]

    modbyte = 0
    if instruction.shift:
        modbyte |= 2
    if instruction.altgr:
        modbyte |= 16 | 64

    logging.info(f"hidbyte: {hex(hidbyte)} modbyte: {"{:08b}".format(modbyte)}")

    keypress[0] = modbyte
    keypress[2] = hidbyte

    return keypress


def make_keypresses(text: str, instructions: dict[str, key_instruction]):
    keypresses: list[bytearray] = []

    for symbol in text:
        while True:
            if symbol not in instructions:
                logging.warning(f"No instructions for [{symbol}]")
                break

            instr = instructions[symbol]

            keypress = make_hidbytearray(instr)

            if not keypress:
                break

            keypresses.append(keypress)
            if not instr.followedby:
                break

            symbol = instr.followedby
    return keypresses

def send_keypress(keypress: bytearray):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(keypress)
        fd.write(keypress_release)

if __name__ == '__main__':
    se_instructions = make_instructions_dict("./data/KBDSW.xml")
    en_instructions = make_instructions_dict("./data/KBDUSX.xml")

    text = "Hello, world"

    keypresses = make_keypresses(text, se_instructions)

    for keypress in keypresses:
        send_keypress(keypress)
        time.sleep(0.01)
