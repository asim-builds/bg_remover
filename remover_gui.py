import os
import io
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
from rembg import remove

# Import the tooltip class from the separate file
from tooltip import HoverTooltip

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class BGRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Background Remover Pro")
        self.geometry("1000x800")
        self.selected_files = []
        
        # Default values for background removal (file format is separate)
        self.default_values = {
            "smooth_edges": 0,      # No smoothing by default (cleaner results)
            "resize_percent": 100,  # Keep original size
            "upscale_factor": 1     # No upscaling by default
        }

        self.init_ui()

    def init_ui(self):
        ctk.CTkLabel(self, text="🖼️ Background Remover", font=("Arial", 24)).pack(pady=10)

        self.preview_frame = ctk.CTkScrollableFrame(self, height=300)
        self.preview_frame.pack(padx=10, pady=10, fill="both", expand=False)

        ctk.CTkButton(self, text="Select Images", command=self.select_images).pack(pady=10)

        # Output format dropdown
        format_frame = ctk.CTkFrame(self)
        format_frame.pack(pady=5)

        format_label = ctk.CTkLabel(format_frame, text="Output Format:")
        format_label.pack(side="left", padx=(10, 2))

        info_button = ctk.CTkButton(format_frame, text="ℹ️", width=20, height=20, fg_color="gray", text_color="white")
        info_button.pack(side="left", padx=2)
        HoverTooltip(info_button, "Choose the output file format.\nPNG keeps transparency, JPEG doesn't.")

        self.format_option = ctk.CTkOptionMenu(format_frame, values=["PNG", "JPEG", "WEBP"])
        self.format_option.set("PNG")  # PNG as default (but user can change this)
        self.format_option.pack(side="left", padx=10)

        # Default settings checkbox
        default_frame = ctk.CTkFrame(self)
        default_frame.pack(pady=10)

        self.use_default_checkbox = ctk.CTkCheckBox(
            default_frame, 
            text="Use Default Settings (Recommended)", 
            command=self.toggle_default_settings
        )
        self.use_default_checkbox.pack(side="left", padx=(10, 2))
        self.use_default_checkbox.select()  # Check by default

        default_info_button = ctk.CTkButton(default_frame, text="ℹ️", width=20, height=20, fg_color="gray", text_color="white")
        default_info_button.pack(side="left", padx=2)
        HoverTooltip(default_info_button, "Uses optimal settings for background removal:\n• No smoothing (cleaner edges)\n• Original size maintained\n• No upscaling\n• Format selection remains independent")

        # Sliders
        self.smooth_slider = self.create_slider("Smooth Edges", 0, 5, self.default_values["smooth_edges"])
        self.resize_slider = self.create_slider("Resize Image (%)", 10, 200, self.default_values["resize_percent"])
        self.upscale_slider = self.create_slider("Upscale Factor", 1, 4, self.default_values["upscale_factor"])

        # Initially disable sliders if default is checked
        self.toggle_default_settings()

        # Remove button
        ctk.CTkButton(self, text="Remove Background", command=self.remove_background).pack(pady=20)

    def create_slider(self, label_text, from_, to, default):
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5)

        label = ctk.CTkLabel(frame, text=f"{label_text}: {default}")
        label.pack(side="left", padx=(10, 2))

        # ℹ️ Button
        info_button = ctk.CTkButton(frame, text="ℹ️", width=20, height=20, fg_color="gray", text_color="white")
        info_button.pack(side="left", padx=2)

        tooltip_texts = {
            "Smooth Edges": "Smooths out jagged edges after removing background.\n0 = No smoothing (recommended)\n2 = Light smoothing\n5 = Heavy smoothing",
            "Resize Image (%)": "Scales the final image size.\n100 = Original size (recommended)\n150 = 1.5× bigger\n50 = Half size",
            "Upscale Factor": "Uses AI to enhance resolution.\n1 = No upscaling (recommended)\n2 = Double resolution\n4 = Quadruple resolution"
        }
        HoverTooltip(info_button, tooltip_texts.get(label_text, "Info not available."))

        slider = ctk.CTkSlider(frame, from_=from_, to=to, number_of_steps=(to - from_), orientation="horizontal")
        slider.set(default)
        slider.pack(side="left", padx=10)

        def update_label(value):
            label.configure(text=f"{label_text}: {int(value)}")
        slider.configure(command=update_label)

        # Store reference to frame for enabling/disabling
        slider.parent_frame = frame
        slider.label = label

        return slider

    def toggle_default_settings(self):
        """Enable/disable sliders based on default checkbox state"""
        use_default = self.use_default_checkbox.get()
        
        sliders = [self.smooth_slider, self.resize_slider, self.upscale_slider]
        
        if use_default:
            # Set to default values and disable sliders
            self.smooth_slider.set(self.default_values["smooth_edges"])
            self.resize_slider.set(self.default_values["resize_percent"])
            self.upscale_slider.set(self.default_values["upscale_factor"])
            # Note: format_option is NOT reset - user choice is preserved
            
            # Update labels
            self.smooth_slider.label.configure(text=f"Smooth Edges: {self.default_values['smooth_edges']}")
            self.resize_slider.label.configure(text=f"Resize Image (%): {self.default_values['resize_percent']}")
            self.upscale_slider.label.configure(text=f"Upscale Factor: {self.default_values['upscale_factor']}")
            
            # Disable sliders by changing their appearance
            for slider in sliders:
                slider.configure(state="disabled")
                # Make the frame look disabled
                slider.parent_frame.configure(fg_color=("#3B3B3B", "#2B2B2B"))
            
            # Format option remains enabled - user can always change it
            
        else:
            # Enable sliders
            for slider in sliders:
                slider.configure(state="normal")
                # Restore normal frame appearance
                slider.parent_frame.configure(fg_color=("gray75", "gray25"))
            
            # Format option is always enabled

    def get_current_settings(self):
        """Get current settings based on checkbox state"""
        if self.use_default_checkbox.get():
            return {
                "smooth_edges": self.default_values["smooth_edges"],
                "resize_percent": self.default_values["resize_percent"],
                "upscale_factor": self.default_values["upscale_factor"]
            }
        else:
            return {
                "smooth_edges": int(self.smooth_slider.get()),
                "resize_percent": int(self.resize_slider.get()),
                "upscale_factor": int(self.upscale_slider.get())
            }

    def select_images(self):
        filetypes = [("Image files", "*.png *.jpg *.jpeg")]
        new_files = filedialog.askopenfilenames(filetypes=filetypes)

        for file in new_files:
            if file not in self.selected_files:
                self.selected_files.append(file)

        self.display_thumbnails()

    def display_thumbnails(self):
        for widget in self.preview_frame.winfo_children():
            widget.destroy()

        for file in self.selected_files:
            container = ctk.CTkFrame(self.preview_frame, width=160, height=180)
            container.pack_propagate(False)
            container.pack(side="left", padx=10, pady=10)

            img = Image.open(file).convert("RGB")
            img.thumbnail((140, 140))
            img_tk = ImageTk.PhotoImage(img)

            img_label = ctk.CTkLabel(container, image=img_tk, text="")
            img_label.image = img_tk
            img_label.pack()

            name = os.path.basename(file)
            name_label = ctk.CTkLabel(container, text=name, font=("Arial", 10))
            name_label.pack(pady=2)

            remove_btn = ctk.CTkButton(
                container,
                text="❌",
                width=20,
                height=20,
                fg_color="red",
                text_color="white",
                command=lambda f=file: self.remove_image(f)
            )
            remove_btn.place(relx=1.0, rely=0.0, anchor="ne")

    def remove_image(self, file):
        if file in self.selected_files:
            self.selected_files.remove(file)
        self.display_thumbnails()

    def remove_background(self):
        if not self.selected_files:
            ctk.CTkMessageBox.show_error("⚠️ No Images Selected", "Please select images to remove backgrounds.")
            return
        
        settings = self.get_current_settings()

        output_format = self.format_option.get().lower()
        output_dir = "output_images"

        os.makedirs(output_dir, exist_ok=True)

        for file in self.selected_files:
            try:
                with open(file, 'rb') as f:
                    input_data = f.read()
                    output_data = remove(input_data)
                
                # Open as a PIL image
                img = Image.open(io.BytesIO(output_data)).convert("RGBA")

                # Resize if needed
                if settings["resize_percent"] != 100:
                    new_size = (int(img.width * settings["resize_percent"] / 100), 
                                int(img.height * settings["resize_percent"] / 100))
                    img = img.resize(new_size, Image.LANCZOS)
                
                # Smooth edges if enabled
                if settings["smooth_edges"] > 0:
                    img = img.filter(ImageFilter.GaussianBlur(radius=settings["smooth_edges"]))

                # Upscale if needed
                if settings["upscale_factor"] > 1:
                    new_size = (img.width * settings["upscale_factor"], img.height * settings["upscale_factor"])
                    img = img.resize(new_size, Image.LANCZOS)

                # Save in the selected format
                filename = os.path.splitext(os.path.basename(file))[0]
                out_path = os.path.join(output_dir, f"{filename}_no_bg.{output_format}")
                img.save(out_path, format=output_format.upper())
                print(f"✅ Processed: {file} -> {out_path}")
            except Exception as e:
                print(f"❌ Error processing {file}: {e}")

if __name__ == "__main__":
    app = BGRemoverApp()
    app.mainloop()