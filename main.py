# TODO:
#   - compare the items to the cutoff date. if still being used then do not archive them
#   - create zip files for both files and folders
#   - zip files must be named after the folder or file it is archiving

from pathlib import Path
from datetime import datetime, timedelta
import zipfile

#find the download path
downloads_path = Path.home() / "Downloads"

# how many days before the file needs to be archived
cutoff = timedelta(days=365)

# create timestamps for when the file/folder was last used,modified or created.
# only files that have been ALL unused, unmodified, and created a very long time ago can be archived
for items in downloads_path.iterdir():
    if items.is_dir():
        created = items.stat().st_ctime
        modified = items.stat().st_mtime
        accessed = items.stat().st_atime

        date_created = datetime.fromtimestamp(created)
        date_modified = datetime.fromtimestamp(modified)
        date_accessed = datetime.fromtimestamp(accessed)

        #combine the timestamps into one and get the latest date they were used
        still_in_use = max(date_modified, date_accessed)





