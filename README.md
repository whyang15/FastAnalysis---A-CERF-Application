# FastAnalysis - A CERF Application 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flet](https://img.shields.io/badge/(https://www.google.com/url?sa=i&url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F73540154%2Fhow-to-change-the-default-loading-icon-in-a-python-flet-app&psig=AOvVaw1y6R3OVHZiv2N3hKrM8yMv&ust=1697416593893000&source=images&cd=vfe&opi=89978449&ved=0CA4QjRxqFwoTCMC8jdvn9oEDFQAAAAAdAAAAABAD)-Flet-flet.svg)
## What is FastAnalysis?
FastAnalysis is a stand alone application developed for Lab-Ally as our capstone project. Lab-Ally LLC is an Ohio based company, founded by CEO Rob Day in 2013. Lab-Ally requested an application that would work alongside their CERF 5.0 ELN software (https://lab-ally.com/products/cerf-eln/). CERF has a useful check-in and check-out feature that allows the file to be viewed and modified using outside applications, file modifications are traced when a file is checked back into CERF. Lab-Ally requested an application that could handle a type of bioinformatics file, and would analyze the files contents, perform useful analysis, then append the analysis data to the file where it could be used as metadata once checked back into CERF. The updated metadata makes the file more easily searchable, this is especially useful if a user is working with many files.

FastAnalysis fulfills all of these requests and more. FastAnalysis is a desktop application that performs analysis on, you guessed it, FASTA files. FASTA files are a commonly used formatted bioinformatics file that stores sequence data. FastAnalysis was written in Python, and uses some key packages like Flet for the GUI and BioPython for the backend sequence analysis. 

What makes FastAnalysis unique is that it offers several optional sequence analysis features, such as a commit option that modifies each sequence header in the FASTA file to inlude the sequence length, base or amino acid counts, AT and GC percentages, etc. FastAnalysis allows users to search for Restriction Enzymes (RE) cut sites in the BioPython database, search for a string, find Open Reading Frames (ORF's), or calculate Melting Temperature (Tm) using one of BioPython's calculation methods. 


## Requirements:
FastAnalysis application was developed and tested on MacOS Mojave Vers 10.14.6 and Windows 10+.

The application requires the following packages and modules installed prior to use:

  - Python 3.7 or greater.  (https://www.python.org/downloads/)
  - Flet (https://flet.dev/docs/guides/python/getting-started/)
  - BioPython 1.81 (https://biopython.org/wiki/Download)

Specific Python Packages/Modules imported for this application are the following:
flet, BioPython (Bio.SeqUtils, Bio.Seq, Bio.Restriction, Bio.SeqRecord), re, os, sys, pathlib, collections


## Installation:
A Mac and Windows desktop app is included in this repository, in addition to the original FastAnalysis scripts. 
Their are five scripts: FastAnalysis.py, aa_dna_main.py, aa_functions.py, fasta_functions.py, and nuc_functions.py. FastAnalysis.py contains main() and the GUI code. The remaining scripts contain the backend FASTA analysis. 

### To install using executable:
Download the appropriate folder for Mac OS or Windows executables.

### To install using binary:
Download all five scripts listed above into a single directory.  


## How to run the application:
- To run the Mac OS or Windows executable, navigate to the directory containing the downloaded executable file and launch the FastAnalysis application. This should open the GUI window described below and start the application.

- To start the application via scripts, ensure all scripts are contained within the same directory. Ensure that the IDE is pointed to the correct Python version.  Then, open FastAnalysis.py in your IDE and select RUN to run the module.  This should open up the GUI window and start the application.

- To run using the command line, in your terminal or command line window, navigate to the directory containing the script files and enter the following command:
  `python FastAnalysis.py`

  You can also specify the python version to run the application by entering the following command:
    `python3.10 FastAnalysis.py`
  

If you have to pass a file directly into CERF, the command `python FastAnalysis.py {path to your file}` can be used.

NOTE: Only the following FASTA extensions types are supported by FastAnalysis: ".fasta", ".fa", ".fna", ".faa". 


## Features List and How To's:
If no file has been passed into FastAnalysis, upon launching the page will only display the Upload File button. A FASTA file containing an appropriate extension is required to continue. Selecting the Upload File button will open the user's default file management system, only one file can be selected at a time.

![upload file icon](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/1149f267-2cf4-45b7-b305-82f4727169c9)

Once a file has been selected the page updates to include the analysis options. FastAnalysis will determine whether the file has already had sequence headers modified. If so, the message “This file has already been analyzed, cannot commit results back to the file” will be displayed. Additionally, if the file has already been modified then the Commit and Tm features are disabled to prevent appending duplicate data. Furthermore, FastAnalysis supports FASTA analysis containing both amino acid and nucleotide sequences, and will determine which type sequences are contained within the file. Tm, ORF, and RE searches cannot be performed on amino acid sequences and will result in an error when attempted. 

### Tm (Melting Temperature) Dropdown: 
This feature is a dropdown menu containing 4 options; Tm_None, Tm_Wallace, Tm_GC, and Tm_NN. If Tm is selected, then any other search or button selection will include Tm in the header data. It should be noted that if a file is uploaded that already has a header modified by FastAnalysis, Tm will not be appended to the header even if selected from the dropdown. The selected option will determine what method BioPython uses to calculate Tm. The exception is the Tm_None option. If Tm_None is selected Tm will not be included in the header data. Tm_None is the default option if the dropdown is not used. There is a 500bp cap to the Tm calculation. If a Tm method is selected, any sequences greater than 500bp long will not include Tm. This is to save on processing time required for longer sequences.

![Tm](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/cc628b34-76c5-47b6-bc8f-73e8b1ea6ee2)

![Tm_list](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/4a97522e-36f3-4374-bfbd-9e7aaf7dfe1c)

### Search String Text Field:
This text field allows users to enter a string. Once entered, selecting the search button located just below the text field launches the search.The results of the search get saved to the “FastAnalysis_Results” desktop folder. The results file is formatted as `{uploaded file name}_{user entered string}_additional_results.txt`.

![search_txt_field](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/a08ce032-a8b5-4cbf-a91c-a7d4491aad74)

### Restriction Enzyme (RE) Search:
The user can enter a RE search in the text field. The string is searched for by selecting the Search button located just below the text field. The user can enter “all” to search the entire REBASE database, “common” to search only commonly used ones. "All" or "Common" can be entered in any case. To search for a specific RE or a list of RE, the format of the RE must be in standard naming convention (i.e. EcoRI). If searching for more than one restriction enzyme, seperate restriction enzymes using a comma (i.e. EcoRI, BamHI, etc.). Results are saved to the “FastAnalysis_Results” desktop folder. The results file is formatted as `{uploaded file name}_{user entered string}_reCut_results.txt`.

![re_search](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/d5d3f984-25ff-4fde-8cad-b6295b80cd91)

### Generate ORF's (Open Reading Frames):
This is a button selectable by the user. ORF results are saved to the “FastAnalysis_Results” desktop folder. The results file is formatted as `{uploaded file name}_ORF _results.txt`.

![ORF](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/ef05a8d8-5438-4341-8bbb-48cd2466b5de)

### Commit Results:
This elevated button is selectable by the user. The headers of each sequence are modified to include additional data calculated by FastAnalysis. An error message will display to the user if the file has already been modified by FastAnalysis which states “This file has already been analyzed, cannot commit results back to the file”. See below for the applicable header formats, where "X" represents a calculated value and Tm is optional.

Amino Acid: {original header} + || FA output[ record_num=X seqlen=X aa_counts={'A':X, 'C':X, 'D':X, 'E':X, 'F':X, 'G':X, 'H':X, 'I':X, 'K':X, 'L':X, 'M':X, 'N':X, 'P':X, 'Q':X, 'R':X, 'S':X, 'T':X, 'V':X, 'W':X, 'Y':X, '-':X, '*':X} hphilic_pct=x hphobic_pct=X ]

Nucleic Acids: {original header} + || FA output[record_num=X seqlen=X base_counts={'A':X, 'C':X, 'G':X, 'T':X, 'U':X, 'N':X, '.':X, '-':X} AT%=X GC%=X Tm{'method selected'}=X'C']

![Commit_results](https://github.com/whyang15/BIOT671i-Group1-Capstone/assets/107033502/c3622f7d-0fac-44c4-8ee4-c70ef0b71282)


## Limitations/Features Not Supported
In this first version of FastAnalysis, we have enabled several very useful features using BioPython's modules, such as Bio.SeqUtils.MeltingTemp and Bio.Restriction.  However, there are limitations to what we currently support.  

- FASTA file extensions:
    - Currently supports only ".fasta", ".fa", ".fna", ".faa"
    - Currently does not support any zipped or gzip extensions, such as ".zip", ".gz", etc.
      
 
- Nucleotide counts:
    - Nucleotide base counts currently only support 'A', 'C', 'G', 'T', 'U', 'N', and '.' and '-' for gaps.
    - Nucleotide code list currently does not include rare or ambigous bases:
      - R ( A or G), Y (C or T), S (G or C), W (A or T), K (G or T), M (A or C), B (C or G or T), D (A or G or T), H (A or C or T), V (A or C or G)
    
- Amino Acid base counts
    - Currently only supports 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y', '-', '*'
    - Amino Acid code list currently does not include rare or ambigous bases:  B (Aspartic acid (D) or Asparagine (N)), J (Leucine (L) or Isoleucine (I)), O (Pyrrolysine), U (Selenocysteine), Z (Glutamic acid (E) or Glutamine (Q)), X (any)

    - Hydrophobic amino acid list is defined as {'A', 'F', 'G', 'I', 'L', 'M', 'P', 'V', 'W'}
        - Current hydrophobic amino acid list does not include ambigous base notation:  J (Leucine (L) or Isoleucine (I))

    - Hydrophilic amino acid list is defined as {'C', 'D', 'E', 'H', 'K', 'N', 'Q', 'R', 'S', 'T', 'Y'}
        - Current hydrophilic amino acid list does not include ambigous base notations:  B (Aspartic acid (D) or Asparagine (N)), Z (Glutamic acid (E) or Glutamine (Q))
    
    
   
- Tm calculations:
    - current implementation of the Bio.SeqUtils.MeltingTemp module supports default methods of Tm_Wallace, Tm_GC, and Tm_NN.
      - Tm_Wallace defaults:  `Bio.SeqUtils.MeltingTemp.Tm_Wallace(seq, check=True, strict=True)`
      - Tm_GC defaults:  `Bio.SeqUtils.MeltingTemp.Tm_GC(seq, check=True, strict=True, valueset=7, userset=None, Na=50, K=0, Tris=0, Mg=0, dNTPs=0, saltcorr=0, mismatch=True)`
      - Tm_NN defaults:  `Bio.SeqUtils.MeltingTemp.Tm_NN(seq, check=True, strict=True, c_seq=None, shift=0, nn_table=None, tmm_table=None, imm_table=None, de_table=None, dnac1=25, dnac2=25, selfcomp=False, Na=50, K=0, Tris=0, Mg=0, dNTPs=0, saltcorr=5)`
         
    - However, the application currently does not allow users to specify more advanced parameters of Tm_GC and Tm_NN functions, such as using different thermodynamic tables for Tm calculations in Tm_NN function, or specifying salt concentrations and DMSO concentrations.

 
- RE analysis:
    - currently supports search using RestrictionBatches function, which includes custom batches, and the preconditioned batches AllEnzymes (ALL) and CommonOnly (Common).
    - Analysis is currently limited to finding restriction sites in linear sequence (linear = True)
    - Analysis also only outputs the restriction enzymes that have cut sites found in the sequence.  We do not list out the enzymes that do not have a cut site within the sequence.
 


## References 
bioinformatics (n.d.). Iupac. Retrieved October 7, 2023, from https://www.bioinformatics.org/sms/iupac.html

Biopython (n.d.). Bio.SeqUtils.MeltingTemp module. BioPython. Retrieved October 7, 2023, from https://biopython.org/docs/1.75/api/Bio.SeqUtils.MeltingTemp.html

BioPython (n.d.). Working with Restriction Enzymes. Retrieved October 8, 2023, from http://biopython.org/DIST/docs/cookbook/Restriction.html#1

Chang, J., Chapman, B., Friedberg, I., Hamelryck, T., De Hoon, M., Cock, P., Antao, T., Talevich, E., & Wilczyński, B. (2023, February 12). BioPython Tutorial and Cookbook. Retrieved October 8, 2023, from http://biopython.org/DIST/docs/tutorial/Tutorial.html

Lab-Ally LLC (n.d.). Lab-Ally LLC - About Us. Lab-Ally. Retrieved October 8, 2023, from https://lab-ally.com/about-us/




