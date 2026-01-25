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
        # set directory path
        main_directory_path = Path.home() / find_folder()
        # executes the main functions
        items_to_archive = convert_old_files_to_zip(main_directory_path)
        delete_original_uncompressed_files(main_directory_path, items_to_archive)
    else:
        print("Type 'do-my-bidding archivist' to launch tool")

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
def is_item_archivable(item):
    # creates timestamps of directories and files
    # creates a log of when they were last used
    modified = item.stat().st_mtime
    accessed = item.stat().st_atime

    # converts into readable format
    date_modified = datetime.fromtimestamp(modified)
    date_accessed = datetime.fromtimestamp(accessed)

    #combine the timestamps into one and get the latest date they were used#
    # how many days before the file needs to be archived
    cutoff = datetime.now() - timedelta(seconds=20)
    last_used = max(date_modified, date_accessed)
    return last_used < cutoff


# converts files and folders into zip files
def convert_old_files_to_zip(main_directory_path):
    # list all archivable items
    items_to_archive = []
    # goes through every item in directory
    for item in main_directory_path.iterdir():
        # identify items to archive
        if item.suffix != '.zip' and is_item_archivable(item):
            # appends items to list
            items_to_archive.append(item)

        # validates if the item is old enough to get archived
    for archivable_item in items_to_archive:
        # Double-check the item still exists and hasn't been moved/deleted
        if not archivable_item.exists():
            continue
        # dynamic naming of zip file
        zip_name = main_directory_path / f'{archivable_item.stem}.zip'

        # archives folder subdirectories in path and scans recursively in them,
        # I do not know why the fuck this stupid shit method is raising a fucking warning god I hate this IDE
        if archivable_item.is_dir():
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
                for file in archivable_item.rglob('*'):
                    if file.is_file():
                        zipf.write(file, arcname=file.relative_to(archivable_item)) # maintain folder structure in zip file

            # archives files in path
        else:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED,  allowZip64=True) as zipf:
                zipf.write(archivable_item, arcname=archivable_item.name) # maintain folder structure in zip file
    # returns the archivable items
    return items_to_archive

# deletes the original files that got compressed
def delete_original_uncompressed_files(main_directory_path, items_to_archive):
    # iterate through the directory and only looks for .zip files belonging to the items it archived
    for item in items_to_archive:
        # Check if corresponding zip exists
        zip_name = main_directory_path / f'{item.stem}.zip'

        if zip_name.exists():
            try:
                # if the item is a directory, delete
                if item.is_dir():
                    shutil.rmtree(item)
                    print(f"Deleted folder: {item.name}")
                # if the item is a file, delete
                elif item.is_file():
                    item.unlink()
                    print(f"Deleted file: {item.name}")
            # raise error if it has trouble deleting
            except Exception as e:
                print(f"Error deleting {item.name}: {e}")




