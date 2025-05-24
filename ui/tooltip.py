import customtkinter as ctk

class HoverTooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        
        # Bind events to the widget
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
        widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        # Schedule tooltip to show after a short delay
        self.schedule_tooltip()

    def on_leave(self, event=None):
        # Cancel any scheduled tooltip and hide current one
        self.cancel_tooltip()
        self.hidetip()

    def on_motion(self, event=None):
        # Update mouse position
        self.x, self.y = event.x_root, event.y_root

    def schedule_tooltip(self):
        # Cancel any existing scheduled tooltip
        self.cancel_tooltip()
        # Schedule new tooltip to appear after 500ms
        self.id = self.widget.after(500, self.showtip)

    def cancel_tooltip(self):
        # Cancel scheduled tooltip
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None

    def showtip(self):
        if self.tipwindow or not self.text:
            return
            
        # Use stored mouse position, or fallback to widget position
        if hasattr(self, 'x') and hasattr(self, 'y'):
            x, y = self.x + 10, self.y + 10
        else:
            x = self.widget.winfo_rootx() + 20
            y = self.widget.winfo_rooty() + 20

        # Create tooltip window
        self.tipwindow = tw = ctk.CTkToplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        tw.attributes('-topmost', True)  # Keep tooltip on top
        
        # Make sure tooltip disappears when clicked or after timeout
        tw.bind("<Button-1>", self.hidetip)
        tw.bind("<FocusOut>", self.hidetip)
        
        # Create label with tooltip text
        label = ctk.CTkLabel(
            tw, 
            text=self.text, 
            justify='left', 
            wraplength=200, 
            fg_color="#333", 
            text_color="white", 
            padx=10, 
            pady=5, 
            corner_radius=5
        )
        label.pack()
        
        # Auto-hide tooltip after 5 seconds as a safety measure
        self.widget.after(5000, self.hidetip)

    def hidetip(self, event=None):
        if self.tipwindow:
            try:
                self.tipwindow.destroy()
            except:
                pass  # Window might already be destroyed
            self.tipwindow = None
