import csv
import logging

def get_translation_dicts(csv_file: str):
  scancode_hids: dict[str, int] = {}
  scancode_js: dict[str, str] = {}

  with open(csv_file, mode="r") as file:
    reader = csv.reader(file)
    next(reader)

    for row in reader:
      if len(row[0]) == 0: continue
      scancode = row[0]
      hidbyte = int(row[1], 0)
      jsname = row[2]
      scancode_hids[scancode] = hidbyte
      scancode_js[scancode] = jsname
      logging.info(f"{jsname} is scancode {scancode} and hid {hex(hidbyte)}")
  
  return scancode_hids, scancode_js