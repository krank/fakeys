from lxml import etree
from pathlib import Path
import typing
import logging

from dataclasses import dataclass
from log_handlers import CollectHandler

type Layout = dict[str, key_instruction]

# logging.basicConfig(level="INFO")

logger = logging.getLogger(__name__)
log_collector = CollectHandler()
logger.addHandler(log_collector)


@dataclass
class key_instruction:
    vk_name: str
    keycode: str
    shift: bool
    altgr: bool
    followedby: str | None

    def __str__(self) -> str:
        return f"Press {self.vk_name} ({self.keycode}){" +Shift" if self.shift else ""}{" +AltGr" if self.altgr else ""}{f" and then you press '{self.followedby}'" if self.followedby else ""}"


def get_available_layouts():
    available_layouts: list[str] = []

    layoutpath = Path("./data/")

    if not layoutpath.is_dir():
        logger.error("'./data' directory not found")
        return available_layouts

    available_files = layoutpath.glob("KBD*.xml")
    return [file.stem[3:] for file in available_files]


def get_layout_file(layoutname: str):
    fileref: Path = Path(f"./data/KBD{layoutname.upper()}.xml")

    if not fileref.is_file():
        logger.error(f"File {fileref} not found")
        return None
    else:
        return fileref


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
    layout: Layout,
    vk_name: str = "",
    scancode: str = "",
    shift: bool = False,
    altgr: bool = False,
    is_deadkey_results: bool = False,
):
    for element_result in elementlist_results:

        text = element_result.get("Text")
        elementlist_deadkeytable_results = element_result.xpath("DeadKeyTable/Result")
        followedby: str | None = None

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
            logger.info("  Found deadtable")
            process_result_elements(
                elementlist_results=elementlist_deadkeytable_results,
                layout=layout,
                vk_name=vk_name,
                scancode=scancode,
                shift=shift,
                altgr=altgr,
                is_deadkey_results=True,
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
            if text in layout:
                current_instr = layout[text]
                if get_instr_complexity(instr) >= get_instr_complexity(current_instr):
                    logger.info(
                        f" Skipping [{text}] because it's not simpler than the current"
                    )
                    continue

            logger.info(f" + [{text}] {instr}")
            layout[text] = instr

    return layout


def read_layout(layoutname: str):
    log_collector.clear()

    xmlfile: Path | None = get_layout_file(layoutname)
    if not xmlfile:
        logger.error("Not a valid layout")
        return None

    xml_tree = etree.parse(xmlfile)
    layout: Layout = {}

    for element_physical_key in xml_tree.xpath("PhysicalKeys/PK"):
        # Get common info for all results of this physical key
        if not element_physical_key.get("SC") or not element_physical_key.get("VK"):
            logger.info("Key lacks SC or VK")
            continue  # Make sure there's a scancode and a vk

        scancode = element_physical_key.get("SC") or ""
        vk_name = element_physical_key.get("VK") or ""

        results = element_physical_key.xpath("Result")

        logger.info(f"Processing {vk_name} [{len(results)} results]")

        layout = process_result_elements(
            results,
            layout=layout,
            vk_name=vk_name,
            scancode=scancode,
        )
    return layout
