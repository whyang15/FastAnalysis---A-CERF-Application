#necessary modules
import flet
import re, os, sys

#from aa_dna_main import pass_file
import aa_dna_main as aa

#initial coomments:
#This GUI example will not show other available icons/text until a file has been successfully uploaded.
#Once a file has been selected, the name of the file is dislayed and the other icons (i.e. for entering search) also appear.
#currently the search function can be entered in lowercase or capitals, FASTA can be in either, so when writing the backend code may need to account for either case
#The full path of the uploaded file is saved to the variable 'full_path'

def main(page: flet.Page):
    
    #main page header
    page.title = "FastAnalysis - A CERF Application"
    #page scrolling
    page.scroll = "adaptive"
    #main page background color
    page.bgcolor = flet.colors.BLUE_100

    #text boxes for displaying selected file name and full path, and analysis results text
    file_name = flet.Text()
    file_path = flet.Text()
    gd = flet.Text(color = "black")

    #accepted FASTA  file extensions
    ext = ["faa", "fa", "fasta", "fna"]

    formatted_seq = ""

    application_description = """\nCommit Results: Selecting this icon will update all headers in the uploaded FASTA file. New header format (where 'X' denotes calculated value):
                                  -Nucleic Acid: original header + || FA output[ record_num=X seqlen=X base_counts={'A': X, 'C': X, 'G': X, 'T': X, 'U': X, 'N': X, '.': X, '-': X} AT%=X GC%=X Tm(Tm_GC)= X'C'
                                  -Amino Acids: original header + || FA output[ seqlen=X aa counts={'A': X, 'C': X, 'D': X, 'E': X, 'F': X, 'G': X, 'H': X, 'I': X, 'K': X, 'L': X, 'M': X, 'N': X, 'P': X, 'Q': X, 'R': X, 'S': X, 'T': X,
                                  'V': X, 'W':X , 'Y': X, '-': X, '*': X} hphilic_pct=X hphobic_pct=X ]
                                  \nTm: Tm is an optional selection. Selecting Tm will include Tm in only nucleic acid sequence headers. Tm will not be calculated if a sequence exceeds 500bps.
                                      -Tm is calculated using BioPython. There are 3 methods to select from. Calculations are based on default parameters.
                                      -Tm_Wallace: Follows the 'Rule of Thumb'
                                      -Tm_GC: Uses empirical formulas based on GC content.
                                      -Tm_NN: Calculaates based on nearest neighbor thermodynamics.
                                      -NOTE: This calculation does not take into account DNA/DNA, DNA/RNA, RNA/RNA and salt or chemical additives conditions.
                                  \nEnter Search String: Enter a string to search for. Search results will be generated in a seperate .txt file. The file will be labelled using the FASTA file name + the string + _additional_results.txt.
                                  \nRestriction Enzyme Search: Enter "All" to look for restriction enzyme cut sites of all enzymes in the database. "Common" will look for restriction enzyme cut sites of commonly used restriction enzymes. Or enter restriction enzyme, or list of restriction enzymes seperated by a ",". Correct RE naming conventions must be used. Search results will be saved to a seperate .txt file using FASTA file name + re + _reCut_results.txt
                                  \nGenerate ORF File: Selecting this button will generate a seperate file containing all ORF's form the uploaded file. Button will only work for FASTA files containing nucleic acid sequences. The results file will be labelled as FASTA file name + ORF_results.txt.
                                  \nNOTE: All additional files will be saved to the folder "FastAnalysis_Results" located on the desktop."""
    
    #must remain embedded within main(), when a file is selected by the user using the Upload button the file path is read in and displayed to the text boxes
    def on_dialog_result(e:flet.FilePickerResultEvent):
        if e.files != None:
            #can add other icons for other search results once those have been decided
            modified, message, formatted_seq_Wallace, formatted_seq_GC, formatted_seq_NN, formatted_seq = aa.pass_file(e.files[0].path)
            #placeholders are returned to none, in case the user selects the Uplod icon more than once
            t.value = None
            GC.value = None
            w.value = None
            NN.value = None
            #w and GC text fields are placeholders for values, they are also inclued in the page to add spacing between icons even though they do not display any data
            page.add(tm_dropdown, NN, string_tb, b, w, re_enzyme_search, re, GC, ORF, gd, c)
            file_path.value = e.files[0].path
            file_path.update()
            
            #save the TM values (optional test) to values outside of the function, only needed when file is not passed in as an argument
            #t.value holds the file with no TM included
            t.value = formatted_seq
            #GC.value holds the updated file contents with TM calculated using GC method
            GC.value = formatted_seq_GC
            #w.value holds the updated file with TM calculated using Wallace method
            w.value = formatted_seq_Wallace
            #NN.value holds the file contents with the TM calculated using NN mothod
            NN.value = formatted_seq_NN
            #file_name.value holds returned statement of whether file has been modified already or not, and whether the file contains protein or nucleotide seqs
            file_name.value = message
            file_name.update()
            gd.value = application_description
            gd.update()
        else:
            file_path.value = ''
            file_path.update()
            file_name.value = "File not selected, select a file to continue"
            file_name.update()

    #function to take in the string to be searched for and do something with it
    def search_button_clicked(e):
        output_file_path = aa.searching(file_path.value, string_tb.value)
        file_name.value = "Results of your search can be found at: " + output_file_path
        file_name.update()

    #perform restriction enyme search using user entered string
    def re_enzyme_search_clicked(e):
        message = aa.restriction_enzyme(file_path.value, re_enzyme_search.value, str(tm_dropdown.value))
        file_name.value = message
        file_name.update()

    def generate_ORF_file(e):
        message = aa.calculate_ORFs(file_path.value, "", str(tm_dropdown.value))
        file_name.value = message
        file_name.update()

    #icons and text boxes
    #containers for tm values
    t = flet.Text()
    w= flet.Text()
    GC = flet.Text()
    NN = flet.Text()

    #icons
    string_tb = flet.TextField(bgcolor=flet.colors.BLUE_50, label="Enter string search:")
    b = flet.ElevatedButton(text="Search", icon=flet.icons.SEARCH, on_click=search_button_clicked)
    file_picker = flet.FilePicker(on_result=on_dialog_result)
    f = flet.Row([flet.ElevatedButton("Upload File", icon=flet.icons.UPLOAD_FILE,
                                         on_click=lambda _:file_picker.pick_files(allow_multiple= False, allowed_extensions= ext))])


    #restriction enzyme search field
    re_enzyme_search = flet.TextField(bgcolor=flet.colors.BLUE_50, label="Enter the Restriction enzyme search: You can enter a list of restriction enzymes to search for, or look through restriction enzyme database (All or Common).")
    re = flet.ElevatedButton(text="Search", icon=flet.icons.SEARCH, on_click=re_enzyme_search_clicked)

    #button for generating ORF data for the file
    ORF = flet.ElevatedButton(text="Generate ORF File", icon=flet.icons.INSERT_DRIVE_FILE, on_click=generate_ORF_file)


    #function that's launched after the Commit button is seleted, this will write the data back to the header
    #can call a function from aa_finder.py to write the results back to the file once the commit button is selected
    def commit_clicked(e):
            if t.value == '':
                    file_name.value = "This file has already been analyzed, cannot commit results back to the file"
            else:
                    #when commit is clicked, adds Tm data to header depending on what value is selected from the tm_dropdown menu
                    #If a different Tm is selected and the commit icon is selected again (same file) the file's contents are updated and the Tm values are replaced.
                    if tm_dropdown.value == "Tm_None" or tm_dropdown.value == None:
                            aa.commit_results(file_path.value, t.value)
                    elif tm_dropdown.value == "Tm_Wallace":
                            aa.commit_results(file_path.value, w.value)
                    elif tm_dropdown.value == "Tm_GC":
                            aa.commit_results(file_path.value, GC.value)
                    elif tm_dropdown.value == "Tm_NN":
                            aa.commit_results(file_path.value, NN.value)
                    file_name.value = "File has been updated."
            file_name.update()
     
    #An info button will be displayed along with the commit button, when selected it will display a container at the bottom of the page.
    #The container will display the information that will be written back to the file if the user decides to select commit
    tm_dropdown = flet.Dropdown(label="Tm: Default = Tm_None", hint_text="Select a Tm method to include in modified header.",
                                options=[flet.dropdown.Option("Tm_None"),flet.dropdown.Option("Tm_Wallace"),flet.dropdown.Option("Tm_GC"), flet.dropdown.Option("Tm_NN"),], filled = True, bgcolor=flet.colors.BLUE_50)
    c = flet.Row([flet.ElevatedButton(bgcolor = flet.colors.BLUE_500, color = flet.colors.WHITE, text="Commit Results", on_click=commit_clicked)], alignment=flet.MainAxisAlignment.END, vertical_alignment=flet.CrossAxisAlignment.END)

    #Potential statement for using sys.argv to check whether the last command line statement was passing in a file of a valid extension [ext]
    #first check to see whether an argument was passed in from the command line (sys.argv[0] = full path to script, if an argument was passed it will be in sys.argv[1])
    length = len(sys.argv)
    if length>1 and sys.argv[1].endswith(tuple(ext)):
        #could get rid of code for reading in file, and read_file function as this is performed in the analysis code?
        modified, message, formatted_seq_Wallace, formatted_seq_GC, formatted_seq_NN, formatted_seq= aa.pass_file(sys.argv[1])
        t.value = None
        #w and GC text fields are placeholders for values, they are also inclued in the page to add spacing between icons ven though they do not display any data
        page.add(file_picker, file_name, file_path, f, t, tm_dropdown, NN, string_tb, b, w, re_enzyme_search, re, GC, ORF, gd, c)
        #for now displays the files contents
        t.value = formatted_seq
        #GC.value holds the updated file contents with TM calculated using GC method
        GC.value = formatted_seq_GC
        #w.value holds the updated file with TM calculated using Wallace method
        w.value = formatted_seq_Wallace
        #NN.value holds the file contents with the TM calculated using NN mothod
        NN.value = formatted_seq_NN
        
        file_path.value = os.path.abspath(sys.argv[1])
        file_path.update()
        #could potentially change GUI so application description is displayed in the GD text field
        file_name.value = message
        file_name.update()
        gd.value = application_description
        gd.update()
    #if no argument is passed in, will only display the Upload file icon prompting the user to select an appropriate file
    else:
         page.add(file_picker, file_name, file_path, f, t)

    
flet.app(target=main)
