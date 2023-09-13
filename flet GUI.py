#imported packages for application
import flet
import re, os

#initial coomments:
#This GUI example will not show other available icons/text until a file has been successfully uploaded.
#Currently, uploading the file involves searching the file in the user's own directory
#Not sure how we can automatically call the file from CERF when a CERF file is selected?
#Once a file has been selected, the name of the file is dislayed and the other icons (i.e. for entering search) also appear.
#currently the search function can be entered in lowercase or capitals, FASTA can be in either, so when writing the backend code may need to account for either case
#The name of the uploaded file (i.e. file_name.extension, not the full path) is saved in the variable 'file'
#The full path of the uloaded file is saved to the variable 'full_path'

def file_read(fileName):
        try:
            open_file = open(fileName)
            fileCont = open_file.read() 
            return fileCont
        except OSError:
            print("The file '{}' is not found.".format(fileName))
            return False

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
    
#this function returns the path of the checked out file in CERF
#the name of the file does not need to be know, the function searches all subfolders of the .cerf folder for appropriate file extensions
#HOWEVER, the script is required to be saved in the .cerf folder in order for the file to be found.
#Additionally, there can only be one file of extension ".txt", ".fasta", or ".fa" checked out at a time
    
def import_CERF():
    rootdir = os.getcwd()
    full_path = None
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            filepath = subdir + os.sep + file
            if (filepath.endswith(".txt") or filepath.endswith(".fasta") or filepath.endswith(".fa")) and file != "Quickstart.txt":
                full_path = filepath
    if full_path != None:
        return full_path
    else:
        return False
    
def main(page: flet.Page):
    #could add application name to title page
    page.title = "Learn about your FASTA file"
    page.scroll = "adaptive"
    
    #Flet code for selecting a file, if file selection successful, file is read and sequences
    #will be placed in a dictionary using seq_dictionary() function
    file = None
    full_path = None

    #text boxes for displaying selected file name and full path, and analysis results text
    file_name = flet.Text()
    file_path = flet.Text()
    gd = flet.Text(color = "black")

    #must remain embedded within main()
    def on_dialog_result(e:flet.FilePickerResultEvent):
        if e.files != None:
            file_name.value = (
                ", ".join(map(lambda f: f.name, e.files)) if e.files else "Cancelled!"
                )
            #can add other icons for other search results once those have been decided
            page.add(string_tb, b, gd)
            file_name.update()
            file_path.value = e.files[0].path
            file_path.update()
            file = file_read(file_path.value)
            full_path = file_path.value
            if file != None:
                seq_dictionary = seq_dictionary_generator(file)
                t.value = list(seq_dictionary.keys())
            gd.value = "\n Would call functions for other analysis and display results here, for example: \n\n GC content \n\n Taxonomy"
            gd.update()
        else:
            file_path.value = ''
            #add if/else to remove string_tb, b, etc. from the page if no file is selected
            file_name.value =f"File not selected, please select a file to continue."
        page.update()

    def search_button_clicked(e):
        t.value = f"String searched for: '{string_tb.value}'"
        page.update()
        
    t = flet.Text()
    string_tb = flet.TextField(label="Enter header or sequence search:")
    b = flet.ElevatedButton(text="Search", on_click=search_button_clicked)
    file_picker = flet.FilePicker(on_result=on_dialog_result)
    f = flet.Row([flet.ElevatedButton("Upload File", icon=flet.icons.UPLOAD_FILE,
                                         on_click=lambda _:file_picker.pick_files(allow_multiple= False, allowed_extensions=['fasta', 'fa', 'txt']))])

    #If there is a checked out CERF file, then the 
    if import_CERF() != False:
        page.add(file_picker, file_name, file_path, f, t)
        file_path.value = import_CERF()
        file_path.update()
        file = file_read(file_path.value)
        page.add(string_tb, b, gd)
        seq_dictionary = seq_dictionary_generator(file)
        t.value = (list(seq_dictionary.keys()))
        t.update()
        gd.value = "\n Would call functions for other analysis and display results here, for example: \n\n GC content \n\n Taxonomy"
        gd.update()
    else:
        page.add(file_picker, file_name, file_path, f, t)
    
flet.app(target=main)
