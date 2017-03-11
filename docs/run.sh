#!/bin/bash

# script to build the document, transforms md -> pdf with pandoc

output=DSSP5_JuanBenjumea.pdf

pandoc report.md --latex-engine=xelatex -o $output

