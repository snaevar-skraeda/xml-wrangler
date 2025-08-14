#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
Imports .xml file, replaces self-closing tags with standard matching tags.

Usage: python3 replace_selfclosing_tags.py <xmlfile.xml>
"""

__author__ = "Snævar Þór Guðmundsson"
__copyright__ = "Creative Commons - Attribution 4.0 International - https://creativecommons.org/licenses/by/4.0/"
__version__ = "1.0"
__email__ = "snaevar@sjukraskra.is"
__status__ = "Test version"

#---------------------------------------------------------------------------------------------------------------------
# File Import
#---------------------------------------------------------------------------------------------------------------------

import os
import sys
from datetime import datetime
#os.chdir(f"{os.path.dirname(__file__)}/") #Force Python to use script's directory as working directory.

if (len(sys.argv)< 2):
    print("No file provided. Exiting...")
    sys.exit()
if (len(sys.argv) > 2):
    print("Too many arguments provided. Exiting...")
    sys.exit()
if (os.path.isfile(sys.argv[1]) == False):
    print("Invalid path to file. Exiting...")
    sys.exit()

now = datetime.now()
date_time = now.strftime("%m-%d-%Y_%H.%M.%S")
import_filename = sys.argv[1]
export_filename = f"{import_filename.split(".")[0]}_noselfclosingtags_{date_time}.{import_filename.split(".")[1]}"

print(f"Converting file: {os.path.dirname(__file__)}/{sys.argv[1]}")

#---------------------------------------------------------------------------------------------------------------------
# Main Program
#---------------------------------------------------------------------------------------------------------------------

with open(import_filename, "r") as file:
    lines = file.readlines()

no_selfclosing_tags = []
for line in lines:
    if ("/>" in line):
        start = line.find("<")
        end = line.find("/>")
        tag_name = line[start+1:end].strip()
        closingtags = f"{line[:start]}<{tag_name}></{tag_name}>\n"
        no_selfclosing_tags.append(closingtags)
    else:
        no_selfclosing_tags.append(line)

with open(export_filename, "w") as output:
    for line in no_selfclosing_tags:
        output.write(str(line))