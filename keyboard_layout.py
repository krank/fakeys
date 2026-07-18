from lxml import etree
from pathlib import Path
import typing
from dataclasses import dataclass
import logging

# logging.basicConfig(level="INFO")


@dataclass
class key_instruction:
    vk_name: str
    keycode: str
    shift: bool
    altgr: bool
    followedby: str | None

    def __str__(self) -> str:
        return f"Press {self.vk_name} ({self.keycode}){" +Shift" if self.shift else ""}{" +AltGr" if self.altgr else ""}{f" and then you press '{self.followedby}'" if self.followedby else ""}"


def interpret_modifiers(modifiers: str):
    # TODO: Add more accepted modifiers?
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
            return None
    return shift, altgr


def get_instr_complexity(instr: key_instruction):
    complexity: int = 0
    if instr.shift:
        complexity += 1
    if instr.altgr:
        complexity += 1
    if instr.followedby:
        complexity += 2

    return complexity


def process_result_elements(
    elementlist_results: typing.Any,
    key_instructions: dict[str, key_instruction],
    vk_name: str = "",
    scancode: str = "",
    shift: bool = False,
    altgr: bool = False,
    is_deadkey_results: bool = False,
):
    for element_result in elementlist_results:

        text = element_result.get("Text")
        elementlist_deadkeytable_results = element_result.xpath("DeadKeyTable/Result")
        followedby:str | None = None

        # ----------------------------------------------------------------------
        # Get & interpret With

        element_with: str = element_result.get("With")

        if is_deadkey_results:
            followedby = element_with
            # In a deadtable; With means "followed by"
            pass

        else:
            # In normal results; With means one or more modifiers
            if element_with:
                modifiers = interpret_modifiers(element_with)
                if modifiers:
                    shift, altgr = modifiers
                else:
                    continue
            else:
                shift, altgr = False, False

        # ----------------------------------------------------------------------
        # DeadKeyTable handling

        if elementlist_deadkeytable_results:
            logging.info("  Found deadtable")
            process_result_elements(
                elementlist_results=elementlist_deadkeytable_results,
                key_instructions=key_instructions,
                vk_name=vk_name,
                scancode=scancode,
                shift=shift,
                altgr=altgr,
                is_deadkey_results=True
            )

        # ----------------------------------------------------------------------
        # Text handling

        if text:
            # Build the instruction
            instr = key_instruction(
                vk_name=vk_name,
                keycode=scancode,
                shift=shift,
                altgr=altgr,
                followedby=followedby,
            )

            # If the result text already has an instruction, check if the new one is
            #  simpler
            if text in key_instructions:
                current_instr = key_instructions[text]
                if get_instr_complexity(instr) >= get_instr_complexity(current_instr):
                    logging.info(
                        f" Skipping [{text}] because it's not simpler than the current"
                    )
                    continue

            logging.info(f" + [{text}] {instr}")
            key_instructions[text] = instr

    return key_instructions


def read_layout(layoutname: str):
    xmlfile: Path | None = get_layout_file(layoutname)
    if not xmlfile:
        logging.warning("Not a valid layout")
        return None

    xml_tree = etree.parse(xmlfile)
    key_instructions: dict[str, key_instruction] = {}

    for element_physical_key in xml_tree.xpath("PhysicalKeys/PK"):
        # Get common info for all results of this physical key
        if not element_physical_key.get("SC") or not element_physical_key.get("VK"):
            logging.info("Key lacks SC or VK")
            continue  # Make sure there's a scancode and a vk

        scancode = element_physical_key.get("SC") or ""
        vk_name = element_physical_key.get("VK") or ""

        results = element_physical_key.xpath("Result")

        logging.info(f"Processing {vk_name} [{len(results)} results]")

        key_instructions = process_result_elements(
            results,
            key_instructions=key_instructions,
            vk_name=vk_name,
            scancode=scancode,
        )
    return key_instructions


def get_available_layouts():
    available_layouts:list[str] = []

    layoutpath = Path("./data/")

    if not layoutpath.is_dir():
        logging.warning("'./data' directory not found")
        return available_layouts
    
    available_files = layoutpath.glob("KBD*.xml")
    return [file.stem[3:] for file in available_files]


def get_layout_file(layoutname: str):
    fileref:Path = Path(f"./data/KBD{layoutname.upper()}.xml")

    if not fileref.is_file():
        logging.warning(f"File {fileref} not found")
        return None
    else:
        return fileref
        



    
    


# se_instructions = make_instructions_dict("./data/KBDSW.xml")

# print(len(se_instructions))
# print(se_instructions["^"])
