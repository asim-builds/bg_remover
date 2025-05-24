import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

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
        self.format_option.set("PNG")
        self.format_option.pack(side="left", padx=10)

        # Sliders
        self.smooth_slider = self.create_slider("Smooth Edges", 0, 5, 1)
        self.resize_slider = self.create_slider("Resize Image (%)", 10, 200, 100)
        self.upscale_slider = self.create_slider("Upscale Factor", 1, 4, 1)

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
            "Smooth Edges": "Smooths out jagged edges left after removing the background. Example: 2 = light smoothing.",
            "Resize Image (%)": "Scales the final image. 100 = same size, 150 = 1.5× bigger.",
            "Upscale Factor": "Uses AI to enhance resolution. Example: 2 = double the image resolution."
        }
        HoverTooltip(info_button, tooltip_texts.get(label_text, "Info not available."))

        slider = ctk.CTkSlider(frame, from_=from_, to=to, number_of_steps=(to - from_), orientation="horizontal")
        slider.set(default)
        slider.pack(side="left", padx=10)

        def update_label(value):
            label.configure(text=f"{label_text}: {int(value)}")
        slider.configure(command=update_label)

        return slider

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
        # This will be implemented in the next step
        print("Removing background with settings:")
        print("Smooth edges:", int(self.smooth_slider.get()))
        print("Resize image:", int(self.resize_slider.get()))
        print("Upscale factor:", int(self.upscale_slider.get()))
        print("Output format:", self.format_option.get())

if __name__ == "__main__":
    app = BGRemoverApp()
    app.mainloop()