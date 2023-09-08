#imported packages for application
import flet
import re

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
    
    #Flet code for selecting a file
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
            file = file_name.value
            file_path.value = e.files[0].path
            file_path.update()
            full_path = file_path.value
            gd.value = "\n Would call functions for other analysis and display results here, for example: \n\n GC content \n\n Taxonomy"
            gd.update()
            seq_dictionary = seq_dictionary_generator(file_read(file))
        else:
            file_path.value = ''
            #add if/else to remove string_tb, b, etc. from the page if no file is selected
            file_name.value =f"File not selected, please select a file to continue."
        page.update()

    #icons: file selection
    file_picker = flet.FilePicker(on_result=on_dialog_result)
    #button for uploading a file, could place a text field in same row to display name of the CERF imported file??
    f = flet.Row([flet.ElevatedButton("Upload File", icon=flet.icons.UPLOAD_FILE,
                                     on_click=lambda _:file_picker.pick_files(allow_multiple= False, allowed_extensions=['fasta', '.fa', 'txt']))])

    #def read_file(x):
        #read_file = open(x, 'r')
        #print(read_file[0])

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
    
    
    
    #read the file
    def file_read(fileName):
        try:
            file = open(str(fileName), "r")
            fileCont = file.readlines()
            return fileCont
        except OSError:
            print("The file '{}' is not found.".format(fileName))
            return False
    #icons and variables: read
    
    
    #seq_dictionary function:
    def seq_dictionary_generator(fileCont):
    
        header_position = []
        file_dictionary = {}
        
        for line in str(fileCont):
            if '>' in line:
                header_position.append(fileCont.index(line))
                
        for pos in header_position:
            file_dictionary[fileCont[pos]] = ' '.join(map(str,fileCont[pos+1:pos+2]))

        return file_dictionary

    #icons and variables: Find taxonomy function
    #etc.

    #Add initial file selection icons, other icons are added to the page after file selection (see on_dialog_result)
    page.add(file_picker, file_name, file_path, f, t)
    #creates sequence dictionary using the uploaded file name
    
    
flet.app(target=main)
