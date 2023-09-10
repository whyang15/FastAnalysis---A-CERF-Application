#imported packages for application
import flet
import re
import os

#initial coomments:
#This GUI example will not show other available icons/text until a file has been successfully uploaded.
#Currently, uploading the file involves searching the file in the user's own directory
#Not sure how we can automatically call the file from CERF when a CERF file is selected?
#Once a file has been selected, the name of the file is dislayed and the other icons (i.e. for entering search) also appear.
#currently the search function can be entered in lowercase or capitals, FASTA can be in either, so when writing the backend code may need to account for either case
#The name of the uploaded file (i.e. file_name.extension, not the full path) is saved in the variable 'file'
#The full path of the uloaded file is saved to the variable 'full_path'


def main(page: flet.Page):
    #could add application name to title page
    page.title = "Learn about your FASTA file"
    page.scroll = "adaptive"
    
    #Flet code for selecting a file, if file selection successful, file is read and sequences
    #will be placed in a dictionary using seq_dictionary() function
    file_picker = flet.FilePicker()
    page.overlay.append(file_picker)
    file = None
    full_path = None
    
    #text boxes for displaying selected file name and full path, and analysis results text
    file_name = flet.Text()
    file_path = flet.Text()
    gd = flet.Text(color = "black")
    
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
            file = file_read(str(file_path.value))
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

    #icons: file selection
    file_picker = flet.FilePicker(on_result=on_dialog_result)
    #button for uploading a file, could place a text field in same row to display name of the CERF imported file??
    f = flet.Row([flet.ElevatedButton("Upload File", icon=flet.icons.UPLOAD_FILE,
                                     on_click=lambda _:file_picker.pick_files(allow_multiple= False, allowed_extensions=['fasta', '.fa', '.FA', 'txt']))])

    #Analysis functions
    #-------
    #search function
    def search_button_clicked(e):
        #add code here to search for string using string_tb.value
        t.value = f"String searched for: '{string_tb.value}'"

        #tb.value represents the variable holding the entered search, when the search button is selected, the print command prints the string to the shell
        page.update()

    #icons and variables: search engine
    t = flet.Text()
    string_tb = flet.TextField(label="Enter header or sequence search:")
    b = flet.ElevatedButton(text="Search", on_click=search_button_clicked)

    #icons and variables: general display
    
    
    
    #read the file (could be added to class)
    def file_read(fileName):
        try:
            open_file = open(fileName)
            fileCont = open_file.read() 
            return fileCont
        except OSError:
            print("The file '{}' is not found.".format(fileName))
            return False
    

    #this creates a dictionary with all newlines removed, and one singe string to contain the sequence per header
    #seq_dictionary function:
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
        print(file_dictionary)
        return file_dictionary

    #icons and variables: Find taxonomy function
    #etc.

    #Add initial file selection icons, other icons are added to the page after file selection (see on_dialog_result)
    page.add(file_picker, file_name, file_path, f, t)
    #creates sequence dictionary using the uploaded file name
    
    
flet.app(target=main)
