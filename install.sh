#!/usr/bin/env bash
parsedVersion=$(python3.6 -c 'import sys; print(".".join(map(str, sys.version_info[:3])))')
echo "Python Version (3.6.x Required): " $parsedVersion
if [[ "$parsedVersion" == "3.6"*  ]]
then
    echo "Valid version"
else
    echo "Invalid version"
    exit
fi
while read requirement
 do pip install $requirement
  done < requirements.txt
echo "Requirements installed"
echo "If you wish for this to run on a schedule please add an entry in your cron tab with the necessary flags --path and --extension"
