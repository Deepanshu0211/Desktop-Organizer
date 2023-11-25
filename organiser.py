import os
import shutil
import tkinter as tk
from tkinter import filedialog

class DesktopOrganizerApp:
    label_style = {'font': ('Helvetica', 12)}

    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Organizer")

        self.create_widgets()

    def create_widgets(self):
        self.root.geometry("400x200")

        # Styles
        button_style = {'font': ('Helvetica', 12), 'padx': 10, 'pady': 5}

        # Select Folder Button
        self.select_folder_button = tk.Button(self.root, text="Select Folder", command=self.select_folder, **button_style)
        self.select_folder_button.pack(pady=(20, 0))

        # Organize Button
        self.organize_button = tk.Button(self.root, text="Organize", command=self.organize_files, **button_style)
        self.organize_button.pack(pady=20)

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        self.show_message(f"Selected Folder: {self.folder_path}")

    def organize_files(self):
        if not hasattr(self, 'folder_path'):
            self.show_message("Please select a folder first.")
            return

        for filename in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, filename)

            if os.path.isfile(file_path):
                file_type = filename.split('.')[-1]
                target_folder = os.path.join(self.folder_path, file_type.upper() + " Files")

                if not os.path.exists(target_folder):
                    os.mkdir(target_folder)

                shutil.move(file_path, os.path.join(target_folder, filename))

        self.show_message("Files organized successfully.")

    def show_message(self, message):
        message_label = tk.Label(self.root, text=message, **self.label_style)
        message_label.pack(pady=20)
        self.root.after(3000, message_label.destroy)  # Display message for 3 seconds

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopOrganizerApp(root)
    root.mainloop()
