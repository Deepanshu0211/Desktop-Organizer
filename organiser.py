import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
from datetime import datetime
import threading

class DesktopOrganizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Organizer Pro")
        self.root.geometry("600x500")
        self.root.configure(bg="#2d2d2d")
        
        # Set dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TButton', background='#3d3d3d', foreground='white', borderwidth=1)
        self.style.map('TButton', background=[('active', '#4d4d4d')])
        self.style.configure('TLabel', background='#2d2d2d', foreground='white')
        self.style.configure('TProgressbar', background='#007acc', troughcolor='#2d2d2d')
        
        self.folder_path = None
        self.custom_categories = {}
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # App title
        title_label = ttk.Label(main_frame, text="Desktop Organizer Pro", font=('Helvetica', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Select Folder Frame
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)
        
        self.folder_path_var = tk.StringVar()
        folder_label = ttk.Label(folder_frame, text="Selected Folder:", font=('Helvetica', 10))
        folder_label.pack(side=tk.LEFT, padx=(0, 10))
        
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_path_var, width=40)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        select_btn = ttk.Button(folder_frame, text="Browse", command=self.select_folder)
        select_btn.pack(side=tk.RIGHT)
        
        # Options Frame
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Left side - Organizing options
        left_frame = ttk.Frame(options_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        options_label = ttk.Label(left_frame, text="Organizing Options", font=('Helvetica', 12, 'bold'))
        options_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Organizing methods
        self.org_method = tk.StringVar(value="extension")
        methods = [
            ("By File Extension", "extension"),
            ("By File Type (Documents, Media, etc.)", "type"),
            ("By Creation Date", "date")
        ]
        
        for text, value in methods:
            rb = ttk.Radiobutton(left_frame, text=text, value=value, variable=self.org_method)
            rb.pack(anchor=tk.W, pady=5)
        
        # Additional options
        self.create_subfolders = tk.BooleanVar(value=True)
        subfolder_check = ttk.Checkbutton(left_frame, text="Create subfolders for better organization", 
                                         variable=self.create_subfolders)
        subfolder_check.pack(anchor=tk.W, pady=5)
        
        self.keep_original_names = tk.BooleanVar(value=True)
        names_check = ttk.Checkbutton(left_frame, text="Keep original filenames", 
                                    variable=self.keep_original_names)
        names_check.pack(anchor=tk.W, pady=5)
        
        # Right side - Custom categories
        right_frame = ttk.Frame(options_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        custom_label = ttk.Label(right_frame, text="Custom Categories", font=('Helvetica', 12, 'bold'))
        custom_label.pack(anchor=tk.W, pady=(0, 10))
        
        self.custom_frame = ttk.Frame(right_frame)
        self.custom_frame.pack(fill=tk.BOTH, expand=True)
        
        add_custom_btn = ttk.Button(right_frame, text="+ Add Custom Category", command=self.add_custom_category)
        add_custom_btn.pack(pady=(10, 0), anchor=tk.W)
        
        # Status Frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=10)
        
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT)
        
        self.progress = ttk.Progressbar(status_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        
        # Action buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(20, 0))
        
        preview_btn = ttk.Button(button_frame, text="Preview Changes", command=self.preview_changes)
        preview_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        organize_btn = ttk.Button(button_frame, text="Organize Files", command=self.start_organize)
        organize_btn.pack(side=tk.LEFT)
        
        undo_btn = ttk.Button(button_frame, text="Undo Last Organization", command=self.undo_organization)
        undo_btn.pack(side=tk.RIGHT)
    
    def add_custom_category(self):
        """Add a custom category with file extensions"""
        popup = tk.Toplevel(self.root)
        popup.title("Add Custom Category")
        popup.geometry("400x200")
        popup.configure(bg="#2d2d2d")
        popup.transient(self.root)
        
        ttk.Label(popup, text="Category Name:").pack(pady=(20, 5), padx=20, anchor=tk.W)
        name_entry = ttk.Entry(popup, width=40)
        name_entry.pack(pady=5, padx=20, fill=tk.X)
        
        ttk.Label(popup, text="File Extensions (comma separated):").pack(pady=5, padx=20, anchor=tk.W)
        ext_entry = ttk.Entry(popup, width=40)
        ext_entry.pack(pady=5, padx=20, fill=tk.X)
        
        def save_category():
            name = name_entry.get().strip()
            extensions = [ext.strip().lower() for ext in ext_entry.get().split(',')]
            
            if name and extensions:
                self.custom_categories[name] = extensions
                self.update_custom_categories_display()
                popup.destroy()
        
        ttk.Button(popup, text="Save", command=save_category).pack(pady=20)
    
    def update_custom_categories_display(self):
        """Update the display of custom categories"""
        for widget in self.custom_frame.winfo_children():
            widget.destroy()
            
        if not self.custom_categories:
            ttk.Label(self.custom_frame, text="No custom categories defined").pack(anchor=tk.W)
            return
            
        for category, extensions in self.custom_categories.items():
            frame = ttk.Frame(self.custom_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=f"{category}: ").pack(side=tk.LEFT)
            ttk.Label(frame, text=", ".join(extensions)).pack(side=tk.LEFT)
            
            def make_delete_func(cat):
                return lambda: self.delete_category(cat)
                
            delete_btn = ttk.Button(frame, text="×", width=2, command=make_delete_func(category))
            delete_btn.pack(side=tk.RIGHT)
    
    def delete_category(self, category):
        """Delete a custom category"""
        if category in self.custom_categories:
            del self.custom_categories[category]
            self.update_custom_categories_display()
    
    def select_folder(self):
        """Select a folder to organize"""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path = folder
            self.folder_path_var.set(folder)
            self.status_var.set(f"Selected: {folder}")
    
    def preview_changes(self):
        """Preview organization changes without actually moving files"""
        if not self.folder_path:
            self.show_message("Please select a folder first")
            return
            
        preview = tk.Toplevel(self.root)
        preview.title("Preview Changes")
        preview.geometry("600x400")
        preview.configure(bg="#2d2d2d")
        
        ttk.Label(preview, text="Files will be organized as follows:", font=('Helvetica', 12, 'bold')).pack(pady=10)
        
        preview_text = tk.Text(preview, bg="#3d3d3d", fg="white", highlightthickness=0)
        preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(preview_text, command=preview_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        preview_text.config(yscrollcommand=scrollbar.set)
        
        files_by_destination = self.get_organization_plan()
        
        for dest, files in files_by_destination.items():
            preview_text.insert(tk.END, f"➤ {dest}:\n", "folder")
            for file in files:
                preview_text.insert(tk.END, f"  - {file}\n", "file")
            preview_text.insert(tk.END, "\n")
            
        preview_text.config(state=tk.DISABLED)
    
    def get_organization_plan(self):
        """Get a plan of how files will be organized"""
        files_by_destination = {}
        
        try:
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                
                if not os.path.isfile(file_path):
                    continue
                    
                destination = self.get_destination_folder(filename)
                
                if destination not in files_by_destination:
                    files_by_destination[destination] = []
                    
                files_by_destination[destination].append(filename)
                
        except Exception as e:
            self.show_message(f"Error: {str(e)}")
            
        return files_by_destination
    
    def get_destination_folder(self, filename):
        """Determine destination folder based on organizing method"""
        method = self.org_method.get()
        file_ext = filename.split('.')[-1].lower() if '.' in filename else 'unknown'
        
        # Check custom categories first
        for category, extensions in self.custom_categories.items():
            if file_ext in extensions:
                return category
        
        if method == "extension":
            return f"{file_ext.upper()} Files"
            
        elif method == "type":
            # Simplified file type categorization
            doc_types = ['pdf', 'doc', 'docx', 'txt', 'rtf', 'odt']
            image_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg']
            video_types = ['mp4', 'mov', 'avi', 'mkv', 'wmv', 'flv']
            audio_types = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a']
            
            if file_ext in doc_types:
                return "Documents"
            elif file_ext in image_types:
                return "Images"
            elif file_ext in video_types:
                return "Videos"
            elif file_ext in audio_types:
                return "Audio"
            else:
                return "Other Files"
                
        elif method == "date":
            try:
                file_path = os.path.join(self.folder_path, filename)
                creation_time = os.path.getctime(file_path)
                date_created = datetime.fromtimestamp(creation_time)
                return date_created.strftime("%Y-%m")
            except:
                return "Unknown Date"
        
        return "Other Files"
    
    def start_organize(self):
        """Start organizing files in a separate thread"""
        if not self.folder_path:
            self.show_message("Please select a folder first")
            return
            
        # Create backup directory for undo operation
        backup_dir = os.path.join(self.folder_path, ".organizer_backup")
        if not os.path.exists(backup_dir):
            os.mkdir(backup_dir)
            
        # Save organization state for undo
        with open(os.path.join(backup_dir, "state.txt"), "w") as f:
            f.write(f"Original folder: {self.folder_path}\n")
            f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # Start organizing in a thread to keep UI responsive
        threading.Thread(target=self.organize_files, daemon=True).start()
    
    def organize_files(self):
        """Organize files according to selected method"""
        try:
            self.status_var.set("Organizing files...")
            self.progress["value"] = 0
            
            files = [f for f in os.listdir(self.folder_path) 
                    if os.path.isfile(os.path.join(self.folder_path, f))]
            
            total_files = len(files)
            processed = 0
            
            # Create backup copies of files
            backup_dir = os.path.join(self.folder_path, ".organizer_backup")
            
            for filename in files:
                if filename.startswith('.'):  # Skip hidden files
                    continue
                    
                # Make backup copy
                src_path = os.path.join(self.folder_path, filename)
                backup_path = os.path.join(backup_dir, filename)
                shutil.copy2(src_path, backup_path)
                
                # Get destination folder
                dest_folder_name = self.get_destination_folder(filename)
                dest_folder = os.path.join(self.folder_path, dest_folder_name)
                
                # Create destination folder if it doesn't exist
                if not os.path.exists(dest_folder):
                    os.makedirs(dest_folder)
                
                # Move file
                dest_path = os.path.join(dest_folder, filename)
                shutil.move(src_path, dest_path)
                
                # Update progress
                processed += 1
                progress_value = int((processed / total_files) * 100)
                self.progress["value"] = progress_value
                
                # Update UI periodically
                if processed % 5 == 0 or processed == total_files:
                    self.status_var.set(f"Processed {processed}/{total_files} files...")
                    self.root.update_idletasks()
            
            self.status_var.set(f"Organization complete! {total_files} files organized.")
            self.progress["value"] = 100
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def undo_organization(self):
        """Undo the last organization operation"""
        backup_dir = os.path.join(self.folder_path, ".organizer_backup")
        
        if not os.path.exists(backup_dir):
            self.show_message("No previous organization to undo")
            return
            
        try:
            self.status_var.set("Undoing organization...")
            self.progress["value"] = 0
            
            backup_files = [f for f in os.listdir(backup_dir) 
                          if os.path.isfile(os.path.join(backup_dir, f)) and not f.startswith('.')]
            
            total_files = len(backup_files)
            processed = 0
            
            for filename in backup_files:
                if filename == "state.txt":  # Skip state file
                    continue
                    
                # Move file back to original location
                backup_path = os.path.join(backup_dir, filename)
                dest_path = os.path.join(self.folder_path, filename)
                
                shutil.copy2(backup_path, dest_path)
                
                # Update progress
                processed += 1
                progress_value = int((processed / total_files) * 100)
                self.progress["value"] = progress_value
                
                if processed % 5 == 0 or processed == total_files:
                    self.status_var.set(f"Restored {processed}/{total_files} files...")
                    self.root.update_idletasks()
            
            # Clean up folders created during organization
            self.status_var.set("Cleaning up folders...")
            self.cleanup_empty_folders()
            
            # Delete backup directory
            shutil.rmtree(backup_dir)
            
            self.status_var.set("Undo complete!")
            self.progress["value"] = 100
            
        except Exception as e:
            self.status_var.set(f"Error during undo: {str(e)}")
    
    def cleanup_empty_folders(self):
        """Remove empty folders created during organization"""
        for item in os.listdir(self.folder_path):
            folder_path = os.path.join(self.folder_path, item)
            
            if os.path.isdir(folder_path) and item != ".organizer_backup":
                if not os.listdir(folder_path):  # If folder is empty
                    try:
                        os.rmdir(folder_path)
                    except:
                        pass
    
    def show_message(self, message, duration=3000):
        """Show a temporary message"""
        self.status_var.set(message)
        self.root.after(duration, lambda: self.status_var.set("Ready"))

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopOrganizerApp(root)
    root.mainloop()