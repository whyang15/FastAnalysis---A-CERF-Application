#imported packages for application
import flet
import re, os, sys
import aa_finder

#initial coomments:
#This GUI example will not show other available icons/text until a file has been successfully uploaded.
#Once a file has been selected, the name of the file is dislayed and the other icons (i.e. for entering search) also appear.
#currently the search function can be entered in lowercase or capitals, FASTA can be in either, so when writing the backend code may need to account for either case
#The name of the uploaded file (i.e. file_name.extension, not the full path) is saved in the variable 'file'
#The full path of the uploaded file is saved to the variable 'full_path'

def file_read(fileName):
        try:
            open_file = open(fileName)
            fileCont = open_file.read() 
            return fileCont
        except OSError:
            print("The file '{}' is not found.".format(fileName))
            return False

#don't necessarily need this anymore, when performing analysis can keep this in the script containing all the analysis functions
def seq_dictionary_generator(fileCont):

        file_dictionary = {}
        seq = ''
        
        for line in fileCont.split('\n'):
            
            if line.startswith('>'):
                if seq != '':
                    file_dictionary[header].append(seq)
                    seq = ''
                header = line.rstrip('\n')
                if header not in file_dictionary:
                    file_dictionary[header] = []
            else:
                sequence = line.strip('\n')
                seq = str(seq) + str(sequence)
                    
        file_dictionary[header].append(seq)
        return file_dictionary
    
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
    full_path = None

    #text boxes for displaying selected file name and full path, and analysis results text
    file_name = flet.Text()
    file_path = flet.Text()
    gd = flet.Text(color = "black")

    #accepted FASTA  file extensions
    ext = ["faa", "fa", "fasta", "fna", "FAA", "FA", "FASTA", "FNA"]

    results = ""
        
    #must remain embedded within main(), when a file is selected by the user using the Upload button the file path is read in and displayed to the text boxes
    def on_dialog_result(e:flet.FilePickerResultEvent):
        if e.files != None:
            file_name.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
                )
            #can add other icons for other search results once those have been decided
            page.add(string_tb, b, gd, c)
            file_name.update()
            file_path.value = e.files[0].path
            file_path.update()
            file = file_read(file_path.value)
            full_path = file_path.value
            gd.value = "Analysis Results: \n\n\n\n\n\n "
            gd.update()
        else:
            file_path.value = ''
            #add if/else to remove string_tb, b, etc. from the page if no file is selected
            file_name.value =f"File not selected, please select a file to continue."
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
            gd.value = aa_finder.primary(True)
            gd.update()
    c = flet.Row([flet.ElevatedButton(text="Commit Results", on_click=commit_clicked)], alignment=flet.MainAxisAlignment.END, vertical_alignment=flet.CrossAxisAlignment.END)

    #Potential statement for using sys.argv to check whether the last command line statement was passing in a file of a valid extension [ext]
    #first check to see whether an argument was passed in from the command line (sys.argv[0] = full path to script, if an argument was passed it will be in sys.argv[1])
    length = len(sys.argv)
    if length>1 and sys.argv[1].endswith(tuple(ext)):
        file = file_read(sys.argv[1])
        page.add(file_picker, file_name, file_path, f, t, string_tb, b, gd, c)
        #for now displays the files contents
        t.value = file
        t.update()
        file_path.value = os.path.abspath(sys.argv[1])
        file_path.update()
        gd.value = "Analysis results will display here"
        gd.update()
    #if no argument is passed in, will only display the Upload file icon prompting the user to select an appropriate file
    else:
         page.add(file_picker, file_name, file_path, f, t)

flet.app(target=main)
