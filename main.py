# TODO:
#   - DO NOT FORGET TO CHANGE PATH ONCE WHOLE TOOL HAS BEEN MADE
#   - DO NOT FORGET TO CHANGE TIMEDELTA IN find_archivable_items_in_path() WHEN DONE DEBUGGING AND TESTING
#   - turn script into CLI tool
#   - runs indefinitely in background until users stop it
#   - users define folder the tool will operate on


from pathlib import Path
from datetime import datetime, timedelta
import zipfile
import shutil

# find the download path
downloads_path = Path.home() / "Downloads/demo"

# create timestamps for when the file/folder was last used,modified or created.
# only files that have been ALL unused, unmodified, and created a very long time ago can be archived
def find_archivable_items_in_path():
    for item in downloads_path.iterdir():
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
            still_in_use = max(date_modified, date_accessed) - timedelta(seconds=5)
            return still_in_use


# converts files and folders into zip files
def convert_to_zip():
    # goes through every item in directory
    for item in downloads_path.iterdir():
        # skips item if already a zip file
        if item.suffix == '.zip':
            continue

        # dynamic naming of zip file
        zip_name = downloads_path / f'{item.stem}.zip'

        # archives folder subdirectories in path and scans recursively in them
        if item.is_dir():
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
                for file in item.rglob('*'):
                    if file.is_file():
                        zipf.write(file, arcname=file.relative_to(item)) # maintain folder structure in zip file

        # archives files in path
        else:
            with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED,  allowZip64=True) as zipf:
                zipf.write(item, arcname=item.relative_to(downloads_path)) # maintain folder structure in zip file


def convert_old_files_to_zip():
    if find_archivable_items_in_path():
        convert_to_zip()

def delete_original_uncompressed_files():
    for item in downloads_path.iterdir():
        if item.suffix != '.zip' and find_archivable_items_in_path():
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()

convert_old_files_to_zip()
delete_original_uncompressed_files()


