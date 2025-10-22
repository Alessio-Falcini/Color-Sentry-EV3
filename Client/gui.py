
import tkinter as tk
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    tk.messagebox.showerror(
        "Error", 
        "The Pillow library is not installed. Install it by running 'pip install pillow'."
    )
    raise
import socket
import threading

THEME_COLORS = {
    'campus_blue': "#1a3c6e",     # Dark blue
    'light_blue': "#3c78d8",      # Lighter blue
    'light_gray': "#f0f0f0",      # Light background
    'white': "#ffffff",           # White
    'text_gray': "#2c3e50",       # Text color
    'error_red': "#E74C3C",       # Error red
    'success_green': "#2ECC71"    # Success green
}

class AppOpenDay:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("LEGOEV3 Color Detection System")
        self.root.geometry("400x600")
        self.root.configure(bg=THEME_COLORS['light_gray'])
        
        # Base style for labels
        self.style_label = {
            'bg': THEME_COLORS['light_gray'],
            'fg': THEME_COLORS['text_gray'],
            'font': ('Helvetica', 12)
        }
        
        # Definition of detectable colors
        self.colors = {
            'RED':    "#E63946",  # Elegant red
            'BLUE':   "#1a3c6e",  # Campus blue 
            'BLACK':  "#2C3E50",  # Elegant black
            'GREEN':  "#2ECC71",  # Soft green
            'YELLOW': "#F1C40F",  # Soft yellow
            'WHITE':  "#ECF0F1"   # Soft white
        }
        
        self.setup_gui()
    
    def setup_gui(self):
        # Creation of the main frame
        main_frame = tk.Frame(self.root, bg=THEME_COLORS['light_gray'])
        main_frame.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Color display setup
        self.setup_color_display(main_frame)
        
        # Status and connection setup
        self.setup_connection_controls(main_frame)
    
    def setup_logo(self, main_frame):
        # Load the logo if available, otherwise show the title
        try:
            pil_image = Image.open("logo_campus.png")
            pil_image = pil_image.resize((300, 150))
            self.logo_image = ImageTk.PhotoImage(pil_image)
            tk.Label(main_frame, image=self.logo_image, 
                    bg=THEME_COLORS['light_gray']).pack(pady=15)
        except:
            tk.Label(main_frame, text="IIS Campus Leonardo da Vinci",
                    font=('Helvetica', 22, 'bold'),
                    fg=THEME_COLORS['campus_blue'],
                    bg=THEME_COLORS['light_gray']).pack(pady=15)
    
    def setup_color_display(self, main_frame):
        # Container for color display
        display_container = tk.Frame(main_frame, 
            bg=THEME_COLORS['light_gray'],
            pady=20)
        display_container.pack(fill='x')
        
        # Subtitle with improved style
        tk.Label(display_container,
            text="Color Detection System",
            font=('Helvetica', 16, 'bold'),
            fg=THEME_COLORS['campus_blue'],
            bg=THEME_COLORS['light_gray']).pack()
        
        # Decorative separator
        separator = tk.Frame(display_container,
            height=2,
            width=100,
            bg=THEME_COLORS['light_blue'])
        separator.pack(pady=10)
        
        # Color display with border and shadow
        color_container = tk.Frame(display_container,
            bg=THEME_COLORS['campus_blue'],
            bd=0,
            highlightthickness=1,
            highlightbackground=THEME_COLORS['light_blue'])
        color_container.pack(pady=20)
        
        self.color_display = tk.Frame(color_container,
            width=200,
            height=200,
            bg="gray")
        self.color_display.pack(padx=2, pady=2)
        self.color_display.pack_propagate(False)
    
    def setup_connection_controls(self, main_frame):
        # Central container to align everything
        center_frame = tk.Frame(main_frame, bg=THEME_COLORS['light_gray'])
        center_frame.pack(expand=True)
        
        # Status label with improved style and thin border
        status_frame = tk.Frame(center_frame, 
            bg=THEME_COLORS['white'],
            highlightbackground=THEME_COLORS['light_blue'],
            highlightthickness=1)
        status_frame.pack(pady=(15,5))
        
        self.status_label = tk.Label(status_frame, 
            text="Waiting for connection...",
            font=('Helvetica', 12, 'italic'),
            fg=THEME_COLORS['text_gray'],
            bg=THEME_COLORS['white'],
            pady=8,
            padx=20)
        self.status_label.pack()
        
        # IP Box
        ip_container = tk.Frame(center_frame, 
            bg=THEME_COLORS['white'],
            highlightbackground=THEME_COLORS['light_blue'],
            highlightthickness=1)
        ip_container.pack(pady=10)
        
        # Centered IP Label
        tk.Label(ip_container, 
            text="Robot IP Address",
            font=('Helvetica', 12, 'bold'),
            bg=THEME_COLORS['white'],
            fg=THEME_COLORS['campus_blue'],
            padx=20).pack(pady=(10,5))
        
        # IP Entry with modern style
        self.ip_entry = tk.Entry(ip_container,
            width=20,  # Reduced to be more compact
            font=('Helvetica', 11),
            bg=THEME_COLORS['light_gray'],
            fg=THEME_COLORS['text_gray'],
            relief='flat',
            justify='center',
            insertbackground=THEME_COLORS['campus_blue'])
        self.ip_entry.insert(0, "169.254.215.169")
        self.ip_entry.pack(pady=(0,10), ipady=5, padx=20)
        
        # Controls Box
        control_container = tk.Frame(center_frame, 
            bg=THEME_COLORS['white'],
            highlightbackground=THEME_COLORS['light_blue'],
            highlightthickness=1)
        control_container.pack(pady=(15,10))
        
        # Centered buttons frame
        btn_frame = tk.Frame(control_container, bg=THEME_COLORS['white'])
        btn_frame.pack(pady=15, padx=20)
        
        # Common style for buttons
        btn_style = {
            'font': ('Helvetica', 11, 'bold'),
            'fg': THEME_COLORS['white'],
            'relief': 'flat',
            'padx': 15,
            'pady': 8,
            'width': 12,
            'cursor': 'hand2'
        }
        
        # All buttons in one row
        self.btn_connect = tk.Button(btn_frame,
            text="Connect",
            bg=THEME_COLORS['campus_blue'],
            activebackground=THEME_COLORS['light_blue'],
            activeforeground=THEME_COLORS['white'],
            command=self.start_connection,
            **btn_style)
        self.btn_connect.pack(side=tk.LEFT, padx=5)
        
        self.btn_motor = tk.Button(btn_frame,
            text="Start Motors",
            bg=THEME_COLORS['campus_blue'],
            activebackground=THEME_COLORS['light_blue'],
            activeforeground=THEME_COLORS['white'],
            command=self.toggle_motor,
            state='disabled',
            **btn_style)
        self.btn_motor.pack(side=tk.LEFT, padx=5)
        
        self.btn_stop = tk.Button(btn_frame,
            text="Stop",
            bg="#E74C3C",
            activebackground="#C0392B",
            activeforeground=THEME_COLORS['white'],
            command=self.stop_program,
            state='disabled',
            **btn_style)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        
        # Hover effects for buttons
        for btn in [self.btn_connect, self.btn_motor, self.btn_stop]:
            btn.bind('<Enter>', lambda e, b=btn: self._on_enter(b))
            btn.bind('<Leave>', lambda e, b=btn: self._on_leave(b))
    
    def start_connection(self):
        # Start connection thread
        if not hasattr(self, 'thread_conn') or not self.thread_conn.is_alive():
            self.thread_conn = threading.Thread(target=self.connect_ev3)
            self.thread_conn.daemon = True
            self.thread_conn.start()
        
        # After enabling controls, also enable the motor button
        self.btn_motor.config(state='normal')
    
    def connect_ev3(self):
        # Manages connection to the robot
        self.status_label.config(text="Connecting...", fg=THEME_COLORS['light_blue'])
        try:
            self.client = socket.socket()
            self.client.settimeout(5)
            self.client.connect((self.ip_entry.get(), 12345))
            
            # Disable connect button
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Frame):
                            for btn in child.winfo_children():
                                if isinstance(btn, tk.Button) and btn['text'] == "Connect":
                                    btn.config(state='disabled')
            
            # Enable controls
            self.btn_stop.config(state='normal')
            self.btn_motor.config(state='normal')  # Enable motor button
            
            # Start program
            self.client.send("START".encode())
            self.status_label.config(text="Program started", fg=THEME_COLORS['campus_blue'])
            
            # Color reception loop
            while True:
                try:
                    color = self.client.recv(1024).decode()
                    if color in self.colors:
                        self.root.after(0, self.update_display, color)
                except socket.timeout:
                    continue  # Continue loop if no data
                except Exception as e:
                    print(f"Reception error: {e}")
                    break
                
        except Exception as e:
            self.status_label.config(text=f"Errore: {str(e)}", fg='red')
            self.disconnect()
    
    def disconnect(self):
        # Handle disconnection
        if hasattr(self, 'client'):
            try:
                self.client.close()
            except:
                pass
        self.btn_stop.config(state='disabled')
        self.btn_motor.config(state='disabled', text="Start Motors", bg=THEME_COLORS['campus_blue'])
    
    def stop_program(self):
        # Stop the program
        try:
            self.client.send("STOP".encode())
            self.status_label.config(text="Program terminated", fg=THEME_COLORS['campus_blue'])
        except:
            pass
        finally:
            self.disconnect()
            self.root.quit()
    
    def update_display(self, color):
        # Update the color display
        self.color_display.config(bg=self.colors[color])
        self.status_label.config(text=f"Detected color: {color}", fg=THEME_COLORS['campus_blue'])
    
    def toggle_motor(self):
        try:
            if self.btn_motor['text'] == "Start Motors":
                self.client.send("START_MOTOR".encode())
                self.btn_motor.config(text="Stop Motors", bg="#E74C3C")
                self.status_label.config(text="Motors started", fg=THEME_COLORS['campus_blue'])
            else:
                self.client.send("STOP_MOTOR".encode())
                self.btn_motor.config(text="Start Motors", bg=THEME_COLORS['campus_blue'])
                self.status_label.config(text="Motors stopped", fg=THEME_COLORS['campus_blue'])
        except Exception as e:
            self.status_label.config(text=f"Motor control error: {str(e)}", fg='red')

    def _on_entry_focus_in(self, event):
        """Effect when entry receives focus"""
        event.widget.config(
            bg=THEME_COLORS['white'],
            highlightbackground=THEME_COLORS['light_blue'],
            highlightthickness=2
        )

    def _on_entry_focus_out(self, event):
        """Effect when entry loses focus"""
        event.widget.config(
            bg=THEME_COLORS['light_gray'],
            highlightthickness=0
        )

    def _on_enter(self, button):
        """Hover effect when mouse enters the button"""
        if button['state'] != 'disabled':
            button.config(relief='solid', highlightthickness=1)
            # Scale effect
            button.config(pady=7)  # Slightly smaller

    def _on_leave(self, button):
        """Hover effect when mouse leaves the button"""
        if button['state'] != 'disabled':
            button.config(relief='flat', highlightthickness=0)
            # Restore original size
            button.config(pady=8)

def main():
    # Main function
    root = tk.Tk()
    app = AppOpenDay(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
