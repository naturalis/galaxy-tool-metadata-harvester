#!/usr/bin/env bash

# Copyright (C) 2018 Jasper Boom

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License version 3 as
# published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Prequisites:
# - Conda environment python >= 3.7
# - conda install -c anaconda pandas

# The getFormatFlow function.
# This function creates a temporary storage directory in the output directory.
# It then calls the getMetaData.py script with the correct input values.
# After the script is finished, output is send to the expected location and
# the temporary storage directory is deleted.

SCRIPTDIR=$(dirname "$(readlink -f "$0")")

getFormatFlow() {
    strDirectory_temp=$(mktemp -d /media/GalaxyData/database/files/XXXXXX)
    strDirectory=${fosOutput::-4}
	echo "Output Directory from sh:"
	echo "$strDirectory_temp"
#    mkdir -p "${strDirectory}_temp"
    if [ "${disProcess}" = "occurrences" ]
    then
        python $SCRIPTDIR"/getMetaData.py" -i ${fisInput} -o ${strDirectory_temp}/ \
                       -p ${disProcess} -f ${disFormat}
        cat ${strDirectory_temp}/flNewOutput.tabular > ${fosOutput}
        rm -rf ${strDirectory_temp}
    elif [ "${disProcess}" = "pictures" ]
    then
        python $SCRIPTDIR"/getMetaData.py" -i ${fisInput} -o ${strDirectory_temp}/ \
                       -p ${disProcess} -f ${disFormat}
        zip -jqr ${strDirectory_temp}/flImageZip.zip ${strDirectory_temp}/*
        cat ${strDirectory_temp}/flImageZip.zip > ${fosOutput}
        rm -rf ${strDirectory_temp}
    fi
}

# The main function.
main() {
    getFormatFlow
}

# The getopts function.
while getopts ":i:o:p:f:vh" opt; do
    case ${opt} in
        i)
            fisInput=${OPTARG}
            ;;
        o)
            fosOutput=${OPTARG}
            ;;
        p)
            disProcess=${OPTARG}
            ;;
        f)
            disFormat=${OPTARG}
            ;;
        v)
            echo ""
            echo "runMetaData.sh [0.1.0]"
            echo ""

            exit
            ;;
        h)
            echo ""
            echo "Usage: runMetaData.sh [-h] [-v] [-i INPUT] [-o OUTPUT]"
            echo "                      [-p PROCESS] [-f FORMAT]"
            echo ""
            echo "Optional arguments:"
            echo " -h                    Show this help page and exit"
            echo " -v                    Show the software's version number"
            echo "                       and exit"
            echo " -i                    The location of the input file(s)"
            echo " -o                    The location of the output file(s)"
            echo " -p                    The metadata process"
            echo "                       type [occurrences/pictures]"
            echo " -f                    The format of the input"
            echo "                       file(s) [otu_old/otu_new/lca/accepted/blast]"
            echo ""
            echo "The MetaData tool will utilize the Naturalis, BOLD and ALA"
            echo "api's to collect meta data such as occurrence status and"
            echo "images based on BLAST identifications or accepted taxonomic"
            echo "names."
            echo ""
            echo "Definitions for all occurrence status codes can be found"
            echo "on this page:"
            echo "https://www.nederlandsesoorten.nl/content/occurrence-status"
            echo ""
            echo "Sample names can not start with a '#'."
            echo "All columns in a OTU table should have a header starting"
            echo "with '#'."
            echo ""
            echo "Source(s):"
            echo " - Naturalis website at"
            echo "   http://docs.biodiversitydata.nl/en/latest/introduction/"
            echo " - Nederlands Soortenregister website at"
            echo "   https://www.nederlandsesoorten.nl/"
            echo " - Ratnasingham S, Hebert PDN, BOLD: The Barcode of Life" 
            echo "   Data System."
            echo "   Molecular Ecology Notes. 2007; 7(3)."
            echo "   doi: 10.1111/j.1471-8286.2007.01678.x"
            echo "   http://www.boldsystems.org/index.php/resources/api"
            echo " - Atlas of Living Australia website at"
            echo "   https://api.ala.org.au/"
            echo ""

            exit
            ;;
        \?)
            echo ""
            echo "You've entered an invalid option: -${OPTARG}."
            echo "Please use the -h option for correct formatting information."
            echo ""

            exit
            ;;
        :)
            echo ""
            echo "You've entered an invalid option: -${OPTARG}."
            echo "Please use the -h option for correct formatting information."
            echo ""

            exit
            ;;
    esac
done

main

# Additional information:
# =======================
#
# Sample names can not start with a "#".
# All columns in a OTU table should have a header starting with "#".
