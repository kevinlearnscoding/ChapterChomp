import sys
import os
import shutil  # Import shutil for directory removal
import xml.etree.ElementTree as ET
from pathlib import Path
from tkinter import Tk, messagebox, Text, Button, Frame, Toplevel, Label
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pyperclip

def parseFCPTimeSeconds(timeString):
    vals = [float(n) for n in timeString.replace('s', '').split('/')]
    return vals[0] / vals[1] if len(vals) > 1 else vals[0]

class Marker:
    def __init__(self, name, startTime):
        self._name = name
        self._startTime = startTime

    @property
    def startTime(self):
        return self._startTime

    @property
    def name(self):
        return self._name

    @staticmethod
    def scanForMarker(element, time=[]):
        start = offset = 0
        try:
            start = parseFCPTimeSeconds(element.attrib['start'])
        except KeyError:
            pass

        try:
            offset = parseFCPTimeSeconds(element.attrib['offset'])
        except KeyError:
            pass

        m = []
        if 'chapter-marker' == element.tag:
            m.append(Marker(element.attrib['value'], start + sum(time)))
        else:
            time.append(offset - start)
            for el in element:
                m.extend(Marker.scanForMarker(el, list(time)))
        return m

def format_time(seconds):
    """Format seconds into H:M:S."""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

def display_time_codes(time_codes):
    """Create a window to display the time codes."""
    def copy_to_clipboard():
        # Copy only the content of the text area (excluding static text)
        time_codes_text = text_area.get("1.0", "end-1c")  # Get text without trailing newline
        pyperclip.copy(time_codes_text)
        messagebox.showinfo("Copied!", "Time Codes copied to clipboard.")

    def save_as_txt():
        save_path = asksaveasfilename(initialdir=Path.home() / 'Desktop',
                                       title="Save Chapter Markers as .txt file",
                                       defaultextension=".txt",
                                       filetypes=[("Text Files", "*.txt")])
        if save_path:
            try:
                with open(save_path, 'w') as output_file:
                    output_file.write(text_area.get("1.0", "end-1c"))
                messagebox.showinfo("Success", f"Chapter Markers saved to: {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save markers: {e}")

    window = Toplevel()
    window.title("Chapter Markers")

    # Static message label
    static_text = (
        "To activate the YouTube chapter function, copy and paste the below table into the YouTube description box or top pinned comment.\n"
        "Be sure the first time code in the table is 00:00 or YouTube won't recognize the time code table as time codes.\n"
        "To create the 00:00 time code, either add it manually here, or add a chapter marker at 00:00 on your Final Cut Pro timeline."
    )

    # Frame for static text and text area
    frame = Frame(window)
    frame.pack(pady=10)

    # Label for static text
    static_label = Label(frame, text=static_text, wraplength=400)
    static_label.pack()

    # Text area for time codes
    text_area = Text(frame, wrap="word", height=10, width=60)
    text_area.insert("1.0", "Time Codes\n" + "\n".join(time_codes))  # Include Time Codes label
    text_area.pack()

    # Buttons
    button_frame = Frame(window)
    button_frame.pack(pady=10)

    copy_button = Button(button_frame, text="Copy to Clipboard", command=copy_to_clipboard)
    copy_button.pack(side="left", padx=5)

    save_button = Button(button_frame, text="Save as .txt", command=save_as_txt)
    save_button.pack(side="left", padx=5)

    close_button = Button(button_frame, text="Close", command=window.destroy)
    close_button.pack(side="left", padx=5)

    # Ensure the window stays open until closed
    window.protocol("WM_DELETE_WINDOW", window.destroy)

    # Wait for the window to close before continuing
    window.wait_window()

def main():
    # Display information pop-up
    Tk().withdraw()  # Hide the root window
    messagebox.showinfo("Instructions", 
        "To use this program, export an XML file from Final Cut Pro. \n\n"
        "In Final Cut Pro 10.8.1, go to the File menu and select\n'Export XML...'\n\n"
        "Final Cut Pro will export a .fcpxmld file.\n\n"
        "Click OK below to locate the file in Finder.")

    # Check if a file was dropped onto the app
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        # Prompt for a file if not provided
        input_path = askopenfilename(title="Select an .FCPXML File", filetypes=[("FCPXML Files", "*.fcpxmld")])

    # Check if the provided path is a .fcpxmld package
    if input_path.endswith('.fcpxmld'):
        # Use the Info.fcpxml file directly
        info_file_path = os.path.join(input_path, 'Info.fcpxml')

        # Debugging: print the expected path
        print(f"Expected Info.fcpxml path: {info_file_path}")

        if not os.path.isfile(info_file_path):
            print(f"Error: '{info_file_path}' not found. Please ensure the .fcpxmld package is structured correctly.")
            return

        input_path = info_file_path
    elif not input_path.endswith('.fcpxml'):
        print("The selected file is not a valid .fcpxmld or .fcpxml file.")
        return

    # Parse the XML file
    try:
        xmlroot = ET.parse(input_path).getroot()
        markers = sorted(Marker.scanForMarker(xmlroot), key=lambda s: s.startTime)
        print(f"Markers found: {len(markers)}")  # Debugging line
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return
    except Exception as e:
        print(f"Unexpected error: {e}")
        return

    final_list = []

    # Collect and format marker data
    for m in markers:
        formatted_time = format_time(m.startTime)
        final_list.append(f"{formatted_time} {m.name}")

    # Display the time codes in an editable text window
    display_time_codes(final_list)

    # Optionally, delete the original .fcpxmld file if the user agrees, after displaying time codes
    Tk().withdraw()  # Hide the root window for the next dialog
    delete_confirmation = messagebox.askyesno("Delete Original File", "Would you like to delete the original .fcpxmld file?")
    if delete_confirmation:
        try:
            shutil.rmtree(os.path.dirname(input_path))  # Delete the package and all its contents
            messagebox.showinfo("Deleted", "The original .fcpxmld file has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete file: {e}")

if __name__ == "__main__":
    main()
