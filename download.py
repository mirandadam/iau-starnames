#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Download data from the IAU Working Group on Star Names (WGSN)

Website:
  https://www.iau.org/science/scientific_bodies/working_groups/280/
Data url:
  http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt


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
 *accepts an empty ("_") band for magnitude. Used in PSR B1257+12 (Lich).
"""

import os
import collections
import json
import re
from urllib import request
import difflib

# UTF-8 codes for greek letters from http://simbad.u-strasbg.fr/guide/chA.htx
greek = {
    "alf": "α",
    "bet": "β",
    "gam": "γ",
    "del": "δ",
    "eps": "ε",
    "zet": "ζ",
    "eta": "η",
    "tet": "θ",
    "iot": "ι",
    "kap": "κ",
    "lam": "λ",
    "mu": "µ",
    "nu": "ν",
    "ksi": "ξ",
    "omi": "o",
    "pi": "π",
    "rho": "ρ",
    "sig": "σ",
    "tau": "τ",
    "ups": "υ",
    "phi": "φ",
    "khi": "χ",
    "psi": "ψ",
    "ome": "ω",
}

if not os.path.exists("catalog_data"):
    print('Creating folder "catalog_data"...')
    os.makedirs("catalog_data")

not_downloaded = False
if os.path.exists("catalog_data/IAU-CSN.txt"):  # debug
    print('"catalog_data/IAU-CSN.txt" already exists. NOT downloading.')
    print("Generating TXT, JSON, and CSV files with old IAU-CSN.txt.")
    print(
        "Delete the file and run this script again to download the current version from the IAU."
    )
    not_downloaded = True
else:
    print("Downloading star names from WGSN...")
    # this will look for http_proxy and https_proxy environment variables:
    local_proxies = request.getproxies()
    if local_proxies:
        print("Proxy server found. Using", local_proxies)
        request.install_opener(
            request.build_opener(request.ProxyHandler(local_proxies))
        )
    request.urlretrieve(
        "http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt",
        "catalog_data/IAU-CSN.txt",
    )

# columns - description, [start col, end col], alignment, validator
columns = [
    [
        "Name/ASCII",
        [1, 17],
        "left",
        re.compile("[A-Z][a-z']+( [A-Z][a-z]+)?").fullmatch,
    ],
    ["Name/Diacritics", [19, 35], "left", re.compile(".*").fullmatch],
    [
        "Designation",
        [37, 48],
        "left",
        re.compile(
            "((HR |HD |GJ |WASP-|HAT-P-|XO-|HIP |TrES-|BD[+-][0-9]{1,2} )[0-9]{1,6}|PSR .+)"
        ).fullmatch,
    ],
    ["ID", [50, 54], "left", re.compile("([A-Za-z]{0,3}[0-9]{0,4}|_)").fullmatch],
    [
        "ID/Diacritics",
        [56, 60],
        "left",
        re.compile("(V[0-9]+|[α-ωb-zAY]{0,3}[0-9]{0,4}|_)").fullmatch,
    ],
    ["Con", [62, 64], "left", re.compile("(_|[A-Z][A-Za-z]{2})").fullmatch],
    ["#", [66, 69], "left", re.compile("(_|A|Aa|Aa1|C|Ca|B)").fullmatch],
    ["WDS_J", [71, 80], "left", re.compile("(_|([0-9]{5}[-+][0-9]{4}))").fullmatch],
    ["mag", [82, 86], "right", lambda x: x == "_" or (float(x) > -2 and float(x) < 13)],
    ["bnd", [88, 89], "right", re.compile("[G|V|_]").fullmatch],
    ["HIP", [91, 96], "right", re.compile("([0-9]{1,6}|_)").fullmatch],
    ["HD", [98, 103], "right", re.compile("([0-9]{1,6}|_)").fullmatch],
    ["RA(J2000)", [105, 114], "right", lambda x: float(x) >= 0 and float(x) <= 360],
    ["Dec(J2000)", [116, 125], "right", lambda x: float(x) >= -90 and float(x) <= 90],
    [
        "Date",
        [127, 136],
        "right",
        re.compile("20[12][0-9]-(1[0-2]|0[1-9])-(3[01]|[12][0-9]|0[1-9])").fullmatch,
    ],
    ["notes", [138, 138], "right", re.compile("[*@]?").fullmatch],
]
for c in columns:
    assert c[1][1] >= c[1][0]  # making sure the intervals make sense
    assert (
        c[2] == "left" or c[2] == "right"
    )  # making sure there is no typo in the alignment field
for i in range(len(columns) - 1):
    # making sure there is a space of exactly one between the values
    # that assumption is made to make parsing easier
    assert columns[i + 1][1][0] - columns[i][1][1] == 2

# parse the results
raw_lines = open("catalog_data/IAU-CSN.txt", "r").readlines()
json_data = []
normalized_lines = []
csv_lines = []
csv_lines.append("\t".join(i[0] for i in columns))  # csv header
for a in raw_lines:
    if not a.strip("\r\n\t "):
        # if it is an empty line, append an empty line
        normalized_lines.append("")
        continue  # go to next line
    if a[0] == "#" or a[0] == "$":
        # if the first character is a '#', it is a comment - keep the line intact except for the blank spaces at the end and line termination
        # $ as the beginning of a line is probably a typo
        a = "#" + a[1:]
        normalized_lines.append(a.strip("\r\n\t "))
        continue  # go to next line
    # we split the values in the space boundaries:
    entry = collections.OrderedDict()
    csv_line = []
    normalized_line = []
    # loading values:
    for k, c in enumerate(columns):
        key = c[0]
        value = a[c[1][0] - 1 : c[1][1]].strip("\r\n\t ")  # .replace('_', '-')
        # validation:
        if not c[3](value):  # trying to validate
            print(
                "Failed validation of ",
                c[0],
                ": column ",
                k + 1,
                ' value "',
                value,
                '" is unexpected.',
                sep="",
            )
            print(a.rstrip("\r\n\t "))
            print(" ... continuing anyway using the unchanged value.")
            print("")
        entry[key] = value
        csv_line.append(value)
        if c[2] == "left":
            value = value.ljust(c[1][1] - c[1][0] + 1, " ")
        else:
            value = value.rjust(c[1][1] - c[1][0] + 1, " ")
        normalized_line.append(value)
    json_data.append(entry)
    # generating the csv lines:
    csv_lines.append("\t".join(csv_line))
    normalized_lines.append(" ".join(normalized_line))
    del a, entry, csv_line, normalized_line  # optional cleanup


# join lines with a linebreak separator and finish with a last linebreak:
normalized_text = "\n".join(normalized_lines) + "\n"
csv_text = "\n".join(csv_lines) + "\n"

print("Recording normalized catalog...")
open("catalog_data/IAU-CSN_normalized.txt", "w", newline="\n").write(normalized_text)

# checking for differences in the normalized catalog:
a = [i.rstrip("\r\n\t ") + "\n" for i in raw_lines]
b = [i.rstrip("\r\n\t ") + "\n" for i in normalized_lines]
diffs = list(
    difflib.context_diff(
        a,
        b,
        fromfile="catalog_data/IAU-CSN.txt",
        tofile="catalog_data/IAU-CSN_normalized.txt",
        n=0,
    )
)
if not diffs:
    print(
        "  The downloaded catalog and the normalized catalog have no differences except for blank spaces at the end of lines."
    )
    print(
        "  (this does not mean that the data did not change from the previous version, it means that the normalization process did not alter the downloaded data too much)"
    )
else:
    print("  The downloaded catalog and the normalized catalog have differences:")
    print("".join(diffs))

print("Recording csv catalog with tab separator...")
open("catalog_data/IAU-CSN.tsv", "w", newline="\n").write(csv_text)

print("Recording json catalog...")
open("catalog_data/IAU-CSN.json", "w", newline="\n").write(
    json.dumps(json_data, indent=2, ensure_ascii=False)
)
print("done.")

if not_downloaded:
    print('"catalog_data/IAU-CSN.txt" already existed. NOT downloaded.')
    print("TXT, JSON, and CSV files generated with old IAU-CSN.txt.")
    print(
        "Delete catalog_data/IAU-CSN.txt and run this script again to download the current version from the IAU."
    )
