# *iau-starnames*
This code will download and parse official star names published by the IAU Working Group on Star Names (WGSN).

The data files were last synced with the IAU on 2017-10-12.

I am not affiliated with nor endorsed by the IAU. This is part of the code of my master's dissertation experiments with star trackers.

**The IAU Catalog of Star Names is not a "full" star catalog**, it's intent is to list the official names for the stars it contains and uniquely identify those stars. For larger catalogs, try the full [Hipparcos catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/311) (117955 stars, complete to magnitude 7.3[reference needed], does not have star names) or the simpler [Bright Star Catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?V/50) (9110 stars, complete to magnitude 6.5[reference needed], has star names). If you need a larger dataset, the [Gaia Mission](http://www.esa.int/Our_Activities/Space_Science/Gaia) has published the [Gaia Data Release 1](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/337) with 1142679769 light sources, and features the actual distance and motion parameters of more than 2 million stars.

## *How to use*

download.py will refuse to download a new IAU-CSN file if the old one is still present.

To update the catalog, remove catalog_data/IAU-CSN.txt and run download.py (python 3 is required). This will download the latest catalog_data/IAU-CSN.txt file from the IAU and rebuild the other files in the folder.

catalog_data/IAU-CSN.json is the parsed version of the catalog, and can be used directly.

catalog_data/IAU-CSN_normalized.txt is a cleaner, aligned version of the original file, intended to make machine parsing easier. Ideally this should be the same as the original file, but there have been points in time in which the original file contained alignment errors.


## *Catalog description*

The Catalog of Star Names (IAU-CSN) is published online as bulletins and as a plain text file which can be downloaded at http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt. See the links in the resources section for the published bulletins.

### *Catalog Preamble*

The [text file](catalog_data/IAU-CSN.txt) contains a preamble explaining it's contents and displays fixed-width columns with the attributes: Name, Designation, RA(J2000), Dec(J2000), Vmag, ID, Con, #, HIP#, HD# and Approved. See the preamble for further information.

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

### *Versions in this repository*
The [original text file](catalog_data/IAU-CSN.txt) is mirrored in this repository.

The code generates a [normalized version](catalog_data/IAU-CSN_normalized.txt), a [json version](catalog_data/IAU-CSN.json) and a [CSV version](catalog_data/IAU-CSN.csv). These versions are also stored in this repository.

The normalized version removes all spaces after the end of the lines, converts all line endings to a single line break character (all '\r\n' become '\n') and replace tabs ('\t') with the appropriate amount of spaces to respect alignment. All the changes should be invisible in the text editor used to generate the file, but will help when trying to convert the file to a table or writing a program to parse it.
* As of 2017-10-28, the IAU file format has changed, and the only difference to the normalized version is the fixing of the entry for Miaplacidus.
* As of 2017-10-31, Miaplacidus entry was fixed. Now there is no difference between the normalized version and the original version

The JSON version is the easiest version to parse, and can be used directly in websites.



## *Resources*

* [Online IAU Catalog of Star Names](https://www.iau.org/public/themes/naming_stars/) with historical context on how stars are named.

* Latest plain text catalog: [IAU-CSN](http://www.pas.rochester.edu/~emamajek/WGSN/IAU-CSN.txt)

* [IAU Working Group on Star Names Website](https://www.iau.org/science/scientific_bodies/working_groups/280/).

* [Hipparcos catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/311) (117955 stars, does not have star names)

* [Bright Star Catalogue](http://cdsarc.u-strasbg.fr/viz-bin/Cat?V/50) (9110 stars, has star names)

* [Gaia Data Release 1](http://cdsarc.u-strasbg.fr/viz-bin/Cat?I/337) (1142679769 light sources)

## *License*
This code is released under the MIT license.

The IAU catalog mirrored here is distributed under the Creative Commons Attribution (i.e. free to use in all perpetuity, world-wide, as long as the source is mentioned).
