import os
import customtkinter as ctk
from PIL import Image, ImageTk
from config.settings import PREVIEW_FRAME_HEIGHT, THUMBNAIL_SIZE, CONTAINER_SIZE

class ImagePreview:
    def __init__(self, parent):
        self.parent = parent
        self.preview_frame = None
        self.selected_files = []
        self.create_preview_frame()
    
    def create_preview_frame(self):
        """Create the scrollable preview frame"""
        self.preview_frame = ctk.CTkScrollableFrame(self.parent, height=PREVIEW_FRAME_HEIGHT)
        self.preview_frame.pack(padx=10, pady=10, fill="both", expand=False)
    
    def add_files(self, new_files):
        """Add new files to the selection, avoiding duplicates"""
        for file in new_files:
            if file not in self.selected_files:
                self.selected_files.append(file)
        self.display_thumbnails()
    
    def remove_file(self, file):
        """Remove a file from the selection"""
        if file in self.selected_files:
            self.selected_files.remove(file)
        self.display_thumbnails()
    
    def get_selected_files(self):
        """Return the list of selected files"""
        return self.selected_files.copy()
    
    def clear_files(self):
        """Clear all selected files"""
        self.selected_files.clear()
        self.display_thumbnails()
    
    def display_thumbnails(self):
        """Display thumbnails for all selected images"""
        # Clear existing thumbnails
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        # Create thumbnails for each file
        for file in self.selected_files:
            self._create_thumbnail(file)
    
    def _create_thumbnail(self, file):
        """Create a single thumbnail container"""
        container = ctk.CTkFrame(
            self.preview_frame, 
            width=CONTAINER_SIZE["width"], 
            height=CONTAINER_SIZE["height"]
        )
        container.pack_propagate(False)
        container.pack(side="left", padx=10, pady=10)
        
        # Load and resize image
        try:
            img = Image.open(file).convert("RGB")
            img.thumbnail(THUMBNAIL_SIZE)
            img_tk = ImageTk.PhotoImage(img)
            
            # Image label
            img_label = ctk.CTkLabel(container, image=img_tk, text="")
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.pack()
            
            # Filename label
            name = os.path.basename(file)
            name_label = ctk.CTkLabel(container, text=name, font=("Arial", 10))
            name_label.pack(pady=2)
            
            # Remove button
            remove_btn = ctk.CTkButton(
                container,
                text="❌",
                width=20,
                height=20,
                fg_color="red",
                text_color="white",
                command=lambda f=file: self.remove_file(f)
            )
            remove_btn.place(relx=1.0, rely=0.0, anchor="ne")
            
        except Exception as e:
            # If image can't be loaded, show error in container
            error_label = ctk.CTkLabel(
                container, 
                text=f"Error loading:\n{os.path.basename(file)}", 
                font=("Arial", 10),
                text_color="red"
            )
            error_label.pack(expand=True)
    
    def get_frame(self):
        """Return the preview frame widget"""
        return self.preview_frame