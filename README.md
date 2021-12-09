# galaxy-tool-metadata-harvester

Collect metadata such as occurrence status and images from Naturalis, BOLD and ALA api's
using BLAST identifications or accepted taxonomic names.

Definitions for all occurrence status codes can be found on this page:  
https://www.nederlandsesoorten.nl/content/occurrence-status

Sample names can not start with a "#".  
All columns in a OTU table should have a header starting with "#".

### Installing
Install the tool by cloning this repo in the Galaxy Tool folder:
```
sudo git clone https://github.com/naturalis/galaxy-tool-metadata-harvester
```
Make the tool visible by adding it to **tool_conf.xml**:\
_/home/galaxy/galaxy/config/tool_conf.xml_
```
<tool file="/home/galaxy/Tools/galaxy-tool-metadata-harvester/"/>
```

## Source(s)
* Naturalis API [website](http://docs.biodiversitydata.nl/en/latest/introduction/)
* Nederlands Soortenregister [website](https://www.nederlandsesoorten.nl/)
* Atlas of Living Australia API [website](https://api.ala.org.au/)
* __Ratnasingham S, Hebert PDN__,  
  BOLD: The Barcode of Life Data System.  
  Molecular Ecology Notes. 2007; 7(3). __doi: 10.1111/j.1471-8286.2007.01678.x__  
  [BOLD](http://www.boldsystems.org/index.php/resources/api)
* __Giardine B, Riemer C, Hardison RC, Burhans R, Elnitski L, Shah P__,  
  Galaxy: A platform for interactive large-scale genome analysis.  
  Genome Research. 2005; 15(10) 1451-1455. __doi: 10.1101/gr.4086505__  
  [Galaxy](https://www.galaxyproject.org/)

_The [origal source](https://github.com/JasperBoom/galaxy-tools-naturalis-internship) for this repo by Jasper Boom._
