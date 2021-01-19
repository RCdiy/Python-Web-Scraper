#!/bin/sh

files=`ls *.py`
echo $files
python3="/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin/python3"

clear
echo ##################################################################################

for file in $files #"$@" 
do
    if [ $? -eq 0 ]
    then 
      $python3 $file
			sleep 1
    fi
done
