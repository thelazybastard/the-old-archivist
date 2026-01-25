# The Old Archivist

A Python command-line tool that automatically identifies and archives old, unused files and folders in your home directory by compressing them into ZIP files.

## Features

- **Automatic File Detection**: Identifies files and folders that haven't been accessed or modified recently
- **Smart Compression**: Converts old items into ZIP files while preserving folder structure
- **Safe Cleanup**: Only deletes original files after successful compression
- **User-Friendly**: Simple command-line interface with guided prompts

## How It Works

The Old Archivist scans a specified directory in your home folder and:

1. Identifies files and folders based on their last access and modification times
2. Creates ZIP archives of items that meet the archival criteria 
3. Deletes the original uncompressed files/folders after successful archiving

## Installation

1. Clone this repository:
```bash
git clone https://github.com/thelazybastard/the-old-archivist.git
cd the-old-archivist
```

2. Install the package:
```bash
pip install .
```

For development mode:
```bash
pip install -e .
```

## Usage

Run the tool with:
```bash
do-my-bidding archivist
```

You'll be prompted to:
1. Enter the name of the directory you want to clean up (must be within your home directory)
2. Specify how many days old files must be before archiving

### Example
```bash
$ do-my-bidding archivist
Starting tool...
Enter the name of the directory you wish to clean up. Currently only supports folders in the User home directory: Downloads
Enter the number of days. files older than this will be archived: 90
Deleted folder: old_project
Deleted file: ancient_document.txt
```

## Configuration

The archival cutoff time is configurable at runtime. When you run the tool, you'll be asked how many days old files must be before they're archived.

For example:
- Enter `90` to archive files not accessed or modified in the last 90 days
- Enter `30` for files older than a month
- Enter `365` for files older than a year

## Requirements

- Python 3.6+
- Standard library only (no external dependencies)

## Safety Notes

**Important**: This tool permanently deletes files after archiving them. Please:
- Test on a non-critical directory first
- Verify the ZIP files are created successfully before the originals are deleted
- Keep backups of important data
- Adjust the time cutoff appropriately for production use

## File Structure

```
the-old-archivist/
├── main.py          # Main application logic
├── setup.py         # Package installation configuration
└── README.md        # This file
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Future Enhancements

- [ ] Add support for directories outside the home folder
- [ ] Implement automatic startup option
- [ ] Add configurable archival rules
- [ ] Create a configuration file for user preferences
- [ ] Add option to restore archived files

## Author

thelazybastard

## Acknowledgments

Built with Python's standard library using `pathlib`, `zipfile`, and `shutil` modules.
