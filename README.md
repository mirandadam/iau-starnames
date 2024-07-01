# IAU Star Names Catalog Processor

This project downloads, processes, and formats the official star names published by the IAU Working Group on Star Names (WGSN).

I am not affiliated with nor endorsed by the IAU. This work is part of my master's dissertation experiments with star trackers.

## Purpose

The main goal is to provide easy-to-use versions of the IAU Catalog of Star Names (CSN) in various formats, including JSON and TSV.

## How to Use

1. Ensure you have Python 3 installed.
2. To update the catalog:
   a. Delete the file `catalog_data/IAU-CSN.txt` if it exists.
   b. Run `python3 download.py`.
3. The script will download the latest catalog and generate the following files in the `catalog_data` folder:
   - `IAU-CSN.txt`: Original downloaded file
   - `IAU-CSN.json`: Parsed version in JSON format
   - `IAU-CSN.tsv`: Parsed version in tab-separated format
   - `IAU-CSN_normalized.txt`: Cleaned and aligned version of the original file

Note: If `IAU-CSN.txt` already exists, the script will use it instead of downloading a new one.

## Catalog Description

The IAU Catalog of Star Names (IAU-CSN) is produced by the [IAU Working Group on Star Names](https://www.iau.org/science/scientific_bodies/working_groups/280/). It's important to note that this is not a comprehensive star catalog, but rather a list of officially named stars.

### File Format

The original `IAU-CSN.txt` file contains:

- A preamble explaining the contents
- Fixed-width columns with attributes such as Name, Designation, RA(J2000), Dec(J2000), etc.
- For full details, refer to the preamble in the file itself.

### Identifier Prefixes

The catalog uses various identifier prefixes, including:

- HR: Bright Star Catalogue
- HIP: Hipparcos catalogue
- HD: Henry Draper Catalogue
- GJ, GL, WO: Gliese Catalogue of Nearby Stars
- PSR: Pulsating Source of Radio (Pulsar)
- WDS_J: The Washington Double Star Catalog

For a more comprehensive list of star catalog prefixes, see [Wikipedia's list](https://en.wikipedia.org/wiki/Star_catalogue).

## Update History

The IAU_CSN.txt data file in this repository was last synced with the IAU on 2022-07-04. The IAU_CSN_normalized.txt file is intended to make machine parsing easier. Ideally, this should be the same as the original file, but there have been instances where the original file contained alignment errors.

### 2024-07-01

- No changes to the original file
- Code updated to handle unicode inconsistencies
- Added fallback method for failed field validations
- IAU-CSN_normalized.txt and other generated files now reflect these changes

### 2022-07-04

- 2 records added, 3 records updated
- Unurgunite renamed to Nganurganity
- "$" (likely a typo) introduced in the header
- Changed escaped unicode to plain unicode in .json output

### 2020-10-26

- Added two columns: "bnd" and "Name/Diacritics"
- Renamed "Name" to "Name/ASCII", "Vmag" to "mag", and "Approved" to "Date"
- Second "ID" column now called "ID/Diacritics"
- Changed treatment of "*" characters (now preferred over "-" for empty fields)
- Noted potential errors: Elgafar star greek id uses capital "phi", Mebsuta star missing "*" in column 7

### 2018-10-11

- Added greek letter identifier column
- 6 star records added
- Replaced more '_' occurrences with '-'

### 2018-08-30

- 4 star records updated, 15 new records added
- Polaris Australis HR 7228: '-' fields replaced with '_'
- Normalization now replaces every '_' with '-'

### 2017-11-28

- Differences between normalized and original files limited to blank spaces

### 2017-10-31

- Miaplacidus entry fixed in original catalog
- No differences between normalized and original versions

### 2017-10-28

- IAU file format changed
- Only difference in normalized version: fixed entry for Miaplacidus

## Resources

- [IAU Catalog of Star Names (Online)](https://www.iau.org/public/themes/naming_stars/): Includes historical context on star naming.
- [IAU-CSN (Text File)](http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt): Latest plain text catalog.
- [IAU Working Group on Star Names](https://www.iau.org/science/scientific_bodies/working_groups/280/): Official working group website.
- [Hipparcos Catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/311): 117,955 stars, no star names.
- [Bright Star Catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?V/50): 9,110 stars, includes star names.
- [Gaia Data Release 2](https://www.cosmos.esa.int/web/gaia/dr2): 1,692,919,135 light sources.
- [Washington Visual Double Star Catalog](http://www.usno.navy.mil/USNO/astrometry/optical-IR-prod/wds/WDS): Constantly updated, over 140,000 entries.

## License

This code is released under the MIT license.

The IAU Catalog of Star Names is distributed under the Creative Commons Attribution license. Users are free to use it worldwide, in perpetuity, as long as the source is mentioned.

For the official catalog, please refer to: [IAU-CSN](http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt)
