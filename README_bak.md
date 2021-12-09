# galaxy-tool-metadata-harvester

__!!Repo can be deleted, copy is also kept [here](https://github.com/JasperBoom/galaxy-tools-naturalis-internship)!!.__

Use a python script to utilize the Naturalis, BOLD and ALA api's to collect meta data.  
The MetaData tool will utilize the Naturalis, BOLD and ALA api's to collect meta data such as occurrence status and images based on BLAST identifications or accepted taxonomic names.

Definitions for all occurrence status codes can be found on this page:  
https://www.nederlandsesoorten.nl/content/occurrence-status

Sample names can not start with a "#".  
All columns in a OTU table should have a header starting with "#".

# Getting started

### Prerequisites
Download and install the following software according to the following steps.
```
sudo apt-get install python-pip
sudo pip install pandas
```

### Installing
Download and install the tool according to the following steps.
```
sudo mkdir -m 755 /home/Tools
cd /home/Tools
sudo git clone https://github.com/JasperBoom/galaxy-tool-metadata-harvester
sudo chmod -R 755 galaxy-tool-metadata-harvester
```
The following file in the galaxy-tool-metadata-harvester folder should be made avaible from any location.
```
sudo ln -s /home/Tools/galaxy-tool-metadata-harvester/getMetaData.py /usr/local/bin/getMetaData.py
```
Continue with the tool installation
```
sudo mkdir -m 755 /home/galaxy/tools/directoryname
sudo cp /home/Tools/galaxy-tool-metadata-harvester/getMetaData.sh /home/galaxy/tools/directoryname/getMetaData.sh
sudo cp /home/Tools/galaxy-tool-metadata-harvester/getMetaData.xml /home/galaxy/tools/directoryname/getMetaData.xml
```
Edit the following file in order to make galaxy display the tool.
```
/home/galaxy/config/tool_conf.xml
```
```
<tool file="airdentification/getMetaData.xml"/>
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

```
Copyright (C) 2018 Jasper Boom

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License version 3 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```
