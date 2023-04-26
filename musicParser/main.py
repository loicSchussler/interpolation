import sys
import os
import json
import xml.etree.ElementTree as ET

# parse xml file
def parse_xml(xmlFilePath):
    tree = ET.parse(xmlFilePath)
    root = tree.getroot()

    # get all the elements in the tree "<part...>"
    parts = root.findall('part')
    notes_and_rhythm = []

    for part in parts:
        measures = part.findall('measure')

        # iterate through each measure in the file
        for measure in measures:
            # initialize a list to store the notes and rhythm at each measure
            current_measure_notes = []

            # get all the elements in the tree "<note...>"
            notes = measure.findall('note')

            # iterate through each note in the measure
            for note in notes:
                step = note.find('pitch/step')
                alter = note.find('pitch/alter')
                octave = note.find('pitch/octave')
                duration = note.find('duration')

                if step is not None and octave is not None and duration is not None:
                    # if there is a sharp or flat, add it to the note
                    if alter is not None:
                        note_name = step.text + alter.text
                    else:
                        note_name = step.text

                    # add the octave to the note
                    note_name += octave.text

                    # add the note and the duration to the list
                    current_measure_notes.append((note_name, int(duration.text)))

            # append the list of notes and their duration for this measure to the overall list
            notes_and_rhythm.append(current_measure_notes)

    # write the list of notes and their duration to a json file
    with open('notes_and_rhythm.json', 'w') as f:
        json.dump(notes_and_rhythm, f)

#change the extension of the file to .zip and unzip it
#unzip the file
#find the file with the extension .xml
def convert_mxl_to_xml(mxlFilePath):
    #change the extension of the file to .zip and unzip it
    zipFilePath = mxlFilePath.replace('.mxl', '.zip')
    os.rename(mxlFilePath, zipFilePath)
    os.system('unzip ' + zipFilePath)

    #find the file with the extension .xml
    xmlFilePath = mxlFilePath.replace('.mxl', '.xml')
    os.rename(zipFilePath, mxlFilePath)
    return xmlFilePath



if __name__ == '__main__':
    musicNotesImgPath = sys.argv[1]
    #send the command 'audiveris -transcribe -export musicNotesImgPath to the terminal
    os.system('audiveris -transcribe -export ' + musicNotesImgPath)

    #find the file with the extension .mxl
    mxlFilePath = musicNotesImgPath.replace('.png', '.mxl')

    if (not mxlFilePath.endswith('.xml')):
        xmlFilePath = convert_mxl_to_xml(mxlFilePath)
    else:
        xmlFilePath = mxlFilePath
    parse_xml(xmlFilePath)

