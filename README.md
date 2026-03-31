# IAU Star Names Catalog Processor

> **This repository is archived.** The upstream data source (hosted on `pas.rochester.edu`) has not been updated since April 2022 and appears to be offline. The IAU Working Group on Star Names has moved its official catalog to a new home. See [Alternatives](#alternatives) below for up-to-date sources.

This project downloaded, processed, and formatted the official star names published by the IAU Working Group on Star Names (WGSN). It was created as part of my master's dissertation experiments with star trackers.

I am not affiliated with nor endorsed by the IAU.

## Alternatives

For up-to-date IAU star name data, use one of these sources instead:

- **[IAU WGSN Official Catalog (exopla.net)](https://exopla.net/star-names/modern-iau-star-names/)** — The new canonical home of the catalog, with an interactive table and export options (CSV, PDF). See also the [catalogs download page](https://exopla.net/iau-wgsn-catalogs/).
- **[cyschneck/iau-star-names](https://github.com/cyschneck/iau-star-names)** — A community repo with automated weekly updates via GitHub Actions, providing CSV files with IAU names, Bayer IDs, constellations, etymological origins, and observational data.
- **[SIMBAD](https://simbad.u-strasbg.fr/)** — Resolves individual IAU star names to catalog identifiers and coordinates. Usable from Python via Astropy's `SkyCoord.from_name()`.

## What This Repo Did

The script `download.py` downloaded the IAU-CSN fixed-width text file, validated each entry against regex rules, and generated JSON, TSV, and normalized text outputs. The data files in `catalog_data/` reflect the state of the catalog as of **2022-07-04** (451 named stars). The IAU has since added approximately 40 more stars that are not reflected here.

## Update History

<details>
<summary>Click to expand full update history</summary>

The IAU_CSN.txt data file in this repository was last synced with the IAU on 2022-07-04.

### 2025-04-24

- No changes to the original file. Website seems to be down.
- Fixed minor typo in regexes.

### 2024-07-01

- No changes to the original file
- Code updated to handle unicode inconsistencies
- Added fallback method for failed field validations

### 2022-07-04

- 2 records added, 3 records updated
- Unurgunite renamed to Nganurganity

### 2020-10-26

- Added two columns: "bnd" and "Name/Diacritics"
- Renamed "Name" to "Name/ASCII", "Vmag" to "mag", and "Approved" to "Date"

### 2018-10-11

- Added greek letter identifier column
- 6 star records added

### 2018-08-30

- 4 star records updated, 15 new records added

### 2017-10-28 – 2017-11-28

- IAU file format changed
- Miaplacidus entry fixed in original catalog

</details>

## License

This code is released under the MIT license.

The IAU Catalog of Star Names is distributed under the Creative Commons Attribution license.
For the official catalog, please refer to the [IAU WGSN catalogs page](https://exopla.net/iau-wgsn-catalogs/).
