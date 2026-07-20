import csv
import logging
import time
from keyboard_layout import key_instruction
from log_handlers import CollectHandler

logger = logging.getLogger(__name__)
log_collector = CollectHandler()
logger.addHandler(log_collector)


def get_translation_dicts(csv_file: str):
    scancode_hids: dict[str, int] = {}
    jsname_hids: dict[str, int] = {}

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
            jsname_hids[jsname] = hidbyte
            logger.info(f"{jsname} is scancode {scancode} and hid {hex(hidbyte)}")

    return scancode_hids, jsname_hids


def make_hidbytearray(instruction: key_instruction, translation_dict: dict[str, int]):
    keypress = bytearray(8)
    keycode = "0x" + instruction.keycode.lower()

    if keycode not in translation_dict:
        print(f"{keycode} not found")
        return None

    hidbyte:int = translation_dict[keycode]

    modbyte = 0
    if instruction.shift:
        modbyte |= 2
    if instruction.altgr:
        modbyte |= 64
        # modbyte |= 16 | 64

    logger.info(f"hidbyte: {hex(hidbyte)} modbyte: {"{:08b}".format(modbyte)}")

    keypress[0] = modbyte
    keypress[2] = hidbyte

    return keypress


def make_keypresslist(text: str, layout: dict[str, key_instruction]):
    keypresses: list[bytearray] = []

    for symbol in text:
        while True:
            if symbol not in layout:
                logger.warning(f"No instructions for [{symbol}]")
                break

            instr = layout[symbol]

            keypress = make_hidbytearray(instr, scancode_hids)

            if not keypress:
                break

            keypresses.append(keypress)
            if not instr.followedby:
                break

            symbol = instr.followedby
    return keypresses

def send_keypress(keypress: bytearray | bytes):
    try:
      with open("/dev/hidg0", "rb+") as fd:
          fd.write(keypress)
          return True
    except:
        logger.warning("Unable to send keypress")
        return False


def type(text: str, layout: dict[str, key_instruction], delay: float = 0):
    log_collector.clear()

    keypresslist = make_keypresslist(text, layout)

    for keypress in keypresslist:
        send_keypress(keypress)
        send_keypress(keypress_release)
        time.sleep(delay)

scancode_hids, jsname_hids = get_translation_dicts("./data/scancode-hid.csv")
keypress_release = bytes(8)