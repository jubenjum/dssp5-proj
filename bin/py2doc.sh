#!/bin/bash

#py_=dspr/people.py
#bs_=bin/top_spots.sh

echo "## Python scripts"
for py_ in dspr/*.py bin/*.py; do
    echo
    echo "### " $py_
    echo "\`\`\` python"
    cat $py_
    echo "\`\`\`"
    echo
    echo 
done 

echo "## Bash scripts"

for bs_ in bin/*.sh; do
    echo
    echo "### " bs__
    echo "\`\`\` bash"
    cat $bs_
    echo "\`\`\`"
    echo
    echo
done
