import csv
import logging
import time
from keyboard_layout import key_instruction

def get_translation_dicts(csv_file: str):
    scancode_hids: dict[str, int] = {}
    scancode_js: dict[str, str] = {}

    with open(csv_file, mode="r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            if len(row[0]) == 0:
                continue
            scancode = row[0]
            hidbyte = int(row[1], 0)
            jsname = row[2]
            scancode_hids[scancode] = hidbyte
            scancode_js[scancode] = jsname
            logging.info(f"{jsname} is scancode {scancode} and hid {hex(hidbyte)}")

    return scancode_hids, scancode_js


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


def make_keypresslist(text: str, instructions: dict[str, key_instruction]):
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
    try:
      with open("/dev/hidg0", "rb+") as fd:
          fd.write(keypress)
          fd.write(keypress_release)
    except:
        logging.warning("Unable to send keypress")


def type(text: str, instructions: dict[str, key_instruction], delay: float = 0):
    keypresslist = make_keypresslist(text, instructions)

    for keypress in keypresslist:
        send_keypress(keypress)
        time.sleep(delay)


scancode_hids, scancode_js = get_translation_dicts("./data/scancode-hid.csv")
keypress_release = bytes(8)