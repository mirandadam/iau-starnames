#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
IAU Working Group on Star Names (WGSN) Catalog Processor

This script downloads, processes, and formats the IAU Catalog of Star Names (CSN)
from the Working Group on Star Names (WGSN). It performs the following tasks:

1. Downloads the latest IAU-CSN.txt file if not present locally.
2. Parses and validates the catalog data according to predefined column rules.
3. Applies preprocessing to handle known data inconsistencies.
4. Generates three output files:
   - A normalized text file (IAU-CSN_normalized.txt)
   - A tab-separated values file (IAU-CSN.tsv)
   - A JSON file (IAU-CSN.json)
5. Compares the original and normalized files, reporting any differences.

Data source:
  Website: https://www.iau.org/science/scientific_bodies/working_groups/280/
  Data URL: http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt

Usage:
  Run this script directly. It will create a 'catalog_data' directory (if not exists)
  and store all output files there.

Note:
  If IAU-CSN.txt already exists locally, the script will use that file instead of
  downloading a new one. Delete the local file to force a new download.

Version History:
  2024-07-01: Added preprocessors for validation failures, unicode corrections,
              code formatting with Ruff, and other minor improvements.
  [Add previous version history here]

Dependencies:
  This script uses only Python standard library modules.

Version History:
The update on 2017-10-28 changed the file format:
 *added a '-' for empty field values (good for parsing)
 *removed all the spurious tabs (good for parsing)
 *added a new WDS_J field (neutral for parsing)
 *introduced a misalignment in the Miaplacidus entry (HIP 45238) (bad for parsing)
A silent update seen on 2017-10-31:
 *fixes Miaplacidus entry
The update on 2017-11-19:
 *adds Ginan, Larawag and Wurren
 *adds a few notes at the end of the file
 *changes order of columns
The update on 2018-10-11:
 *adds a new ID column with the utf-8 greek letter symbolic identifier
 *adds Gudja, Guniibuu, Imai, La Superba, Paikauhale, Toliman
The update on 2022-07-05:
 *adds validation for TrES and BD star designators
 *accepts bayer designations with Ab-z, not only α-ω.
 *accepts the latin Y in designations, which should not be an allowed Bayer designation, but is used on HR 4846 (La Superba) in several sources.
 *accepts an empty ("_") band for magnϕude. Used in PSR B1257+12 (Lich).
The update on 2024-07-01:
 *Adds preprocessors as fallbacks for validation failures. This addresses a unicode difference for the greek lowercase letter "phi" and an empty field which should have an underscore.
 *Changed the greek letter index to account for two unicode inconsistencies in the original reference file with the letters "mu" and "omicron".
 *The normalized txt file now reflects the unicode correction and the empty field correction.
 *Replaces [0-9] with \d on regular expressions to silence linter warnings.
 *Uses "Ruff" to format the code.
"""

import os
import collections
import json
import re
from urllib import request
import difflib

# Greek letter mappings (UTF-8 codes)
# Modified from http://simbad.u-strasbg.fr/guide/chA.htx
# fmt:off
greek = {
    "alf": "α", "bet": "β", "gam": "γ", "del": "δ", "eps": "ε",
    "zet": "ζ", "eta": "η", "tet": "θ", "iot": "ι", "kap": "κ",
    "lam": "λ", "mu": "μ", "nu": "ν", "ksi": "ξ", "omi": "ο",
    "pi": "π", "rho": "ρ", "sig": "σ", "tau": "τ", "ups": "υ",
    "phi": "φ", "khi": "χ", "psi": "ψ", "ome": "ω",
}
# fmt:on

# Create output directory
if not os.path.exists("catalog_data"):
    print('Creating folder "catalog_data"...')
    os.makedirs("catalog_data")

# Download or use existing catalog file
catalog_local_copy = "catalog_data/IAU-CSN.txt"
not_downloaded = False

if os.path.exists(catalog_local_copy):
    print(f"{catalog_local_copy} already exists. Using existing file.")
    print("Delete the file and run this script again to download the current version.")
    not_downloaded = True
else:
    print("Downloading star names from WGSN...")
    local_proxies = request.getproxies()
    if local_proxies:
        print("Proxy server found. Using", local_proxies)
        request.install_opener(request.build_opener(request.ProxyHandler(local_proxies)))
    request.urlretrieve("http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt", catalog_local_copy)

# Preprocessing functions
def dummy_preprocess(value):
    return value

def lowercase_preprocess(value):
    """
    Normalize the character "ϕ" (unicode U+03D5 "Greek Phi Symbol ϕ")
      to "φ" (unicode U+03C6 "Greek Small Letter Phi φ")for consistency.
    """
    return value.upper().lower().strip()

def empty_to_underscore_preprocess(value):
    """Convert empty values to underscores."""
    return "_" if value == "" else value

# Column definitions with validation rules
# description, [start col, end col], alignment, validator, preprocessor
# fmt:off
columns = [
    ["Name/ASCII", [1, 17], "left", re.compile("[A-Z][a-z']+( [A-Z][a-z]+)?").fullmatch, dummy_preprocess],
    ["Name/Diacritics", [19, 35], "left", re.compile(".*").fullmatch, dummy_preprocess],
    ["Designation", [37, 48], "left", re.compile("((HR |HD |GJ |WASP-|HAT-P-|XO-|HIP |TrES-|BD[+-]\d{1,2} )\d{1,6}|PSR .+)").fullmatch, dummy_preprocess],
    ["ID", [50, 54], "left", re.compile("([A-Za-z]{0,3}\d{0,4}|_)").fullmatch, dummy_preprocess],
    ["ID/Diacritics", [56, 60], "left", re.compile("(V\d+|[α-ωb-zAY]{0,3}\d{0,4}|_)").fullmatch, lowercase_preprocess],
    ["Con", [62, 64], "left", re.compile("(_|[A-Z][A-Za-z]{2})").fullmatch, dummy_preprocess],
    ["#", [66, 69], "left", re.compile("(_|A|Aa|Aa1|C|Ca|B)").fullmatch, empty_to_underscore_preprocess],
    ["WDS_J", [71, 80], "left", re.compile("(_|(\d{5}[-+]\d{4}))").fullmatch, dummy_preprocess],
    ["mag", [82, 86], "right", lambda x: x == "_" or (float(x) > -2 and float(x) < 13), dummy_preprocess],
    ["bnd", [88, 89], "right", re.compile("[GV_]").fullmatch, dummy_preprocess],
    ["HIP", [91, 96], "right", re.compile("(\d{1,6}|_)").fullmatch, dummy_preprocess],
    ["HD", [98, 103], "right", re.compile("(\d{1,6}|_)").fullmatch, dummy_preprocess],
    ["RA(J2000)", [105, 114], "right", lambda x: float(x) >= 0 and float(x) <= 360, dummy_preprocess],
    ["Dec(J2000)", [116, 125], "right", lambda x: float(x) >= -90 and float(x) <= 90, dummy_preprocess],
    ["Date", [127, 136], "right", re.compile("20[12]\d-(1[0-2]|0[1-9])-(3[01]|[12]\d|0[1-9])").fullmatch, dummy_preprocess],
    ["notes", [138, 138], "right", re.compile("[*@]?").fullmatch, dummy_preprocess],
]
# fmt:on

# Validate column definitions
for c in columns:
    assert c[1][1] >= c[1][0], "Invalid column interval"
    assert c[2] in ["left", "right"], "Invalid alignment"
for i in range(len(columns) - 1):
    assert columns[i + 1][1][0] - columns[i][1][1] == 2, "Invalid spacing between columns"

# Parse the catalog
raw_lines = open(catalog_local_copy, "r").readlines()
json_data = []
normalized_lines = []
csv_lines = ["\t".join(i[0] for i in columns)]  # CSV header

for line in raw_lines:
    line = line.strip("\r\n\t ")
    if not line:
        normalized_lines.append("")
        continue
    if line[0] in "#$":
        normalized_lines.append("#" + line[1:])
        continue

    entry = collections.OrderedDict()
    csv_line = []
    normalized_line = []

    for key, interval, alignment, validator, preprocessor in columns:
        value = line[interval[0] - 1 : interval[1]].strip()

        if not validator(value):
            preprocessed_value = preprocessor(value)
            if preprocessed_value != value:
                print(f"Warning: Preprocessing applied for {key}. Original: '{value}', Preprocessed: '{preprocessed_value}'")

            if not validator(preprocessed_value):
                print(f"Failed validation of {key}: value '{value}' is unexpected.")
                print(line)
                print("Continuing with unchanged value.")
                print("")
            else:
                value = preprocessed_value

        entry[key] = value
        csv_line.append(value)
        normalized_value = value.ljust(interval[1] - interval[0] + 1) if alignment == "left" else value.rjust(interval[1] - interval[0] + 1)
        normalized_line.append(normalized_value)

    json_data.append(entry)
    csv_lines.append("\t".join(csv_line))
    normalized_lines.append(" ".join(normalized_line))

# Generate output files
normalized_text = "\n".join(normalized_lines) + "\n"
csv_text = "\n".join(csv_lines) + "\n"

print("Recording normalized catalog...")
with open("catalog_data/IAU-CSN_normalized.txt", "w", newline="\n") as f:
    f.write(normalized_text)

print("Recording csv catalog with tab separator...")
with open("catalog_data/IAU-CSN.tsv", "w", newline="\n") as f:
    f.write(csv_text)

print("Recording json catalog...")
with open("catalog_data/IAU-CSN.json", "w", newline="\n") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

# Compare original and normalized files
original_lines = [line.rstrip() + "\n" for line in raw_lines]
normalized_lines = [line.rstrip() + "\n" for line in normalized_lines]
diffs = list(difflib.context_diff(original_lines, normalized_lines, fromfile=catalog_local_copy, tofile="catalog_data/IAU-CSN_normalized.txt", n=0))

if not diffs:
    print("The downloaded catalog and the normalized catalog have no significant differences.")
else:
    print("The downloaded catalog and the normalized catalog have differences:")
    print("".join(diffs))

print("Processing complete.")

if not_downloaded:
    print("Note: Used existing IAU-CSN.txt file. Delete it to download the latest version.")
