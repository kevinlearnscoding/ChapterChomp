# ChapterChomp

**ChapterChomp** is a simple application for parsing Final Cut Pro X FCPXML files to extract timecodes and titles of Chapter Markers. The app generates a table of chapter markers that can be copied to the clipboard or saved as a text file.

## Features
- **Parse FCPXML**: Quickly extracts chapter marker information, including timecodes and titles.
- **Editable Text Window**: View and edit the extracted chapter data before copying or saving.
- **Copy to Clipboard**: Copies all text in the window to your clipboard with a single click.
- **Save as .txt**: Saves the extracted chapter data as a .txt file in a location of your choice.
- **Close with Options**: Optionally delete the FCPXML file upon closing or simply exit the app.

## Getting Started

### Prerequisites
No prior coding knowledge is required. Just download and run ChapterChomp.

### Instructions

1. In **Final Cut Pro**, choose `File > Export XML...` and save the XML file on your computer.
2. Open **ChapterChomp**.
3. Select the XML file you saved and click **Open**.
4. ChapterChomp will parse the file, producing a table of timecodes and chapter text in an editable window.
5. Choose from the following options:
   - **Copy to Clipboard**: Copies the table of chapter markers to your clipboard.
   - **Save as .txt**: Saves the text to a .txt file in a location you choose.
   - **Close**: Closes the app. You’ll be prompted to delete the XML file or simply exit the app.

### Example Workflow
1. Export an XML file from Final Cut Pro.
2. Open ChapterChomp, select the file, and view your chapter marker table.
3. Copy the table for immediate use or save it as a .txt file.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support
For questions or help with ChapterChomp, please open an issue in the repository.
