#!/bin/bash


batPath="/c/Program Files/Audiveris/bin/Audiveris.bat"
inputImg=$1
exitFileName=$2
outputPath="/c/Users/schus/OneDrive/Bureau/MusicSimplifier/musicsimplifier/musicParser/$exitFileName"

cleanInputImg=${inputImg//\//\/}
cleanOutputXml=${outputPath//\//\/}

#replace inputImg extension with .xml   
"$batPath" -transcribe "$cleanInputImg" -output "$cleanOutputXml"


