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

def file_read(fileName):
        try:
            open_file = open(fileName)
            fileCont = open_file.read() 
            return fileCont
        except OSError:
            print("The file '{}' is not found.".format(fileName))
            return False

def main(page: flet.Page):
    
    #could add application name to title page
    #main page header
    page.title = "Learn about your FASTA file"
    #page scrolling
    page.scroll = "adaptive"
    #main page background color
    page.bgcolor = flet.colors.BLUE_100
    
    #Flet code for selecting a file, if file selection successful, file is read and sequences
    #will be placed in a dictionary using seq_dictionary() function
    file = None

    #text boxes for displaying selected file name and full path, and analysis results text
    #may not need file_name box anymore
    file_name = flet.Text()
    file_path = flet.Text()
    gd = flet.Text(color = "black")

    #accepted FASTA  file extensions
    ext = ["faa", "fa", "fasta", "fna", "FAA", "FA", "FASTA", "FNA"]

    results = ""
    formatted_seq = ""
    
    #must remain embedded within main(), when a file is selected by the user using the Upload button the file path is read in and displayed to the text boxes
    def on_dialog_result(e:flet.FilePickerResultEvent):
        if e.files != None:
            #can add other icons for other search results once those have been decided
            modified, message, formatted_seq = aa.pass_file(e.files[0].path) 
            page.add(string_tb, b, gd, c)
            file_path.value = e.files[0].path
            file_path.update()
            file = file_read(file_path.value)
            #currently displays all of file contents, could remove?
            t.value = file + "\n\n" + message
            t.update()
            gd.value = "\n\nAnalysis results: \n"
            gd.update()
        else:
            file_path.value = ''
            file_path.update()
            file_name.value = "File not selected, select a file to continue"
            file_name.update()
        return modified, message
        page.update()

    #function to take in the string to be searched for and do something with it
    def search_button_clicked(e):
        t.value = f"String searched for: '{string_tb.value}'"
        page.update()

    #icons and text boxes
    t = flet.Text()
    string_tb = flet.TextField(label="Enter header or sequence search:")
    b = flet.ElevatedButton(text="Search", icon=flet.icons.SEARCH, on_click=search_button_clicked)
    file_picker = flet.FilePicker(on_result=on_dialog_result)
    f = flet.Row([flet.ElevatedButton("Upload File", icon=flet.icons.UPLOAD_FILE,
                                         on_click=lambda _:file_picker.pick_files(allow_multiple= False, allowed_extensions=['fasta', 'fa', 'faa', 'fna']))])


    #function that's launched after the Commit button is seleted, this will write the data back to the header
    #can call a function from aa_finder.py to write the results back to the file once the commit button is selected
    def commit_clicked(e):
            if formatted_seq == '':
                    gd.value = "This file has already been analyzed, cannot commit results back to the file"
            else:
                    aa.commit_results(file_path.value, formatted_seq)
                    gd.value = "File has been updated."
            gd.update()

    #Code for creating info button and bottom sheet, provides info to the user about what is committed back to the file
    def close_bs(e):
            bs.open = False
            page.update()
            
    bs = flet.BottomSheet(flet.Container(flet.Row(
            [flet.Text("Selecting the Commit Button will write the results back to each sequence header\nIf results have already been previously committed, nothing will be added to the file."),
            flet.ElevatedButton("Okay", on_click=close_bs)]), bgcolor=flet.colors.WHITE, padding=10, animate=flet.animation.Animation(1000, "bounceOut")))
    page.overlay.append(bs)

    def show_bs_click(e):
            bs.open = True
            page.update()
            
    #An info button will be displayed along with the commit button, when selected it will display a container at the bottom of the page.
    #The container will display the information that will be written back to the file if the user decides to select commit
    c = flet.Row([flet.ElevatedButton(text="Commit Results", on_click=commit_clicked), flet.ElevatedButton("Info", icon=flet.icons.INFO_OUTLINED, on_click=show_bs_click)], alignment=flet.MainAxisAlignment.END, vertical_alignment=flet.CrossAxisAlignment.END)

    #Potential statement for using sys.argv to check whether the last command line statement was passing in a file of a valid extension [ext]
    #first check to see whether an argument was passed in from the command line (sys.argv[0] = full path to script, if an argument was passed it will be in sys.argv[1])
    length = len(sys.argv)
    if length>1 and sys.argv[1].endswith(tuple(ext)):
        #could get rid of code for reading in file, and read_file function as this is performed in the analysis code?
        file = file_read(sys.argv[1])
        #if create a seperate function to write back to the file upon committing, can remove second argument from pass_file
        modified, message, formatted_seq = aa.pass_file(file_read(sys.argv[1]))
        page.add(file_picker, file_name, file_path, f, t, string_tb, b, gd, c)
        #for now displays the files contents
        t.value = file + "\n\n" + message
        t.update()
        file_path.value = os.path.abspath(sys.argv[1])
        file_path.update()
        gd.value = "Analysis results will display here"
        gd.update()
    #if no argument is passed in, will only display the Upload file icon prompting the user to select an appropriate file
    else:
         page.add(file_picker, file_name, file_path, f, t)

    
flet.app(target=main)
