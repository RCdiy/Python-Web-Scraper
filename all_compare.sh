#!/bin/sh
cwd=`pwd`/
files=`ls $cwd/compare*.py`
echo $files
python3="/usr/local/opt/python@3.9/Frameworks/Python.framework/Versions/3.9/bin/python3"
cmds=""
i=1;
for file in $files #"$@" 
do
    if [ $? -eq 0 ]
    then 
      echo $file
      $python3 $file
			sleep 1
    fi
done
