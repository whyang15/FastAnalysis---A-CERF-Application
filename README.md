# FastAnalysis - A CERF Application 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flutter(Flet)](https://img.shields.io/badge/Flutter-%2302569B.svg?style=for-the-badge&logo=Flutter&logoColor=white)
## What is FastAnalysis?
FastAnalysis is a stand alone application developed for Lab-Ally as our capstone project. Lab-Ally LLC is an Ohio based company, founded by CEO Rob Day in 2013. Lab-Ally requested an application that would work alongside their CERF 5.0 ELN software (https://lab-ally.com/products/cerf-eln/). CERF has a useful check-in and check-out feature that allows the file to be viewed and modified using outside applications, file modifications are traced when a file is checked back into CERF. Lab-Ally requested an application that could handle a type of bioinformatics file, and would analyze the files contents, perform useful analysis, then append the analysis data to the file where it could be used as metadata once checked back into CERF. The updated metadata makes the file more easily searchable, this is especially useful if a user is working with many files.

FastAnalysis fulfills all of these requests and more. FastAnalysis is a desktop application that performs analysis on, you guessed it, FASTA files. FASTA files are a commonly used formatted bioinformatics file that stores sequence data. FastAnalysis was written in Python, and uses some key packages like Flet for the GUI and BioPython for the backend sequence analysis. 

What makes FastAnalysis unique is that it offers several optional sequence analysis features, such as a commit option that modifies each sequence header in the FASTA file to inlude the sequence length, base or amino acid counts, AT and GC percentages, etc. FastAnalysis allows users to search for Restriction Enzymes (RE) cut sites in the BioPython database, search for a string, find Open Reading Frames (ORF's), or calculate Melting Temperature (Tm) using one of BioPython's calculation methods. 

## Requirements:

A Mac and Windows desktop app is included in this repository, in addition to the original FastAnalysis scripts. The FastAnalysis scripts require Python 3.7 or greater, and require Flet and BioPython packages. Their are 5 scripts: FastAnalysis.py, aa_dna_main.py, aa_functions.py, fasta_functions.py, and nuc_functions.py. FastAnalysis.py contains main() and the GUI code. The remaining scripts contain the backend FASTA analysis. To run the scripts, ensure all scripts are contained within the same directory. FastAnalysis.py can be opened and ran in your IDE of your choice, or use the command line and navigate to the directory containing the script files and enter "python FastAnalysis.py". To pass a file directly into CERF, the command "python FastAnalysis.py {path to your file}" can be used.

NOTE: Only the following FASTA extensions types are supported by FastAnalysis: ".fasta", ".fa", ".fna", ".faa". 

### Imported Python Packages/Modules:

flet, BioPython (Bio.SeqUtils, Bio.Seq, Bio.Restriction, Bio.SeqRecord), re, os, sys, pathlib, collections

## Installation:

To download the Mac or Windows App, download the appropriate folder. 

## Features List and How To's:
If no file has been passed into FastAnalysis, upon launching the page will only display the Upload File button. A FASTA file containing an appropriate extension is required to continue. Selecting the Upload File button will open the user's default file management system, only one file can be selected at a time.

![upload file icon](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/1149f267-2cf4-45b7-b305-82f4727169c9)

Once a file has been selected the page updates to include the analysis options. FastAnalysis will determine whether the file has already had sequence headers previously modified, if so, the message “This file has already been analyzed, cannot commit results back to the file” will be displayed. Additionally, if the file has already been modified then the Commit and Tm features are disabled to prevent appending duplicate data. Additionally, FastAnalysis supports FASTA analysis containing both amino acid and nucleotide sequences, and will determine which type sequences are contained within the file. Tm, ORF, and RE searches cannot be performed on amino acid sequences and will result in an error when attempted. 

### Tm (Melting Temperature) Dropdown: 
This feature is a dropdown menu containing 4 options; Tm_None, Tm_Wallace, Tm_GC, and Tm_NN. If Tm is selected, then any other search or button selection will include Tm in the header data. It should be noted that if a file is uploaded that already has a header modified by FastAnalysis, Tm will not be appended to the header even if selected from the dropdown. The selected option will determine what method BioPython uses to calculate Tm. The exception is the Tm_None option. If Tm_None is selected Tm will not be included in the header data. Tm_None is the default option if the dropdown is not used. There is a 500bp cap to the Tm calculation. If a Tm method is selected, any sequences greater than 500bp long will not include Tm. This is to save on processing time required for longer sequences.

![Tm](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/cc628b34-76c5-47b6-bc8f-73e8b1ea6ee2)

![Tm_list](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/4a97522e-36f3-4374-bfbd-9e7aaf7dfe1c)

### Search String Text Field:
This text field allows users to enter a string. Once entered, selecting the search button located just below the text field launches the search.The results of the search get saved to the “FastAnalysis_Results” desktop folder. The results file is formatted as {uploaded file name}_{user entered string}_additional_results.txt.

![search_txt_field](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/a08ce032-a8b5-4cbf-a91c-a7d4491aad74)

### Restriction Enzyme (RE) Search:
The user can enter a RE search in the text field, the string is searched for by selecting the Search button located just below the text field. The user can enter “all” to search the entire database, “common” to search only common ones. "All" or "Common" can be entered in any case. To search for a specific RE or a list of RE, the format of the RE must be in standard naming convention (i.e. EcoRI). If searching for more than 1, seperate restriction enzymes using a comma (i.e. EcoRI, BamHI, etc.). Results are saved to the “FastAnalysis_Results” desktop folder. The results file is formatted as {uploaded file name}_{user entered string}_reCut_results.txt.

![re_search](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/d5d3f984-25ff-4fde-8cad-b6295b80cd91)

### Generate ORF's (Open Reading Frames):
This is a button selectable by the user. ORF results are saved to the “FastAnalysis_Results” desktop folder. The results file is formatted as {uploaded file name}_ORF _results.txt.

![ORF](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/ef05a8d8-5438-4341-8bbb-48cd2466b5de)

### Commit Results:
This elevated button is selectable by the user. The headers of each sequence are modified to include additional data calculated by FastAnalysis. An error message will display to the user if the file has already been modified by FastAnalysis which states “This file has already been analyzed, cannot commit results back to the file”. See below for the applicable header formats, where "X" represents a calculated value and Tm is optional.

Amino Acid: {original header} + || FA output[ record_num=X seqlen=X aa_counts={'A':X, 'C':X, 'D':X, 'E':X, 'F':X, 'G':X, 'H':X, 'I':X, 'K':X, 'L':X, 'M':X, 'N':X, 'P':X, 'Q':X, 'R':X, 'S':X, 'T':X, 'V':X, 'W':X, 'Y':X, '-':X, '*':X} hphilic_pct=x hphobic_pct=X ]

Nucleic Acids: {original header} + || FA output[record_num=X seqlen=X base_counts={'A':X, 'C':X, 'G':X, 'T':X, 'U':X, 'N':X, '.':X, '-':X} AT%=X GC%=X Tm{'method selected'}=X'C']

![Commit_results](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/c3622f7d-0fac-44c4-8ee4-c70ef0b71282)

## Limitations/Features Not Supported


