#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Download data from the IAU Working Group on Star Names (WGSN)

Website:
  https://www.iau.org/science/scientific_bodies/working_groups/280/
Data url:
  http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt
'''

import os
import collections
import json
from urllib import request

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

print('Normalizing the downloaded catalog...')
raw_lines = open('catalog_data/IAU-CSN.txt', 'r').readlines()
processed_lines = []
for i in raw_lines:
  a = i.strip('\r\n\t ')  # strip blanks and linebreaks
  if a[0] == '#':
    # if the first character is a '#' keep the rest of the line intact
    processed_lines.append(a)
  else:
    # fixing tabs. they seem to round to multiples of 8 in the original file.
    # split the line where there is a tab character in multiple sections:
    sections = a.split('\t')
    a = ''
    for j in sections:
      # append each section progressively
      a = a + j
      # pad with spaces to reach a multiple of 8 boundary:
      padding = ' ' * ((-len(a)) % 8)
      a = a + padding
      # make sure we got the length right:
      assert len(a) % 8 == 0
      del j, padding  # cleanup - optional
    # remove the extra spaces at the end of the last section:
    a = a.rstrip(' ')
    processed_lines.append(a)
  del i, a  # cleanup - optional
del raw_lines  # cleanup - optional

# join lines with a linebreak separator and finish with a last linebreak:
processed_text = '\n'.join(processed_lines) + '\n'
print('Recording normalized catalog...')
open('catalog_data/IAU-CSN_normalized.txt', 'w').write(processed_text)

# parse the results.
# columns - description, [start col, end col], alignment, validator
columns = [
    ['Name', [1, 18], 'left'],
    ['Designation', [19, 33], 'left'],
    ['RA(J2000)', [34, 43], 'right'],
    ['Dec(J2000)', [44, 54], 'right'],
    ['Vmag', [55, 61], 'right'],
    ['ID', [63, 68], 'left'],
    ['Con', [69, 72], 'left'],
    ['#', [73, 76], 'left'],
    ['HIP#', [77, 82], 'right'],
    ['HD#', [83, 89], 'left'],
    ['Approved', [91, 100], 'right']
]

json_data = []
for i in processed_lines:
  if i[0] == '#':
    # do not process comments.
    continue
  entry = collections.OrderedDict()
  for j in columns:
    key = j[0]
    value = i[j[1][0] - 1: j[1][1]].strip(' ')
    entry[key] = value
  json_data.append(entry)


print('Recording json catalog...')
open('catalog_data/IAU-CSN.json', 'w').write(json.dumps(json_data, indent=2))
print('done.')
