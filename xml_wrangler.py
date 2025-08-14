#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
GUI tool for XML cleanup utilities

Usage: python3 xmlfix_gui.py
"""

__author__ = "Snævar Þór Guðmundsson"
__copyright__ = "Creative Commons - Attribution 4.0 International - https://creativecommons.org/licenses/by/4.0/"
__version__ = "0.1"
__email__ = "snaevar@sjukraskra.is"
__status__ = "Test version"

import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re
from datetime import datetime

class xmlfile:
    filename = ''
    export_filename = ''
    contents = []
    quicksave = True

xml = xmlfile()

#----------------------------------------------------------------------------------------------------------------
# Function Definitions (XML Operations)
#----------------------------------------------------------------------------------------------------------------

#---------------------------------------
# Generate export filename
#---------------------------------------

def generate_export_filename(filename):
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H.%M.%S")
    export_filename = f"{filename.split(".")[0]}_{date_time}.{filename.split(".")[1]}"
    return export_filename

#---------------------------------------
# Update export filename display
#---------------------------------------

def update_export_filename_display(export_filename):
    short_export_filename = get_short_filename(export_filename)
    labelExportedFile.config(text=f"File exported to: {short_export_filename}")

#---------------------------------------
# Remove selfclosing tags
#---------------------------------------

def remove_selfclosing_tags():
    xml_list = xml.contents

    xml.contents = []
    for line in xml_list:
        if ("/>" in line):
            start = line.find("<")
            end = line.find("/>")
            tag_name = line[start+1:end].strip()
            closingtags = f"{line[:start]}<{tag_name}></{tag_name}>\n"
            xml.contents.append(closingtags)
        else:
            xml.contents.append(line)

    if(xml.quicksave == True):
        export_xml_file()

#---------------------------------------
# Remove text between files
#---------------------------------------

def remove_text_between_files():
    xml_list = xml.contents

    xml.contents = []
    for line in xml_list:
        res = re.search(">.*</", line)
        if (res != None):
            span = res.span()
            line_with_no_text = f"{line[:span[0]+1]}{line[span[1]-2:]}"
            xml.contents.append(line_with_no_text)
        else:
            xml.contents.append(line)

    if(xml.quicksave == True):
        export_xml_file()

#---------------------------------------
# Add translation subtags
#---------------------------------------

def add_translation_subtags():
    xml_list = xml.contents

    xml.contents = []
    for line in xml_list:
        begin = line.find('>')
        if(begin != -1):
            xml.contents.append(f"{line[:begin]} t=(){line[begin:]}")
        else:
            xml.contents.append(line)

    if(xml.quicksave == True):
        export_xml_file()

#---------------------------------------
# Remove translation subtags
#---------------------------------------

def remove_translation_subtags():
    xml_list = xml.contents

    xml.contents = []
    for line in xml_list:
        begin = line.find(' t=(')
        if(begin != -1):
            end = line.find(')')
            xml.contents.append(f"{line[:begin]}{line[end+1:]}")
        else:
            xml.contents.append(line)

    if(xml.quicksave == True):
        export_xml_file()

#---------------------------------------
# Read XML file
#---------------------------------------

def read_xml_file(filename):
    with open(file=filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    return(lines)

#---------------------------------------
# Export XML file
#---------------------------------------

def export_xml_file():
    xml.export_filename = generate_export_filename(xml.filename)
    with open(xml.export_filename, "w") as output:
        for line in xml.contents:
            output.write(str(line))
    update_export_filename_display(xml.export_filename)

#---------------------------------------
# Update text box
#---------------------------------------

def update_text_box_contents():
    textboxXML.delete("1.0", "end")
    for line in xml.contents:
        textboxXML.insert(tk.END, line)

#----------------------------------------------------------------------------------------------------------------
# Function Definitions (Buttons)
#----------------------------------------------------------------------------------------------------------------

def enable_buttons():
    buttonReplace.config(state=tk.NORMAL)
    buttonRemove.config(state=tk.NORMAL)
    buttonBoth.config(state=tk.NORMAL)
    buttonAddTranslations.config(state=tk.NORMAL)
    buttonRemoveTranslations.config(state=tk.NORMAL)
    buttonSave.config(state=tk.NORMAL)
    buttonSaveAs.config(state=tk.NORMAL)

def open_file():
    # TODO: Permit user to search for other file types, simply default to XML without locking out other types
    xml.filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])

    if xml.filename:
        xml.contents = read_xml_file(xml.filename)
        filename_short = get_short_filename(xml.filename)
        labelCurrentFile.config(text=f"File selected: {filename_short}")
        enable_buttons()
        update_text_box_contents()

def get_short_filename(filename_with_path):
    filename_short = os.path.split(filename_with_path)[1]
    return filename_short

def xml_replace():
    if xml.filename:
        remove_selfclosing_tags()
        update_text_box_contents()

def xml_remove():
    if xml.filename:
        remove_text_between_files()
        update_text_box_contents()

def xml_both():
    if xml.filename:
        remove_text_between_files()
        remove_selfclosing_tags()
        update_text_box_contents()

def xml_add_subtags():
    if xml.filename:
        add_translation_subtags()
        update_text_box_contents()

def xml_remove_subtags():
    if xml.filename:
        remove_translation_subtags()
        update_text_box_contents()

def save():
    xml.contents = textboxXML.get('1.0', 'end-1c')
    export_xml_file()

def save_as():
    # Prompts user for file name, then calls save function
    xml.filename = filedialog.asksaveasfilename(defaultextension=".xml")
    print("Save As... button pressed")
    print(xml.export_filename)
    save()

def toggle_quicksave():
    if toggleQuicksave.config('relief')[-1] == 'sunken':
        toggleQuicksave.config(relief="raised", text="Quicksave Disabled")
        xml.quicksave = False
    else:
        toggleQuicksave.config(relief="sunken", text="Quicksave Enabled")
        xml.quicksave = True

def exit_program():
    root.destroy() #exit program loop

#----------------------------------------------------------------------------------------------------------------
# Main Program (Tkinter GUI)
#----------------------------------------------------------------------------------------------------------------

root = tk.Tk(className="electronic sheets XML wrangler")
root.geometry("720x690")

labelXMLCleanup = tk.Label(root, font='Arial 10 bold', height=2, text="XML Cleanup")
buttonOpenFile = tk.Button(root, width=26, text="Open file", command=open_file)
buttonReplace = tk.Button(root, state=tk.DISABLED, width=26, text="Replace self-closing tags", command=xml_replace)
buttonRemove = tk.Button(root, state=tk.DISABLED, width=26, text="Remove text between tags", command=xml_remove)
buttonBoth = tk.Button(root, state=tk.DISABLED, width=26, text="Perform both operations", command=xml_both)

buttonExit = tk.Button(root, width=26, text="Exit", command=exit_program)

labelTranslation = tk.Label(root, font='Arial 10 bold', height=2, text="Translation sub-tags")
buttonAddTranslations = tk.Button(root, state=tk.DISABLED, width=26, text="Add translation sub-tags", command=xml_add_subtags)
buttonRemoveTranslations = tk.Button(root, state=tk.DISABLED, width=26, text="Remove translation sub-tags", command=xml_remove_subtags)

labelSaveFile = tk.Label(root, font='Arial 10 bold', height=2, text="Save File")
toggleQuicksave = tk.Button(text="Quicksave Enabled", width=26, relief="sunken", command=toggle_quicksave)
buttonSave = tk.Button(root, state=tk.DISABLED, width=26, text="Save", command=save)
buttonSaveAs = tk.Button(root, state=tk.DISABLED, width=26, text="Save As...", command=save_as)

labelCurrentFile = tk.Label(root, font='Courier 10', height=2, text="")
labelExportedFile = tk.Label(root, font='Courier 10', height=2, text="")
textboxXML = tk.Text(root, width=88, padx=2)
textboxXML.insert(tk.END, "XML will be displayed here.\n")

#--------------------------------
# Add widgets to Tkinter grid
#--------------------------------

# XML Cleanup
labelXMLCleanup.grid(row=0, column=0, padx=2)
buttonOpenFile.grid(row=1, column=0, padx=2)
buttonReplace.grid(row=2, column=0, padx=2)
buttonRemove.grid(row=3, column=0, padx=2)
buttonBoth.grid(row=4, column=0, padx=2)

# Translation subtags
labelTranslation.grid(row=0, column=1, padx=2)
buttonAddTranslations.grid(row=1, column=1, padx=2)
buttonRemoveTranslations.grid(row=2, column=1, padx=2)

# Save File
labelSaveFile.grid(row=0, column=2, padx=2)
toggleQuicksave.grid(row=1, column=2, padx=2)
buttonSave.grid(row=2, column=2, padx=2)
buttonSaveAs.grid(row=3, column=2, padx=2)

# Exit button
buttonExit.grid(row=5, column=0, padx=2)

# Current file
labelCurrentFile.grid(row=6, column=0, padx=2, columnspan=3)

# Exported file name
labelExportedFile.grid(row=7, column=0, padx=2, columnspan=3)

# Text box area
textboxXML.grid(row=8, column=0, columnspan=10)

root.mainloop()