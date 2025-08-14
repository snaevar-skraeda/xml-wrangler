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

xml = xmlfile()

def generate_export_filename(filename):
    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H.%M.%S")
    return f"{filename.split(".")[0]}_noselfclosingtags_{date_time}.{filename.split(".")[1]}"

def remove_selfclosing_tags(filename):
    export_filename = generate_export_filename(filename)
    print(f"Converting file: {os.path.dirname(__file__)}/{filename}")

    with open(filename, "r") as file:
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

    # update which file is being referred to
    xml.filename = export_filename
    update_text_box_contents()

def remove_text_between_files(filename):
    export_filename = generate_export_filename(filename)
    print(f"Converting file: {os.path.dirname(__file__)}/{filename}")

    with open(filename, "r") as file:
        lines = file.readlines()

    no_text = []
    for line in lines:
        res = re.search(">.*</", line)
    #    res = re.search("\>.*\<\/", line)
        if (res != None):
            span = res.span()
            line_with_no_text = f"{line[:span[0]+1]}{line[span[1]-2:]}"
            no_text.append(line_with_no_text)
        else:
            no_text.append(line)

    with open(export_filename, "w") as output:
        for line in no_text:
            output.write(str(line))
    
    # update which file is being referred to
    xml.filename = export_filename
    update_text_box_contents()

def remove_translations(filename):
    export_filename = generate_export_filename(filename)
    print(f"Converting file: {os.path.dirname(__file__)}/{filename}")

    with open(filename, "r") as file:
        lines = file.readlines()

    no_translations = []
    for line in lines:
        begin = line.find(' t=(')
        if(begin != -1):
            end = line.find(')')
            no_translations.append(f"{line[:begin]}{line[end+1:]}")
        else:
            no_translations.append(line)

    with open(export_filename, "w") as output:
        for line in no_translations:
            output.write(str(line))

    # update which file is being referred to
    xml.filename = export_filename
    update_text_box_contents()

def update_text_box_contents():
    text_box.delete("1.0", "end")
    with open(xml.filename, "r") as file:
        lines = file.readlines()
    for line in lines:
        text_box.insert(tk.END, line)

def select_file():
    xml.filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    #filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
#    print(xml.filename)
# TODO: Add button enable/disable feature here
# button.config(state=tk.E)
# button.config(state=tk.DISABLED)
    if xml.filename:
        update_text_box_contents()
        # buttonReplace.config(state=tk.ACTIVE)
        # buttonRemove.config(state=tk.ACTIVE)
        # buttonBoth.config(state=tk.ACTIVE)
        # buttonRemoveTranslations.config(state=tk.ACTIVE)

        buttonReplace.config(state=tk.NORMAL)
        buttonRemove.config(state=tk.NORMAL)
        buttonBoth.config(state=tk.NORMAL)
        buttonRemoveTranslations.config(state=tk.NORMAL)

def xml_replace():
#    filename = filedialog.askopenfilename()
    if xml.filename:
        remove_selfclosing_tags(xml.filename)
        update_text_box_contents()
#        exit_program()
#        root.destroy() #exit program loop

def xml_remove():
#    filename = filedialog.askopenfilename()
    if xml.filename:
        remove_text_between_files(xml.filename)
        update_text_box_contents()
        #exit_program()
#        root.destroy() #exit program loop

def xml_both():
#    filename = filedialog.askopenfilename()
    if xml.filename:
        remove_text_between_files(xml.filename)
        remove_selfclosing_tags(xml.filename)
        update_text_box_contents()
#        exit_program()

def xml_remove_subtags():
    if xml.filename:
        remove_translations(xml.filename)
        update_text_box_contents()

def exit_program():
    root.destroy() #exit program loop


root = tk.Tk(className="Electronic sheets XML tool")
root.geometry("500x500")

label = tk.Label(root, text="XML Cleanup Utilities")
label.pack()

#Open file button
buttonSelectFile = tk.Button(root, text="Open file", command=select_file)
buttonSelectFile.pack()

#Replace self-closing tags button
buttonReplace = tk.Button(root, text="Replace self-closing tags", command=xml_replace)
buttonReplace.config(state=tk.DISABLED)
buttonReplace.pack()

#Remove text button
buttonRemove = tk.Button(root, text="Remove text between tags", command=xml_remove)
buttonRemove.config(state=tk.DISABLED)
buttonRemove.pack()

#Replace self-closing tags and remove text
buttonBoth = tk.Button(root, text="Perform both operations", command=xml_both)
buttonBoth.config(state=tk.DISABLED)
buttonBoth.pack()

label = tk.Label(root, text="Translation sub-tags")
label.pack()

#Remove translation sub-tags
buttonRemoveTranslations = tk.Button(root, text="Remove translation sub-tags", command=xml_remove_subtags)
buttonRemoveTranslations.config(state=tk.DISABLED)
buttonRemoveTranslations.pack()

#Quit program
buttonExit = tk.Button(root, text="Exit", command=exit_program)
buttonExit.pack()

text_box = tk.Text(root, height=100, width=100)
text_box.pack(side='right')
text_box.insert(tk.END, "XML will be displayed here.\n")

root.mainloop()