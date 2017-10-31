#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
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
'''

import os
import collections
import json
import re
from urllib import request

# UTF-8 codes for greek letters from http://simbad.u-strasbg.fr/guide/chA.htx
greek = {'alf': 'α',
         'bet': 'β',
         'gam': 'γ',
         'del': 'δ',
         'eps': 'ε',
         'zet': 'ζ',
         'eta': 'η',
         'tet': 'θ',
         'iot': 'ι',
         'kap': 'κ',
         'lam': 'λ',
         'mu': 'µ',
         'nu': 'ν',
         'ksi': 'ξ',
         'omi': 'o',
         'pi': 'π',
         'rho': 'ρ',
         'sig': 'σ',
         'tau': 'τ',
         'ups': 'υ',
         'phi': 'φ',
         'khi': 'χ',
         'psi': 'ψ',
         'ome': 'ω'}

if not os.path.exists('catalog_data'):
    print('Creating folder "catalog_data"...')
    os.makedirs('catalog_data')

if os.path.exists('catalog_data/IAU-CSN.txt'):  # debug
    print('"catalog_data/IAU-CSN.txt" already exists.')
    print('Delete the file and run this script again to repeat the download.')
else:
    print('Downloading star names from WGSN...')
    request.urlretrieve('http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt',
                        'catalog_data/IAU-CSN.txt')  # debug

# columns - description, [start col, end col], alignment, validator
columns = [
    ['Name', [1, 17], 'left', re.compile('[A-Z][a-z\']+( [A-Z][a-z]+)?').fullmatch],
    ['Designation', [19, 32], 'left', re.compile('((HR|HD|GJ) [0-9]{1,6}|PSR .+)').fullmatch],
    ['RA(J2000)', [34, 43], 'right', lambda x: float(x) >= 0 and float(x) <= 360],
    ['Dec(J2000)', [45, 54], 'right', lambda x: float(x) >= -90 and float(x) <= 90],
    ['Vmag', [56, 61], 'right', lambda x: x == '-' or (float(x) > -2 and float(x) < 12)],
    ['ID', [63, 67], 'left', re.compile('([A-Za-z]{0,3}[0-9]{0,4}|-)').fullmatch],
    ['Con', [69, 71], 'left', re.compile('[A-Z][A-Za-z]{2}').fullmatch],
    ['#', [73, 75], 'left', re.compile('(-|A|Aa|Aa1|C|Ca)').fullmatch],
    ['WDS_J', [77, 86], 'left', re.compile('(-|([0-9]{5}[-+][0-9]{4}))').fullmatch],
    ['HIP#', [88, 94], 'right', re.compile('([0-9]{1,6}|-)').fullmatch],
    ['HD#', [96, 101], 'right', re.compile('([0-9]{1,6}|-)').fullmatch],
    ['Approved', [103, 112], 'right', re.compile('20[12][0-9]-(1[0-2]|0[1-9])-(3[01]|[12][0-9]|0[1-9])').fullmatch],
    ['notes', [114, 114], 'right', re.compile('[*@]?').fullmatch],
]
for c in columns:
    assert c[1][1] >= c[1][0]  # making sure the intervals make sense
    assert c[2] == 'left' or c[2] == 'right'  # making sure there is no typo in the alignment field
for i in range(len(columns) - 1):
    # making sure there is a space of exactly one between the values
    # that assumption is made to make parsing easier
    assert columns[i + 1][1][0] - columns[i][1][1] == 2

# parse the results
raw_lines = open('catalog_data/IAU-CSN.txt', 'r').readlines()
json_data = []
normalized_lines = []
csv_lines = []
csv_lines.append('\t'.join(i[0] for i in columns))  # csv header
for a in raw_lines:
    if not a.strip('\r\n\t '):
        # if it is an empty line, append an empty line
        normalized_lines.append('')
        continue  # go to next line
    if a[0] == '#':
        # if the first character is a '#', it is a comment - keep the line intact except for the blank spaces at the end and line termination
        normalized_lines.append(a.strip('\r\n\t '))
        continue  # go to next line
    # we split the values in the space boundaries:
    entry = collections.OrderedDict()
    csv_line = []
    normalized_line = []
    # loading values:
    for k, c in enumerate(columns):
        key = c[0]
        value = a[c[1][0] - 1: c[1][1]].strip('\r\t\n ')
        # validation:
        if not c[3](value):
            print('Failed validation of ', c[0])
            print(a)
        entry[key] = value
        csv_line.append(value)
        if c[2] == 'left':
            value = value.ljust(c[1][1] - c[1][0] + 1, ' ')
        else:
            value = value.rjust(c[1][1] - c[1][0] + 1, ' ')
        normalized_line.append(value)
    json_data.append(entry)
    # generating the csv lines:
    csv_lines.append('\t'.join(csv_line))
    normalized_lines.append(' '.join(normalized_line))
    del a, entry, csv_line, normalized_line  # optional cleanup


# join lines with a linebreak separator and finish with a last linebreak:
normalized_text = '\n'.join(normalized_lines) + '\n'
csv_text = '\n'.join(csv_lines) + '\n'

print('Recording normalized catalog...')
open('catalog_data/IAU-CSN_normalized.txt', 'w').write(normalized_text)

print('Recording csv catalog with tab separator...')
open('catalog_data/IAU-CSN.csv', 'w').write(csv_text)

print('Recording json catalog...')
open('catalog_data/IAU-CSN.json', 'w').write(json.dumps(json_data, indent=2))
print('done.')
