# *iau-starnames*
This code will download and parse official star names published by the IAU Working Group on Star Names (WGSN) from [IAU-CSN](http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt)

I am not affiliated with nor endorsed by the IAU. This work is part of my master's dissertation experiments with star trackers.

**The IAU Catalog of Star Names is not a "full" star catalog**, it's intent is to list the official names for the stars it contains and uniquely identify those stars. For more complete catalogs, try the full [Hipparcos catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/311) (117955 stars, complete to magnitude 7.3[reference needed], does not have star names) or the simpler [Bright Star Catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?V/50) (9110 stars, complete to magnitude 6.5[reference needed], has star names). If you need a larger dataset, the [Gaia Mission](https://www.cosmos.esa.int/web/gaia/home) has published the [Gaia Data Release 2](https://www.cosmos.esa.int/web/gaia/dr2) downloadable [here](http://cdsarc.u-strasbg.fr/viz-bin/cat?I/345) with 1,692,919,135 light sources, and features the distance and motion parameters of more than 1 billion stars.

## *How to use*

To update the catalog, **remove catalog_data/IAU-CSN.txt** and run download.py (python 3 is required). This will download the latest catalog_data/IAU-CSN.txt file from the IAU and rebuild the other files in the folder.

download.py will produce a warning and will not download a newer IAU-CSN.txt file if the old one is present.

The following files will be rebuilt:
* [catalog_data/IAU-CSN.txt](catalog_data/IAU-CSN.txt) will be downloaded from [IAU-CSN](http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt)
* [catalog_data/IAU-CSN.json](catalog_data/IAU-CSN.json) is the parsed version of the catalog in json format.
* [catalog_data/IAU-CSN.csv](catalog_data/IAU-CSN.csv) is the parsed version of the catalog in a tab separated format (TSV). The CSV extension is used for compatibility.
* [catalog_data/IAU-CSN_normalized.txt](catalog_data/IAU-CSN_normalized.txt) is a cleaner, aligned version of the original file.

The IAU-CSN.txt original file is mirrored in this repository to keep a version history.


## *Catalog description*

The Catalog of Star Names (IAU-CSN) is produced by the [IAU Working Group on Star Names](https://www.iau.org/science/scientific_bodies/working_groups/280/). It is published [online](https://www.iau.org/public/themes/naming_stars/) as bulletins and as a plain text file which can be downloaded at http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt.

### *Catalog Preamble*

The [text file](catalog_data/IAU-CSN.txt) contains a preamble explaining it's contents and displays fixed-width columns with the attributes: Name, Designation, RA(J2000), Dec(J2000), Vmag, ID, Con, #, WDS_J, HIP#, HD# and Approved. See the preamble for further information.

### *Identifier prefixes*

Used in the IAU-CSN:

* HR - [Bright Star Catalogue (Harvard Revised Photometry)](https://en.wikipedia.org/wiki/Bright_Star_Catalogue)
* HIP - [Hipparcos catalogue](https://en.wikipedia.org/wiki/Hipparcos)
* HD - [Henry Draper Catalogue](https://en.wikipedia.org/wiki/Henry_Draper_Catalogue)
* GJ, GL, WO - [Gliese Catalogue of Nearby Stars](https://en.wikipedia.org/wiki/Gliese_Catalogue_of_Nearby_Stars)
* PSR - [Pulsating Source of Radio](https://en.wikipedia.org/wiki/PSR_B1257%2B12) - Pulsar
* WDS_J - [The Washington Double Star Catalog](http://www.usno.navy.mil/USNO/astrometry/optical-IR-prod/wds/WDS)

Other catalogs:

* BD - [Bonner Durchmusterung](https://en.wikipedia.org/wiki/Durchmusterung)
The BD is supplemented by the Cordoba Durchmusterung (CD) and the Cape Durchmusterung for stars in the southern hemisphere.
* GC - [General Catalogue of Boss](https://en.wikipedia.org/wiki/Boss_General_Catalogue)
* SAO - [Smithsonian Astrophysical Observatory Catalogue](https://en.wikipedia.org/wiki/Smithsonian_Astrophysical_Observatory_Star_Catalog)
* PPM - [Positions and Proper Motions Catalogue](https://en.wikipedia.org/wiki/PPM_Star_Catalogue)

For the wikipedia list of prefixes, see [here](https://en.wikipedia.org/wiki/Star_catalogue)

## *Updates*
The IAU_CSN.txt data file was last synced with the IAU on 2020-01-25.

The IAU_CSN_normalized.txt file is intended to make machine parsing easier. Ideally this should be the same as the original file, but there have been points in time in which the original file contained alignment errors.
* As of 2017-10-28, the IAU file format has changed, and the only difference to the normalized version is the fixing of the entry for Miaplacidus.
* As of 2017-10-31, Miaplacidus entry was fixed. There is no difference between the normalized and the original versions.
* As of 2017-11-28, the differences between the normalized file and the original are limited to blank spaces.
* As of 2018-08-30, 4 star records were updated and 15 more have been added. Polaris Australis HR 7228 had the '-' fields replaced with '\_' for some reason. Normalization will replace every '\_' with '-'.
* As of 2018-10-11, a greek letter identifier column has been added and 6 star records have been added. More '\_' occurrences that have been all replaced with '-'.

## *Resources*

* [Online IAU Catalog of Star Names](https://www.iau.org/public/themes/naming_stars/) with historical context on how stars are named.

* Latest plain text catalog: [IAU-CSN](http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt)

* [IAU Working Group on Star Names Website](https://www.iau.org/science/scientific_bodies/working_groups/280/).

* [Hipparcos catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/311) (117955 stars, does not have star names)

* [Bright Star Catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?V/50) (9110 stars, has star names)

* [Gaia Data Release 2](https://www.cosmos.esa.int/web/gaia/dr2) (1,692,919,135 light sources)

* [Washington Visual Double Star Catalog](http://cdsarc.u-strasbg.fr/viz-bin/Cat?B/wds), direct [USNO link](http://www.usno.navy.mil/USNO/astrometry/optical-IR-prod/wds/WDS) (constantly updated, more than 140000 entries)

## *License*
This code is released under the MIT license.

The IAU catalog mirrored here is distributed under the Creative Commons Attribution (i.e. free to use in all perpetuity, world-wide, as long as the source is mentioned).
