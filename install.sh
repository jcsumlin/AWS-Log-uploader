#!/usr/bin/env bash
parsedVersion=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
echo "Python Version (2.7.x Required): " $parsedVersion
if [[ "$parsedVersion" == "2.7"*  ]]
then
    echo "Valid version"
else
    echo "Invalid version"
    exit
fi
pip install --upgrade pip
while read requirement
 do pip install $requirement
  done < requirements.txt
echo "Requirements installed"
echo "If you wish for this to run on a schedule please add an entry in your cron tab with the necessary flags --path and --extension"
