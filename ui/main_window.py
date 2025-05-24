import os
import io
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import tkinter.messagebox as messagebox
import webbrowser
from tkinter import filedialog
from PIL import Image, ImageFilter
from rembg import remove
from pathlib import Path

from config.settings import (
    APP_TITLE, 
    WINDOW_SIZE, 
    APPEARANCE_MODE, 
    COLOR_THEME,
    INPUT_FILETYPES,
    DEFAULT_OUTPUT_DIR
)
from ui.image_preview import ImagePreview
from ui.control_panel import ControlPanel

# Set theme
ctk.set_appearance_mode(APPEARANCE_MODE)
ctk.set_default_color_theme(COLOR_THEME)

class BGRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(WINDOW_SIZE)
        
        # Output directory for processed images
        self.output_directory = ""
        
        # Initialize UI components
        self.image_preview = None
        self.control_panel = None
        self.progress_bar = None
        self.output_label = None
        self.theme_switch = None
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        self._create_header()
        self._create_image_preview()
        self._create_buttons()
        self._create_control_panel()
        self._create_action_buttons()
        self._create_output_selection()
        self._create_progress_bar()
        self._create_theme_switch()
    
    def _create_header(self):
        """Create the application header"""
        ctk.CTkLabel(
            self, 
            text="🖼️ Background Remover", 
            font=("Arial", 24)
        ).pack(pady=10)
    
    def _create_image_preview(self):
        """Create the image preview component"""
        self.image_preview = ImagePreview(self)
    
    def _create_buttons(self):
        """Create the select images button"""
        ctk.CTkButton(
            self, 
            text="Select Images", 
            command=self.select_images
        ).pack(pady=10)
    
    def _create_control_panel(self):
        """Create the control panel component"""
        self.control_panel = ControlPanel(self)
    
    def _create_action_buttons(self):
        """Create the main action button"""
        ctk.CTkButton(
            self, 
            text="Remove Background", 
            command=self.remove_background
        ).pack(pady=20)
    
    def _create_output_selection(self):
        """Create output directory selection widgets"""
        ctk.CTkButton(
            self, 
            text="Choose Output Folder", 
            command=self.choose_output_directory
        ).pack(pady=5)
        
        self.output_label = ctk.CTkLabel(
            self, 
            text="Output: Not selected", 
            text_color="gray"
        )
        self.output_label.pack(pady=2)
    
    def _create_progress_bar(self):
        """Create and hide the progress bar"""
        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()  # Hide initially
    
    def _create_theme_switch(self):
        """Create the theme toggle switch"""
        self.theme_switch = ctk.CTkSwitch(
            self, 
            text="Dark Mode", 
            command=self.toggle_theme
        )
        self.theme_switch.pack(pady=5)
    
    def select_images(self):
        """Open file dialog to select images"""
        new_files = filedialog.askopenfilenames(filetypes=INPUT_FILETYPES)
        if new_files:
            self.image_preview.add_files(new_files)
    
    def choose_output_directory(self):
        """Choose output directory for processed images"""
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory = directory
            self.output_label.configure(text=f"Output: {directory}")
    
    def ensure_output_directory(self):
        """Ensure output directory is set. If not, prompt user or use default."""
        if not self.output_directory:
            response = messagebox.askyesno(
                "No Output Directory",
                f"No output directory selected.\nWould you like to use this default location?\n\n{DEFAULT_OUTPUT_DIR}"
            )
            if response:
                os.makedirs(DEFAULT_OUTPUT_DIR, exist_ok=True)
                self.output_directory = DEFAULT_OUTPUT_DIR
                self.output_label.configure(text=f"Output: {DEFAULT_OUTPUT_DIR}")
                return True
            else:
                self.choose_output_directory()
                return bool(self.output_directory)
        return True
    
    def toggle_theme(self):
        """Toggle between dark and light themes"""
        if self.theme_switch.get():
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def remove_background(self):
        """Main function to process selected images"""
        selected_files = self.image_preview.get_selected_files()
        
        if not selected_files:
            messagebox.showwarning(
                "⚠️ No Images Selected", 
                "Please select images to remove backgrounds."
            )
            return
        
        # Ensure output directory is set
        if not self.ensure_output_directory():
            return
        
        # Show progress bar
        self.progress_bar.pack()
        self.progress_bar.set(0)
        self.update_idletasks()
        
        # Get current settings
        settings = self.control_panel.get_current_settings()
        output_format = self.control_panel.get_output_format().lower()
        
        try:
            processed_count = 0
            total = len(selected_files)
            
            for i, file in enumerate(selected_files):
                try:
                    # Process single image
                    if self._process_single_image(file, settings, output_format):
                        processed_count += 1
                except Exception as e:
                    print(f"❌ Error processing {file}: {e}")
                    messagebox.showerror("❌ Processing Error", f"Failed to process {file}: {str(e)}")
                
                # Update progress
                self.progress_bar.set((i + 1) / total)
                self.update_idletasks()
            
            # Hide progress bar
            self.progress_bar.set(0)
            self.progress_bar.pack_forget()
            
            # Show results
            if processed_count > 0:
                messagebox.showinfo(
                    "Processing Complete", 
                    f"✅ Successfully processed {processed_count} out of {total} images."
                )
                webbrowser.open(self.output_directory)
            else:
                messagebox.showwarning(
                    "No Images Processed", 
                    "No images were processed successfully. Please check for errors."
                )
                
        except Exception as err:
            self.progress_bar.pack_forget()
            print(f"❌ Unexpected error: {err}")
            messagebox.showerror("Unexpected Error", f"❌ An unexpected error occurred: {str(err)}")
    
    def _process_single_image(self, file_path, settings, output_format):
        """Process a single image file"""
        try:
            # Read and remove background
            with open(file_path, 'rb') as f:
                input_data = f.read()
                output_data = remove(input_data)
            
            # Load processed image
            img = Image.open(io.BytesIO(output_data)).convert("RGBA")
            
            # Apply post-processing
            img = self._apply_post_processing(img, settings)
            
            # Generate output filename
            filename = os.path.splitext(os.path.basename(file_path))[0]
            out_path = os.path.join(self.output_directory, f"{filename}_no_bg.{output_format}")
            
            # Save processed image
            if output_format == "jpeg":
                # JPEG doesn't support transparency, convert to RGB with white background
                background = Image.new("RGB", img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
                img = background
            
            img.save(out_path, format=output_format.upper())
            return True
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return False
    
    def _apply_post_processing(self, img, settings):
        """Apply resize, smoothing, and upscaling to image"""
        # Resize
        if settings["resize_percent"] != 100:
            new_size = (
                int(img.width * settings["resize_percent"] / 100), 
                int(img.height * settings["resize_percent"] / 100)
            )
            img = img.resize(new_size, Image.LANCZOS)
        
        # Smooth edges
        if settings["smooth_edges"] > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=settings["smooth_edges"]))
        
        # Upscale
        if settings["upscale_factor"] > 1:
            new_size = (
                img.width * settings["upscale_factor"], 
                img.height * settings["upscale_factor"]
            )
            img = img.resize(new_size, Image.LANCZOS)
        
        return img