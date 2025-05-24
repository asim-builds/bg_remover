import customtkinter as ctk
from config.settings import (
    DEFAULT_SETTINGS, 
    SUPPORTED_FORMATS, 
    DEFAULT_FORMAT, 
    SLIDER_CONFIGS, 
    TOOLTIP_TEXTS
)
from ui.tooltip import HoverTooltip

class ControlPanel:
    def __init__(self, parent):
        self.parent = parent
        self.sliders = {}
        self.format_option = None
        self.use_default_checkbox = None
        self.create_controls()
    
    def create_controls(self):
        """Create all control widgets"""
        self._create_format_selector()
        self._create_default_settings_checkbox()
        self._create_sliders()
        self._toggle_default_settings()  # Apply initial state
    
    def _create_format_selector(self):
        """Create the output format selection dropdown"""
        format_frame = ctk.CTkFrame(self.parent)
        format_frame.pack(pady=5)
        
        format_label = ctk.CTkLabel(format_frame, text="Output Format:")
        format_label.pack(side="left", padx=(10, 2))
        
        info_button = ctk.CTkButton(
            format_frame, 
            text="ℹ", 
            width=20, 
            height=20, 
            fg_color="gray", 
            text_color="white"
        )
        info_button.pack(side="left", padx=2)
        HoverTooltip(info_button, TOOLTIP_TEXTS["format_info"])
        
        self.format_option = ctk.CTkOptionMenu(format_frame, values=SUPPORTED_FORMATS)
        self.format_option.set(DEFAULT_FORMAT)
        self.format_option.pack(side="left", padx=10)
    
    def _create_default_settings_checkbox(self):
        """Create the default settings checkbox"""
        default_frame = ctk.CTkFrame(self.parent)
        default_frame.pack(pady=10)
        
        self.use_default_checkbox = ctk.CTkCheckBox(
            default_frame, 
            text="Use Default Settings (Recommended)", 
            command=self._toggle_default_settings
        )
        self.use_default_checkbox.pack(side="left", padx=(10, 2))
        self.use_default_checkbox.select()  # Check by default
        
        default_info_button = ctk.CTkButton(
            default_frame, 
            text="ℹ", 
            width=20, 
            height=20, 
            fg_color="gray", 
            text_color="white"
        )
        default_info_button.pack(side="left", padx=2)
        HoverTooltip(default_info_button, TOOLTIP_TEXTS["default_settings"])
    
    def _create_sliders(self):
        """Create all sliders based on configuration"""
        for key, config in SLIDER_CONFIGS.items():
            slider = self._create_slider(
                config["label"],
                config["from_"],
                config["to"],
                DEFAULT_SETTINGS[key],
                config["tooltip"]
            )
            self.sliders[key] = slider
    
    def _create_slider(self, label_text, from_, to, default, tooltip_text):
        """Create a single slider with label and tooltip"""
        frame = ctk.CTkFrame(self.parent)
        frame.pack(pady=5)
        
        label = ctk.CTkLabel(frame, text=f"{label_text}: {default}")
        label.pack(side="left", padx=(10, 2))
        
        # Info button with tooltip
        info_button = ctk.CTkButton(
            frame, 
            text="ℹ", 
            width=20, 
            height=20, 
            fg_color="gray", 
            text_color="white"
        )
        info_button.pack(side="left", padx=2)
        HoverTooltip(info_button, tooltip_text)
        
        # Slider
        slider = ctk.CTkSlider(
            frame, 
            from_=from_, 
            to=to, 
            number_of_steps=(to - from_), 
            orientation="horizontal"
        )
        slider.set(default)
        slider.pack(side="left", padx=10)
        
        # Update label when slider changes
        def update_label(value):
            label.configure(text=f"{label_text}: {int(value)}")
        slider.configure(command=update_label)
        
        # Store references for enabling/disabling
        slider.parent_frame = frame
        slider.label = label
        
        return slider
    
    def _toggle_default_settings(self):
        """Enable/disable sliders based on default checkbox state"""
        use_default = self.use_default_checkbox.get()
        
        if use_default:
            # Set to default values and disable sliders
            for key, slider in self.sliders.items():
                default_value = DEFAULT_SETTINGS[key]
                slider.set(default_value)
                
                # Update label
                config = SLIDER_CONFIGS[key]
                slider.label.configure(text=f"{config['label']}: {default_value}")
                
                # Disable slider
                slider.configure(state="disabled")
                slider.parent_frame.configure(fg_color=("#3B3B3B", "#2B2B2B"))
        else:
            # Enable sliders
            for slider in self.sliders.values():
                slider.configure(state="normal")
                slider.parent_frame.configure(fg_color=("gray75", "gray25"))
    
    def get_current_settings(self):
        """Get current settings based on checkbox state"""
        if self.use_default_checkbox.get():
            return DEFAULT_SETTINGS.copy()
        else:
            return {
                key: int(slider.get()) 
                for key, slider in self.sliders.items()
            }
    
    def get_output_format(self):
        """Get the selected output format"""
        return self.format_option.get()
    
    def is_using_defaults(self):
        """Check if using default settings"""
        return self.use_default_checkbox.get()