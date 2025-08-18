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
#    contents = []
    quicksave = False

    textboxcontents = '' #DEBUG GLOBAL VARIABLE

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
# Textbox string to list
#---------------------------------------

def convert_textbox_string_to_list(textbox_string):
    textbox_list = textbox_string.split('\n')
    # Restore newline character at end of line
    textboxlist_with_newline = []
    for line in textbox_list:
        textboxlist_with_newline.append(line+"\n")

    print(textboxlist_with_newline)
    # Using indexing to fix newline issue.
    # TODO: Locate source of issue, prevent get/insert functions from appending newline char to last line
    return textboxlist_with_newline[:-1]

# Removes final line from list if it happens to be an empty line
def terminating_newline_check(xml_list):
    if xml_list[-1] == "\n":
        return xml_list[:-1]
    return xml_list

def textbox_contents_to_list():
    xml_text = get_textbox_contents()
    xml_list = convert_textbox_string_to_list(xml_text)
    return xml_list

#---------------------------------------
# Remove selfclosing tags
#---------------------------------------

def remove_selfclosing_tags():
    xml_list = textbox_contents_to_list()
    # xml_list = get_textbox_contents()
    # xml_list = convert_textbox_string_to_list(xml_list)
#    xml_list = terminating_newline_check(xml_list)

    contents = []
    for line in xml_list:
        if ("/>" in line):
            start = line.find("<")
            end = line.find("/>")
            tag_name = line[start+1:end].strip()
            closingtags = f"{line[:start]}<{tag_name}></{tag_name}>\n"
            contents.append(closingtags)
            # xml.contents.append(closingtags)
        else:
            contents.append(line)
            # xml.contents.append(line)

    update_textbox(contents)

    if(xml.quicksave == True):
        export_xml_file(False)

#---------------------------------------
# Remove text between files
#---------------------------------------

def remove_text_between_files():
    # xml_list = xml.contents
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
# Add translation subtags
#---------------------------------------

def add_translation_subtags():
    # xml_list = xml.contents
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

def remove_translation_subtags():
    # xml_list = xml.contents
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
# Read XML file
#---------------------------------------

def read_xml_file(filename):
    with open(file=filename, mode="r", encoding="utf-8") as file:
        lines = file.readlines()

    # print("read xml file")
    # print(lines)
    # print(type(lines))
    return(lines)

#---------------------------------------
# Export XML file
#---------------------------------------

def export_xml_file(custom_name):
    if(custom_name == False):
        xml.export_filename = generate_export_filename(xml.filename)
    with open(xml.export_filename, "w") as output:
        for line in xml.contents:
            output.write(str(line))
    update_export_filename_display(xml.export_filename)

#---------------------------------------
# Textbox
#---------------------------------------

def clear_textbox():
    textboxXML.delete("1.0", "end")

def update_textbox(contents):
    # print("update textbox reached")
    # print(contents)
    clear_textbox()
    for line in contents:
        textboxXML.insert(tk.END, line)

def get_textbox_contents():
    #DEBUG
#    res = textboxXML.get('1.0', 'end-1c')
    # res = textboxXML.get('1.0', tk.END).splitlines()
    # res = textboxXML.get("1.0", "end-1c")
    # res = textboxXML.get("1.0", "end - 1 lines")
    # print("read textbox contents")
    # print(res)
    # print(type(res))
    #end DEBUG

    # txt = textboxXML.get('1.0', tk.END).splitlines()
    # Fixes newline issue
    # for line in txt:
    #     txt.append(f"{line}\n")

    # return textboxXML.get("1.0", "end - 1 lines")
    # return textboxXML.get('1.0', tk.END).splitlines()
#    return textboxXML.get('1.0', tk.END).splitlines()
# working better, but need to add newline char to everything
    return textboxXML.get('1.0', 'end-1c')
    # return textboxXML.get('1.0', 'end')

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
    xml.filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All Files", "*.*")])

    if xml.filename:
#        xml.contents = read_xml_file(xml.filename)
        filename_short = get_short_filename(xml.filename)
        labelCurrentFile.config(text=f"File selected: {filename_short}")
 
#        textboxXML.delete("1.0", "end")

#        for line in xml.contents:
#        xml.contents = read_xml_file(xml.filename)
        # for line in read_xml_file(xml.filename):
        #     textboxXML.insert(tk.END, line)

        contents = read_xml_file(xml.filename)
        clear_textbox()
        update_textbox(contents)
        enable_buttons()

def get_short_filename(filename_with_path):
    filename_short = os.path.split(filename_with_path)[1]
    return filename_short

def xml_replace():
    if xml.filename:
        remove_selfclosing_tags()
#        update_text_box_contents()

def xml_remove():
    if xml.filename:
        remove_text_between_files()
#        update_text_box_contents()

def xml_both():
    if xml.filename:
        remove_text_between_files()
        remove_selfclosing_tags()
#        update_text_box_contents()

def xml_add_subtags():
    if xml.filename:
        add_translation_subtags()
#        update_text_box_contents()

def xml_remove_subtags():
    if xml.filename:
        remove_translation_subtags()
#        update_text_box_contents()

def save():
    xml.contents = textboxXML.get('1.0', 'end-1c')
    # xml.contents = textboxXML.get('1.0', 'end-1c').split()
    # Fixes issue with textbox/xml.contents type mismatch
    # xml_add_newline = []
    # for line in xml.contents:
    #     xml_add_newline.append(line+"\n")
    # xml.contents = xml_add_newline
    custom_filename = False
    export_xml_file(custom_filename)

def save_as():
    savefile = filedialog.asksaveasfilename(defaultextension=".xml")
    if savefile:
#        xml.filename = savefile
        xml.export_filename = savefile
        xml.contents = textboxXML.get('1.0', 'end-1c')
#        save()
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
buttonReplace = tk.Button(root, state=tk.DISABLED, width=26, text="Replace self-closing tags", command=xml_replace)
buttonRemove = tk.Button(root, state=tk.DISABLED, width=26, text="Remove text between tags", command=xml_remove)
buttonBoth = tk.Button(root, state=tk.DISABLED, width=26, text="Perform both operations", command=xml_both)

# System Function Widgets
buttonExit = tk.Button(root, width=26, text="Exit", command=exit_program)

# Translation Subtag Widgets
labelTranslation = tk.Label(root, font='Arial 10 bold', height=2, text="Translation sub-tags")
buttonAddTranslations = tk.Button(root, state=tk.DISABLED, width=26, text="Add translation sub-tags", command=xml_add_subtags)
buttonRemoveTranslations = tk.Button(root, state=tk.DISABLED, width=26, text="Remove translation sub-tags", command=xml_remove_subtags)

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

# Information Display Grid
labelCurrentFile.grid(row=6, column=0, padx=2, columnspan=3)
labelExportedFile.grid(row=7, column=0, padx=2, columnspan=3)
textboxXML.grid(row=8, column=0, columnspan=10)


# -----------------------------------------------------------------------------------------------
# DEBUG AREA
# -----------------------------------------------------------------------------------------------

# def showcontents():
#     print("---------------------------------------------------")
#     # print(f"xml.contents ({type(xml.contents)}):")
#     # print(xml.contents)
#     txt = textboxXML.get('1.0', 'end-1c')
#     # txt = textboxXML.get('1.0', 'end-1c').split()
#     # xml_add_newline = []
#     # for line in txt:
#     #     xml_add_newline.append(line+"\n")
#     # txt = xml_add_newline
#     print()
#     print(f"text box contents ({type(txt)}):")
#     print(txt)

# buttonShowContents = tk.Button(root, width=26, text="-Show Contents-", command=showcontents)
# buttonShowContents.grid(row=4, column=2, padx=2)
# buttonShowContents.grid(row=4, column=2, padx=2)


# def debugcleartextbox():
#     clear_textbox()

# def debugprinttextbox():
#     print("\n ---Print textbox contents--\n")
#     res = textboxXML.get("1.0", "end - 1 lines")
#     print(res)
#     print(type(res))

# def debugprinttextboxlist():
#     print("\n ---Print textbox contents--\n")
#     res = textboxXML.get("1.0", "end - 1 lines")
#     print(res)
#     print(type(res))

# def debugupdatetextbox():
#     aschars = ['c','h','a','r','s']
#     aslist = ['<chars>', '    <more chars>']
#     astext = 'chars \n more chars'
#     clear_textbox()

#     # charfix = []
#     # for line in aschars:
#     #     charfix.append(f"{line}\n")

#     # x = charfix

#     # x = aslist
#     # for line in x:
#     #     # textboxXML.insert(tk.END, line+"\n")
#     #     textboxXML.insert(tk.END, line+"\n")

#     # print("\n ---Update textbox contents as list--\n")
#     # res = textboxXML.get("1.0", "end-1c")
#     # # res = textboxXML.get("1.0", "end - 1 lines")
#     # #end-1c
#     # # x = res.split()
#     # x = res.split('\n')
#     # clear_textbox()
#     # for line in x:
#     #     textboxXML.insert(tk.END, line+"\n")


#     xml.filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml"), ("All Files", "*.*")])

#     if xml.filename:
#         contents = read_xml_file(xml.filename)

#         print(contents)
#         print(type(contents))
#         print(len(contents))

#         for line in contents:
#             textboxXML.insert(tk.END, line)
#             # textboxXML.insert(tk.END, line+"\n")

#         # clear_textbox()
#         # update_textbox(contents)
#         # enable_buttons()



# def printtextboxlist():
#     print("\n ---Print textbox contents as list--\n")
#     res = textboxXML.get("1.0", "end - 1 lines")
#     x = res.split('\n')
#     print(x)
#     print(type(x))
#     print(len(x))

# buttonClearTextbox = tk.Button(root, width=26, text="-Clear Textbox-", command=debugcleartextbox)
# buttonPrintTextbox = tk.Button(root, width=26, text="-Print Textbox-", command=debugprinttextbox)
# buttonUpdateTextbox = tk.Button(root, width=26, text="-Update Textbox-", command=debugupdatetextbox)
# buttonPrintTextboxList = tk.Button(root, width=26, text="-Print Textbox as List-", command=printtextboxlist)


# buttonClearTextbox.grid(row=5, column=2, padx=2)
# buttonPrintTextbox.grid(row=6, column=2, padx=2)
# buttonUpdateTextbox.grid(row=7, column=1, padx=2)
# buttonPrintTextboxList.grid(row=7, column=2, padx=2)


# def copyfrom():
#     xml.textboxcontents = textboxXML.get("1.0", "end-1c")
#     print("Copying textbox contents")
#     print(xml.textboxcontents)
#     print(type(xml.textboxcontents))
#     print(len(xml.textboxcontents))

#     xml.textboxcontents = xml.textboxcontents.split('\n')
#     withnewline = []
#     for line in xml.textboxcontents:
#         withnewline.append(line+"\n")

#     xml.textboxcontents = withnewline

# def pasteto():
#     clear_textbox()
#     print("Pasting textbox contents")
#     for line in xml.textboxcontents:
#         textboxXML.insert(tk.END, line)
#     print()

# buttonCopyFrom = tk.Button(root, width=26, text="-Copy From Textbox-", command=copyfrom)
# buttonPasteTo = tk.Button(root, width=26, text="-Paste To Textbox-", command=pasteto)

# buttonCopyFrom.grid(row=6, column=0, padx=2)
# buttonPasteTo.grid(row=7, column=0, padx=2)


# -----------------------------------------------------------------------------------------------
# END OF DEBUG AREA
# -----------------------------------------------------------------------------------------------

root.mainloop()