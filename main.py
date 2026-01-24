# TODO:
#   - DO NOT FORGET TO CHANGE PATH ONCE WHOLE TOOL HAS BEEN MADE
#   - DO NOT FORGET TO CHANGE TIMEDELTA IN find_archivable_items_in_path() WHEN DONE DEBUGGING AND TESTING
#   - debug this stupid fucking bastard eating whore licking asshole of a program. FUCK FUCK FUCK FUCK FUCK
#   - currently it ignores the cutoff date the stupid crap refuses to do a thing i say it just archives everything
#   - idk why nothing works oh cruel world WHY THE FUCK DOES IT ASK FOR USER INPUT TWICE.
#   - make a separate GUI tool


from pathlib import Path
from datetime import datetime, timedelta
import zipfile
import shutil
import sys

# group the main functions
def main():
    # checks if users launched tool properly
    if len(sys.argv) > 1 and sys.argv[1] == 'archivist':
        print("Starting tool...")
        #runs the main functions
        # set directory path
        main_directory_path = Path.home() / find_folder()
        convert_old_files_to_zip(main_directory_path)
        delete_original_uncompressed_files(main_directory_path)
    else:
        print("Type 'do-my-bidding archiver' to launch tool")

# find the main path
def find_folder():
    # start from root home directory
    home_path = Path.home().resolve()
    # take in the right and expected input from the user
    while True:
        user_input = input("Enter the name of the directory you wish to clean up. "
                           "Currently only supports folders in the User home directory: ")
        try:
            # convert the string input object into a Path object
            user_path = (home_path / user_input).resolve()

            # check to see if inputted path exists in directory
            if user_path.is_relative_to(home_path) and user_path.exists():
                return user_path.relative_to(home_path)
            else:
                # if the path is valid but does not exist in directory then try again
                print("Invalid path. Input a folder within the User home directory.")
        except Exception as e:
            # handles wrong path names
            print(f"Invalid path. Please try again. Error: {e}")

# ask users if the tool should run on startup or nah
#windows_startup_choice = input("Do you want this tool to run on startup? "
#                               "Tool will need to be launched manually if not. "
#                               " y/n: ")

# create timestamps for when the file/folder was last used,modified or created.
# only files that have been ALL unused, unmodified, and created a very long time ago can be archived
def find_archivable_items_in_path(main_directory_path):
    for item in main_directory_path.iterdir():
        # creates timestamps of directories and files
        if item.is_dir() or item.is_file():
        # creates a log of when they were last used
            modified = item.stat().st_mtime
            accessed = item.stat().st_atime

            # converts into readable format
            date_modified = datetime.fromtimestamp(modified)
            date_accessed = datetime.fromtimestamp(accessed)

            #combine the timestamps into one and get the latest date they were used#
            # how many days before the file needs to be archived
            still_in_use = max(date_modified, date_accessed) - timedelta(days=180)
            return still_in_use


# converts files and folders into zip files
def convert_to_zip(main_directory_path):
    # goes through every item in directory
    for item in main_directory_path.iterdir():
        # skips item if already a zip file
        if item.suffix == '.zip':
            continue

        # dynamic naming of zip file
        zip_name = main_directory_path / f'{item.stem}.zip'

        # archives folder subdirectories in path and scans recursively in them,
        # I do not know why the fuck this stupid shit method is raising a fucking warning god I hate this IDE
        if item.is_dir():
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
                for file in item.rglob('*'):
                    if file.is_file():
                        zipf.write(file, arcname=file.relative_to(item)) # maintain folder structure in zip file

        # archives files in path
        else:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED,  allowZip64=True) as zipf:
                zipf.write(item, arcname=item.relative_to(main_directory_path)) # maintain folder structure in zip file


def convert_old_files_to_zip(main_directory_path):
    if find_archivable_items_in_path(main_directory_path):
        convert_to_zip(main_directory_path)

def delete_original_uncompressed_files(main_directory_path):
    for item in main_directory_path.iterdir():
        if item.suffix != '.zip' and find_archivable_items_in_path(main_directory_path):
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()

main()


