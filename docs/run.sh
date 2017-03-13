#!/bin/bash

# script to build the document, transforms md -> pdf with pandoc

output=DSSP5_JuanBenjumea.docx
cls=ieee-with-url.csl

## https://github.com/matthiasbeyer/pandoc-paper-template/blob/master/Makefile

pandoc report.md \
    --filter pandoc-fignos \
    --variable linestretch=1.5 \
    --variable papersize=a4paper \
    --bibliography=biblio.bib \
    --filter pandoc-citeproc --latex-engine=xelatex \
    --csl=$cls  -o $output


