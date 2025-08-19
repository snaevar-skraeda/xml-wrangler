#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""\
GUI tool for quickly editing XML

Usage: python3 xml_wrangler.py
"""

__author__ = "Snævar Þór Guðmundsson"
__copyright__ = "Creative Commons - Attribution 4.0 International - https://creativecommons.org/licenses/by/4.0/"
__version__ = "0.2"
__email__ = "snaevar@sjukraskra.is"
__status__ = "Test version"

import tkinter as tk
from tkinter import filedialog
import os
import re
from datetime import datetime

class xmlfile:
    filename = ''
    export_filename = ''
    quicksave = False

xml = xmlfile()

#----------------------------------------------------------------------------------------------------------------
# Function Definitions (XML Operations)
#----------------------------------------------------------------------------------------------------------------

#---------------------------------------
# Textbox string to list
#---------------------------------------

def convert_textbox_string_to_list(textbox_string):
    textbox_list = textbox_string.split('\n')
    # Restore newline character at end of line
    textboxlist_with_newline = []
    for line in textbox_list:
        textboxlist_with_newline.append(line+"\n")
    # TODO: Using indexing to fix newline issue. Locate source of issue, prevent get/insert functions from appending newline char to last line
    return textboxlist_with_newline
#    return textboxlist_with_newline[:-1]

#---------------------------------------
# Terminate newline check
#---------------------------------------

# Removes final line from list if it happens to be an empty line
def terminating_newline_check(xml_list):
# TODO: Debut issue with last line disappearing
#    if xml_list[-1] == "\n":
#        return xml_list[:-1]
    return xml_list

#---------------------------------------
# Textbox contents to list
#---------------------------------------

# Converts textbox contents from string to list
def textbox_contents_to_list():
    xml_text = get_textbox_contents()
    xml_list = convert_textbox_string_to_list(xml_text)
    return xml_list

#---------------------------------------
# Remove selfclosing tags
#---------------------------------------

def xml_replace_selfclosing_tags():
    if xml.filename:
        xml_list = textbox_contents_to_list()
        contents = []
        for line in xml_list:
            if ("/>" in line):
                start = line.find("<")
                end = line.find("/>")
                tag_name = line[start+1:end].strip()
                closingtags = f"{line[:start]}<{tag_name}></{tag_name}>\n"
                contents.append(closingtags)
            else:
                contents.append(line)

        update_textbox(contents)

        if(xml.quicksave == True):
            export_xml_file(False)

#---------------------------------------
# Remove text between files
#---------------------------------------

def xml_remove_text_between_lines():
    if xml.filename:
        xml_list = textbox_contents_to_list()
        contents = []
        for line in xml_list:
            res = re.search(">.*</", line)
            if (res != None):
                span = res.span()
                line_with_no_text = f"{line[:span[0]+1]}{line[span[1]-2:]}"
                contents.append(line_with_no_text)
            else:
                contents.append(line)

        update_textbox(contents)

        if(xml.quicksave == True):
            export_xml_file(False)

#---------------------------------------
# Perform both operations
#---------------------------------------

def xml_both():
    if xml.filename:
        xml_remove_text_between_lines()
        xml_replace_selfclosing_tags()

#---------------------------------------
# Add translation subtags
#---------------------------------------

def xml_add_translation_subtags():
    if xml.filename:
        xml_list = textbox_contents_to_list()
        contents = []
        for line in xml_list:
            begin = line.find('>')
            if(begin != -1):
                contents.append(f"{line[:begin]} t=(){line[begin:]}")
            else:
                contents.append(line)

        update_textbox(contents)

        if(xml.quicksave == True):
            export_xml_file(False)

#---------------------------------------
# Remove translation subtags
#---------------------------------------

def xml_remove_translation_subtags():
    if xml.filename:
        xml_list = textbox_contents_to_list()
        contents = []
        for line in xml_list:
            begin = line.find(' t=(')
            if(begin != -1):
                end = line.find(')')
                contents.append(f"{line[:begin]}{line[end+1:]}")
            else:
                contents.append(line)

        update_textbox(contents)

        if(xml.quicksave == True):
            export_xml_file(False)

#---------------------------------------
# Replace Brackets
#---------------------------------------

def xml_replace_brackets():
    if xml.filename:
        xml_list = textbox_contents_to_list()
        
        contents = []
        for line in xml_list:
            contents.append(line.replace("<", "&lt;"))

        contents2 = []
        for line in contents:
            contents2.append(line.replace(">", "&gt;"))

        update_textbox(contents2)

        if(xml.quicksave == True):
            export_xml_file(False)

#---------------------------------------
# XML to One Line
#---------------------------------------

def xml_one_line():
    xml_list = textbox_contents_to_list()
    one_line = ''
    for line in xml_list:
        print(one_line)
#        print(line.strip())
        one_line = one_line + line.strip()
#    print(xml_list)
#    print()
#    print(type(xml_list))
#    print(len(xml_list))

    # Only inserting a single line
    clear_textbox()
    textboxXML.insert(tk.END, one_line)


def xml_CDATA():
    xml_list = textbox_contents_to_list()
    one_line = ''
    for line in xml_list:
        one_line = one_line + line.strip()

    one_line = f"<![CDATA[{one_line}]]>"

    # Only inserting a single line
    clear_textbox()
    textboxXML.insert(tk.END, one_line)

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
# Read XML file
#---------------------------------------

def read_xml_file(filename):
    with open(file=filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()
    return(lines)

#---------------------------------------
# Export XML file
#---------------------------------------

def export_xml_file(custom_name):
    if(custom_name == False):
        xml.export_filename = generate_export_filename(xml.filename)

    xml_list = textbox_contents_to_list()
    with open(xml.export_filename, "w") as output:
        for line in xml_list:
            output.write(str(line))
    update_export_filename_display(xml.export_filename)

#---------------------------------------
# Textbox Functions
#---------------------------------------

def clear_textbox():
    textboxXML.delete("1.0", "end")

def update_textbox(contents):
    clear_textbox()
    for line in contents:
        textboxXML.insert(tk.END, line)

def get_textbox_contents():
    return textboxXML.get('1.0', 'end-1c')

#----------------------------------------------------------------------------------------------------------------
# Function Definitions (Buttons)
#----------------------------------------------------------------------------------------------------------------

def enable_buttons():
    buttonReplace.config(state=tk.NORMAL)
    buttonRemove.config(state=tk.NORMAL)
    buttonBoth.config(state=tk.NORMAL)
    buttonAddTranslations.config(state=tk.NORMAL)
    buttonRemoveTranslations.config(state=tk.NORMAL)
    buttonReplaceBrackets.config(state=tk.NORMAL)
    buttonOneLineXML.config(state=tk.NORMAL)
    buttonCDATA.config(state=tk.NORMAL)
    buttonSave.config(state=tk.NORMAL)
    buttonSaveAs.config(state=tk.NORMAL)

def open_file():
    xml.filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All Files", "*.*")])

    if xml.filename:
        filename_short = get_short_filename(xml.filename)
        labelCurrentFile.config(text=f"File selected: {filename_short}")

        contents = read_xml_file(xml.filename)
        clear_textbox()
        update_textbox(contents)
        enable_buttons()

def get_short_filename(filename_with_path):
    filename_short = os.path.split(filename_with_path)[1]
    return filename_short

def save():
    custom_filename = False
    export_xml_file(custom_filename)

def save_as():
    savefile = filedialog.asksaveasfilename(defaultextension=".xml")
    if savefile:
        xml.export_filename = savefile
        custom_filename = True
        export_xml_file(custom_filename)

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
# GUI Settings
#----------------------------------------------------------------------------------------------------------------

# Root Window Settings
window_height = 720
window_width = 690
root = tk.Tk(className="electronic sheets XML wrangler")
root.geometry(f"{window_height}x{window_width}")

# XML Cleanup Widgets
labelXMLCleanup = tk.Label(root, font='Arial 10 bold', height=2, text="XML Cleanup")
buttonOpenFile = tk.Button(root, width=26, text="Open file", command=open_file)
buttonReplace = tk.Button(root, state=tk.DISABLED, width=26, text="Replace self-closing tags", command=xml_replace_selfclosing_tags)
buttonRemove = tk.Button(root, state=tk.DISABLED, width=26, text="Remove text between tags", command=xml_remove_text_between_lines)
buttonBoth = tk.Button(root, state=tk.DISABLED, width=26, text="Perform both operations", command=xml_both)

# System Function Widgets
buttonExit = tk.Button(root, width=26, text="Exit", command=exit_program)

# Translation Subtag Widgets
labelTranslation = tk.Label(root, font='Arial 10 bold', height=2, text="Translation sub-tags")
buttonAddTranslations = tk.Button(root, state=tk.DISABLED, width=26, text="Add translation sub-tags", command=xml_add_translation_subtags)
buttonRemoveTranslations = tk.Button(root, state=tk.DISABLED, width=26, text="Remove translation sub-tags", command=xml_remove_translation_subtags)

# File Saving Widgets
labelSaveFile = tk.Label(root, font='Arial 10 bold', height=2, text="Save File")
toggleQuicksave = tk.Button(text="Quicksave Disabled", width=26, relief="raised", command=toggle_quicksave)
buttonSave = tk.Button(root, state=tk.DISABLED, width=26, text="Save", command=save)
buttonSaveAs = tk.Button(root, state=tk.DISABLED, width=26, text="Save As...", command=save_as)

# Information Display Widgets
labelCurrentFile = tk.Label(root, font='Courier 10', height=2, text="")
labelExportedFile = tk.Label(root, font='Courier 10', height=2, text="")
textboxXML = tk.Text(root, width=88, padx=2)
textboxXML.insert(tk.END, "XML will be displayed here.\n")

# XML Mimimize Widgets
labelXMLMinimize = tk.Label(root, font='Arial 10 bold', height=2, text="Minimize XML")
buttonReplaceBrackets = tk.Button(root, state=tk.DISABLED, width=26, text="Replace Brackets", command=xml_replace_brackets)
buttonOneLineXML = tk.Button(root, state=tk.DISABLED, width=26, text="One Line", command=xml_one_line)
buttonCDATA = tk.Button(root, state=tk.DISABLED, width=26, text="CDATA", command=xml_CDATA)

#--------------------------------------------------------------------------
# Add widgets to Tkinter grid
#--------------------------------------------------------------------------

# XML Cleanup Grid
labelXMLCleanup.grid(row=0, column=0, padx=2)
buttonOpenFile.grid(row=1, column=0, padx=2)
buttonReplace.grid(row=2, column=0, padx=2)
buttonRemove.grid(row=3, column=0, padx=2)
buttonBoth.grid(row=4, column=0, padx=2)

# Translation Subtag Grid
labelTranslation.grid(row=0, column=1, padx=2)
buttonAddTranslations.grid(row=1, column=1, padx=2)
buttonRemoveTranslations.grid(row=2, column=1, padx=2)

# File Saving Grid
labelSaveFile.grid(row=0, column=2, padx=2)
toggleQuicksave.grid(row=1, column=2, padx=2)
buttonSave.grid(row=2, column=2, padx=2)
buttonSaveAs.grid(row=3, column=2, padx=2)

# Exit button Grid
buttonExit.grid(row=5, column=0, padx=2)

# Minimize XML Grid
labelXMLMinimize.grid(row=3, column=1, padx=2)
buttonReplaceBrackets.grid(row=4, column=1, padx=2)
buttonOneLineXML.grid(row=5, column=1, padx=2)
buttonCDATA.grid(row=5, column=2, padx=2)

# Information Display Grid
labelCurrentFile.grid(row=6, column=0, padx=2, columnspan=3)
labelExportedFile.grid(row=7, column=0, padx=2, columnspan=3)
textboxXML.grid(row=8, column=0, columnspan=10)

root.mainloop()