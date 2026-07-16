from typing import Optional
from lxml import etree
from dataclasses import dataclass
import logging

xmlfile: str = "./data/KBDSW.xml"
logging.basicConfig(level="INFO")


@dataclass
class key_instruction:
    vk_name: str
    keycode: str
    shift: bool
    altgr: bool
    followedby: Optional["key_instruction"] | None


xml_text = ""


xml_tree = etree.parse(xmlfile)

key_instructions: dict[str, key_instruction] = {}

for physical_key_element in xml_tree.findall("PhysicalKeys/PK"):

    # Get common info for all results of this physical key
    if not physical_key_element.get("SC") or not physical_key_element.get("VK"):
        print("Key lacks SC or VK")
        continue  # Make sure there's a scancode and a vk

    scancode = physical_key_element.get("SC") or ""
    vk_name = physical_key_element.get("VK") or ""
    text = ""
    shift = False
    altgr = False

    logging.info("Processing " + vk_name)

    # Process base unmodified result
    base_result = physical_key_element.xpath("Result[not(@With)]")

    if len(base_result) > 0 and base_result[0].get("Text"):
        text = base_result[0].get("Text")

        instr = key_instruction(
            vk_name=vk_name,
            keycode=scancode,
            shift=shift,
            altgr=altgr,
            followedby=None,
        )

        key_instructions[text] = instr
        logging.info(f" Added {text}")

    # Process modified results
    modified_results = physical_key_element.xpath("Result[@With]")
    if len(modified_results) > 0:
        for modified_result in modified_results:
            text = modified_result.get("Text")
            if not text: continue

            modifiers = modified_result.get("With")
            match modifiers:
                case "VK_SHIFT":
                    shift = True
                    altgr = False
                case "VK_CONTROL VK_MENU":
                    shift = False
                    altgr = True
                case "VK_SHIFT VK_CONTROL VK_MENU":
                    shift = True
                    altgr = True
                case _:
                    continue

            instr = key_instruction(
                vk_name=vk_name,
                keycode=scancode,
                shift=shift,
                altgr=altgr,
                followedby=None,
            )

            key_instructions[text] = instr
            logging.info(f" Added {text}")

    # Process DeadKeyTables

for symbol in key_instructions:
  instr = key_instructions[symbol]
  print(f"To make '{symbol}' press key {instr.vk_name} ({instr.keycode}) and {"do" if instr.shift else "don't"} press Shift and {"do" if instr.altgr else "don't"} press AltGr")