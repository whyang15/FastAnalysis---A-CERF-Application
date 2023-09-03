import os

dir_path = input("Please enter full directory path to your names.txt file: ")
file_path = os.path.join(dir_path, "names.txt")

def read_and_print():
    with open(file_path, "r") as file:
        content = file.read()
        print("original file content: ")
        print(content, "\n")

def ask_and_print_name():
    name = input("Please enter your first and last name: ")
    print("team member name is: ", name)

    # open member file list and append new member name:
    with open(file_path, "a") as file:
        file.write(name + "\n")

def print_newfile():
    with open(file_path, "r") as newfile:
        new_content = newfile.read()
        print("new file content: ")
        print(new_content, "\n")


def main():
    print("\n")
    read_and_print()
    ask_and_print_name()
    print_newfile()

# call the function
if __name__ == '__main__':
    main()

    

    