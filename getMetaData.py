#!/usr/bin/python
# Copyright @2001-2019 Python Software Foundation

# Author: Jasper Boom

# Prequisites:
# - sudo apt-get install python
# - sudo apt-get install python-pip
# - sudo pip install pandas

# Galaxy prequisites:
# - sudo ln -s /path/to/folder/galaxy-tool-metadata/getMetaData.py 
#              /usr/local/bin/getMetaData.py

# Imports
import os
import sys
import argparse
import re
import math
import itertools
import pandas as pd
import subprocess as sp

# The getDownload function.
# This function downloads a image based on the getPictureUrl function output.
# The name of such a image consists of [OTU_ID]-[species_name]-[database].
def getDownload(strUrl):
    rafDownload = sp.Popen(["wget", "-O", strUrl[1], strUrl[0]], stdout=sp.PIPE, 
                           stderr=sp.PIPE)
    strOut, strError = rafDownload.communicate()

# The getPictureUrl function.
# This function calls a database api [Naturalis/BOLD/ALA] and searches through
# the output for a specific string. This string differs depending on what
# database is being searched. After finding this string, the image link is
# isolated. In the case of the BOLD database, a small edit needs to be applied
# in order to create a correct http format. This http link, along with a species
# name linked by _ is returned as output.
def getPictureUrl(strCommand, strStart, strOutputPath, strOtu, lstSpecies,
                  strDatabase):
    rafApi = sp.Popen(["curl", "-X", "GET", strCommand], stdout=sp.PIPE, 
                      stderr=sp.PIPE)
    strOut, strError = rafApi.communicate()
    try:
        intUrlStart = re.search(strStart, strOut).end()
        intUrlEnd = re.search('"', strOut[intUrlStart+3:]).start()
        strDownload = strOut[intUrlStart+3:][:intUrlEnd]
        strSpeciesName = "_".join(lstSpecies)
        strPictureFile = strOutputPath + strOtu + "-" + strSpeciesName + "-" +\
                         strDatabase + ".jpg"
        if strDatabase == "BOLD":
            strDownload = strDownload.replace("\\", "")
        else:
            pass
        return strDownload, strPictureFile
    except AttributeError:
        pass

# The getBoldApi function.
# This function creates a api string with the provided name. This api string is
# based on the BOLD api backbone. The created api string is included in the call
# of the getPictureUrl function.
def getBoldApi(strSpeciesCommand, strOutputPath, strOtu, lstSpecies):
    strBoldCommand = "http://www.boldsystems.org/index.php/API_Public/" +\
                     "specimen?taxon=" + strSpeciesCommand + "&format=json"
    strBoldUrl = getPictureUrl(strBoldCommand, "image_file", strOutputPath,
                               strOtu, lstSpecies, "BOLD")
    return strBoldUrl

# The getAlaApi function.
# This function creates a api string with the provided name. This api string is
# based on the ALA api backbone. The created api string is included in the call
# of the getPictureUrl function.
def getAlaApi(strSpeciesCommand, strOutputPath, strOtu, lstSpecies):
    strAlaCommand = "http://bie.ala.org.au/ws/search.json?q=" +\
                    strSpeciesCommand + "&facets=imageAvailable"
    strAlaUrl = getPictureUrl(strAlaCommand, "imageUrl", strOutputPath,
                                strOtu, lstSpecies, "ALA")
    return strAlaUrl

# The getPicture function.
# This function loops through the names column and OTU column. Every name is 
# transformed into a correct format in order to support the database api's. The
# first database called in this function is the Naturalis database. If that call
# does not provide a image, the BOLD database is called. If the call does
# provide a file, but its a empty one, the BOLD database is also called. These
# same rules apply to the BOLD calls. Which means the ALA database is called.
# No result after the ALA call, means no image.
def getPicture(tblReadInput, strOutputPath, tblSpecies):
    tblOtu = tblReadInput.iloc[:,0]
    for strOtu, strSpecies in itertools.izip(tblOtu, tblSpecies):
        try:
            lstSpecies = strSpecies.split()
            strSpeciesCommand = "%20".join(lstSpecies).lower()
            # Naturalis database.
            strNaturalisCommand = "http://api.biodiversitydata.nl/v2/multi" +\
                                  "media/query?identifications.scientific" +\
                                  "Name.scientificNameGroup=" +\
                                  strSpeciesCommand + "&_fields=service" +\
                                  "AccessPoints"
            strNaturalisUrl = getPictureUrl(strNaturalisCommand, "accessUri",
                                            strOutputPath, strOtu, lstSpecies,
                                            "NATURALIS")
            if strNaturalisUrl:
                getDownload(strNaturalisUrl)
                if os.stat(strNaturalisUrl[1]).st_size == 0:
                    rafRemove = sp.call(["rm", strNaturalisUrl[1]])
                    # BOLD database.
                    strBoldUrl = getBoldApi(strSpeciesCommand, strOutputPath,
                                            strOtu, lstSpecies)
                    if strBoldUrl:
                        getDownload(strBoldUrl)
                        if os.stat(strBoldUrl[1]).st_size == 0:
                            rafRemove = sp.call(["rm", strBoldUrl[1]])
                            # ALA database.
                            strAlaUrl = getAlaApi(strSpeciesCommand, 
                                                  strOutputPath, strOtu,
                                                  lstSpecies)
                            if strAlaUrl:
                                getDownload(strAlaUrl)
                                if os.stat(strAlaUrl[1]).st_size == 0:
                                    rafRemove = sp.call(["rm", strAlaUrl[1]])
                                else:
                                    pass
                            else:
                                pass
                        else:
                            pass
                    else:
                        # ALA database.
                        strAlaUrl = getAlaApi(strSpeciesCommand, strOutputPath,
                                              strOtu, lstSpecies)
                        if strAlaUrl:
                            getDownload(strAlaUrl)
                            if os.stat(strAlaUrl[1]).st_size == 0:
                                rafRemove = sp.call(["rm", strAlaUrl[1]])
                            else:
                                pass
                        else:
                            pass
                else:
                    pass
            else:
                # BOLD database.
                strBoldUrl = getBoldApi(strSpeciesCommand, strOutputPath,
                                        strOtu, lstSpecies)
                if strBoldUrl:
                    getDownload(strBoldUrl)
                    if os.stat(strBoldUrl[1]).st_size == 0:
                        rafRemove = sp.call(["rm", strBoldUrl[1]])
                        # ALA database.
                        strAlaUrl = getAlaApi(strSpeciesCommand, strOutputPath, 
                                              strOtu, lstSpecies)
                        if strAlaUrl:
                            getDownload(strAlaUrl)
                            if os.stat(strAlaUrl[1]).st_size == 0:
                                rafRemove = sp.call(["rm", strAlaUrl[1]])
                            else:
                                pass
                        else:
                            pass
                    else:
                        pass
                else:
                    # ALA database.
                    strAlaUrl = getAlaApi(strSpeciesCommand, strOutputPath,
                                              strOtu, lstSpecies)
                    if strAlaUrl:
                        getDownload(strAlaUrl)
                        if os.stat(strAlaUrl[1]).st_size == 0:
                            rafRemove = sp.call(["rm", strAlaUrl[1]])
                        else:
                            pass
                    else:
                        pass
        except AttributeError:
            pass

# The getOccurrenceStatus function.
# This function loops through the names column generated by the
# getNameColumn function. Every name is transformed into a correct format in
# order to support the Naturalis bioportal api. The Naturalis bioportal api is
# called. The word "occurrenceStatusVerbatim" is searched for in the output of
# the api. The value after the word occurrenceStatusVerbatim is isolated and
# this value is added to the list lstStatus. If no value can be found, a empty
# string is added to the list lstStatus. After every species name is processed,
# the list lstStatus is added to the input file as a new column and outputted as
# a new file.
def getOccurrenceStatus(tblReadInput, strOutputPath, tblSpecies):
    dicOccurrence = {"0": "Reported", "0a": "Reported correctly, to be refined",
                     "1": "Indigenous (undetermined)",
                     "1a": "Indigenous: native species",
                     "1b": "Indigenous: incidental/periodical species",
                     "2": "Introduced (undetermined)",
                     "2a": "Introduced: at least 100 years independent survival",
                     "2b": "Introduced: 10-100 years independent survival",
                     "2c": "Introduced: less than 10 years independent survival",
                     "2d": "Introduced: incidental import", "3a": "Data deficient",
                     "3b": "Incorrectly reported", "3c": "To be expected",
                     "3d": "Incorrectly used name (auct.)", "4": "Miscellaneous"}
    lstStatus = []
    for strRow in tblSpecies:
        try:
            lstSpecies = strRow.split()
            strSpeciesCommand = "%20".join(lstSpecies).lower()
            strCommand = "http://api.biodiversitydata.nl/v2/taxon/query?" +\
                         "acceptedName.scientificNameGroup=" +\
                         strSpeciesCommand +\
                         "&_fields=occurrenceStatusVerbatim"
            rafNaturalisApi = sp.Popen(["curl", "-X", "GET", strCommand],
                                       stdout=sp.PIPE, stderr=sp.PIPE)
            strOut, strError = rafNaturalisApi.communicate()
            intOccurrenceStart = re.search("occurrenceStatusVerbatim", 
                                           strOut).end()
            strOccurrence = strOut[intOccurrenceStart+3:intOccurrenceStart+5]
            strOccurrenceTotal = strOccurrence.strip(" ") + " " +\
                                 dicOccurrence[str(strOccurrence)]
            lstStatus.append(strOccurrenceTotal)
        except AttributeError:
            lstStatus.append("")
    tblReadInput["OccurrenceStatus"] = lstStatus
    strOutputPath = strOutputPath + "flNewOutput.tabular"
    tblReadInput.to_csv(strOutputPath, sep="\t", encoding="utf-8", index=False)

# The getNameColumn function.
# This function isolates a list of names used for the metadata processes. When
# processing a OTU file with standard BLAST identifications the names are
# isolated based on the taxonomy column at the end of a OTU file. Species names
# are extracted from the taxonomy column. When processing a OTU file with a LCA
# process file, the names are extracted from the lowest common ancestor column.
# When processing a accepted taxonomic name file, the names are extracted from
# the third column, but if a row is empty, the name in the second column is
# used. When processing a BLAST file, the names are isolated from the taxonomy
# column and extracted per row. Depending on what type of meta data the user
# wants, the species column is send to the correct functions.
def getNameColumn(flInput, flOutput, strProcess, strFormat):
    tblReadInput = pd.read_table(flInput)
    if strFormat == "otu_old":
        intColumnLength = 11
    elif strFormat == "otu_new":
        intColumnLength = 10
    else:
        pass
    if strFormat == "accepted":
        intCounter = 0
        lstSpecies = []
        for strRow in tblReadInput.iloc[:,2]:
            try:
                if math.isnan(strRow) == True:
                    lstSpecies.append(tblReadInput.iloc[:,1][intCounter])
            except TypeError:
                lstSpecies.append(strRow)
            intCounter += 1
    elif strFormat == "otu_old" or strFormat == "otu_new":
        lstSpecies = []
        intFiles = 0
        for strHeader in list(tblReadInput):
            if strHeader[:1] != "#" and strHeader[:7] != "Unnamed"\
               and strHeader[:16] != "OccurrenceStatus":
                intFiles += 1
        tblTaxonomyColumn = tblReadInput.iloc[:,intFiles+intColumnLength]
        for strRow in tblTaxonomyColumn:
            strTaxonLine = str(strRow).split("/")
            strTaxonLine = [strName.strip(" ") for strName in strTaxonLine]
            lstSpecies.append(strTaxonLine[-1])
    elif strFormat == "lca":
        lstOtuNames = tblReadInput.ix[:,0]
        intFiles = 0
        for strHeader in list(tblReadInput):
            if strHeader[:1] != "#" and strHeader[:7] != "Unnamed"\
               and strHeader[:16] != "OccurrenceStatus":
                intFiles += 1
        lstSpecies = tblReadInput.iloc[:,intFiles+3]
    elif strFormat == "blast":
        lstSpecies = []
        for strRow in tblReadInput["Taxonomy"]:
            strTaxonLine = str(strRow).split("/")
            strTaxonLine = [strName.strip(" ") for strName in strTaxonLine]
            lstSpecies.append(strTaxonLine[-1])
    else:
        pass
    if strProcess == "occurrences":
        getOccurrenceStatus(tblReadInput, flOutput, lstSpecies)
    elif strProcess == "pictures":
        getPicture(tblReadInput, flOutput, lstSpecies)
    else:
        pass

# The argvs function.
def parseArgvs():
    parser = argparse.ArgumentParser(description="Use a python script to\
                                                  utilize the Naturalis, BOLD\
                                                  and ALA api's to collect\
                                                  meta data.")
    parser.add_argument("-v", action="version", version="%(prog)s [0.1.0]")
    parser.add_argument("-i", action="store", dest="fisInput",
                        help="The location of the input file(s)")
    parser.add_argument("-o", action="store", dest="fosOutput",
                        help="The location of the output file(s)")
    parser.add_argument("-p", action="store", dest="disProcess",
                        help="The metadata process type [occurrences/pictures]")
    parser.add_argument("-f", action="store", dest="disFormat",
                        help="The format of the input file(s) [otu_old/otu_new/lca/accepted/blast]")
    argvs = parser.parse_args()
    return argvs

# The main function.
def main():
    argvs = parseArgvs()
    getNameColumn(argvs.fisInput, argvs.fosOutput, argvs.disProcess,
                  argvs.disFormat)

if __name__ == "__main__":
    main()

# Additional information:
# =======================
#
# Sample names can not start with a "#".
# All columns in a OTU table should have a header starting with "#".