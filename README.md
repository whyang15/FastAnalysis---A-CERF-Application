# <FastAnalysis - A CERF Application>

## What is FastAnalysis?
FastAnalysis is a stand alone application developed for Lab-Ally as our capstone project. Lab-Ally LLC is an Ohio based company, founded by CEO Rob Day in 2013. Lab-Ally requested an application that would work alongside their CERF 5.0 ELN software (https://lab-ally.com/products/cerf-eln/). CERF has a useful check-in and check-out feature that allows the file to be viewed and modified using outside applications, file modifications are traced when a file is checked back into CERF. The application Lab-Ally requested would handle a type of bioinformatics file, and would analyze the files contents, perform useful analysis, then append the analysis data to the file where it could be used as metadata once checked back into CERF. The updated metadata makes the file more easily searchable, this is especially useful if a user is working with many files.

FastAnalysis fulfills all of these requests and more. Fastanalysis is a desktop application that performs analysis on FASTA files; a commonly used formatted bioinformatics file that stores sequence data. FastAnalysis was written in Python, and uses some key packages like Flet for the GUI and BioPython for the backend sequence analysis. 

What makes FastAnalysis unique is that it offers several optional sequence analysis features, such as a commit option that modifies each sequence header in the FASTA file to inlude the sequence length, base or amino acid counts, At and GC percentages, etc. Additionally, FastAnalysis allows users to search for Restriction Enzymes cut sites in the BioPython database, or the user can search for a sequence string within the file. ORF's can also be calulated.

## Requirements:

A Mac and Windows desktop app is included in this repository, in addition to the original FastAnalysis scripts. The FastAnalysis scripts require Python 3.7 or greater, and require Flet and BioPython packages. The other packages used are often included when Python is downloaded. Their are 5 scripts: FastAnalysis.py, aa_dna_main.py, aa_functions.py, fasta_functions.py, and nuc_functions.py. FastAnalysis.py contains main() and the GUI code. To run the scripts, ensure all scripts are contained within the same directory. FastAnalysis.py can be opened and ran in your IDE or choice, or "python FastAnalysis.py" can be used on the command line. To pass a file directly into CERF, "python FastAnalysis.py {path to your file}" can be used. 

Imported Packages:

flet
BioPython


## Installation:

To download the Mac or Windows App, download the appropriate folder.


## Features List:

## How to Use:

## Testing:

## Limitations/Features Not Supported

## Collaborators: (Roles?)

## Badges
[badmath](https://img.shields.io/github/languages/top/lernantino/badmath)

