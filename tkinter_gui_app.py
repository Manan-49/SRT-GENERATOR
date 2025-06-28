#!/usr/bin/env python3
"""
Modern Desktop GUI Application for Automatic Subtitle Generator
Built with CustomTkinter for a modern, responsive design
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import threading
from pathlib import Path
import sys
import webbrowser
from PIL import Image, ImageTk

# Import your subtitle generator class
try:
    from app import SubtitleGenerator
except ImportError:
    def show_import_error():
        root = ctk.CTk()
        root.withdraw()
        messagebox.showerror("Import Error", 
                           "Could not import SubtitleGenerator from app.py\n"
                           "Make sure app.py is in the same directory as this GUI script.")
        sys.exit(1)
    show_import_error()

# Configure CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class ModernSubtitleGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Subtitle Generator - Unimax Studios")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.video_path = ctk.StringVar()
        self.output_path = ctk.StringVar()
        self.model_type = ctk.StringVar(value="default")
        self.language = ctk.StringVar(value="en")
        self.custom_model_path = ctk.StringVar()
        self.keep_audio = ctk.BooleanVar()
        self.processing = False
        
        # Initialize subtitle generator
        self.generator = None
        
        # Set up the GUI
        self.setup_gui()
        
        # Load default model
        self.load_model()
    
    def setup_gui(self):
        """Set up the modern GUI layout"""
        # Main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title Section
        self.create_title_section()
        
        # Input Section
        self.create_input_section()
        
        # Model Selection Section
        self.create_model_section()
        
        # Options Section
        self.create_options_section()
        
        # Action Buttons Section
        self.create_action_section()
        
        # Progress Section
        self.create_progress_section()
        
        # Log Section
        self.create_log_section()
        
        # Set default paths
        self.set_default_paths()
    
    def create_title_section(self):
        """Create title section with app name and description"""
        title_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        title_frame.pack(fill="x", pady=(0, 10))  # Reduced outer padding
        
        # App Title
        title_label = ctk.CTkLabel(
            title_frame, 
            text="🎬 Subtitle Generator",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=28, weight="bold"),
            text_color=("#2b2b2b", "#f0f0f0")
        )
        title_label.pack(pady=(5, 0))  # Reduced top padding
        
        # Subtitle
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Generate accurate subtitles from videos using Vosk speech recognition",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color=("#555555", "#cccccc")
        )
        subtitle_label.pack(pady=(2, 5))  # Reduced padding below subtitle
        
        # Credits frame
        credits_frame = ctk.CTkFrame(
            title_frame,
            fg_color=("#f0f0f0", "#2b2b2b"),
            corner_radius=8,
            height=48  # Slightly reduced height
        )
        credits_frame.pack(fill="x", pady=(0, 0))  # Removed vertical padding
        credits_frame.pack_propagate(False)
        
        credits_container = ctk.CTkFrame(credits_frame, fg_color="transparent")
        credits_container.pack(expand=True, padx=10)
        
        credits_line = ctk.CTkFrame(credits_container, fg_color="transparent")
        credits_line.pack(expand=True)
        
        # Made with love section
        made_label = ctk.CTkLabel(
            credits_line,
            text="Made with ❤️ by ",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#666666", "#aaaaaa")
        )
        made_label.pack(side="left", padx=(0, 0))
        
        manan_link = ctk.CTkLabel(
            credits_line,
            text="@manan_ae",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=12, underline=True),
            text_color=("#1E90FF", "#00BFFF"),
            cursor="hand2"
        )
        manan_link.pack(side="left", padx=(0, 0))
        manan_link.bind("<Button-1>", lambda e: webbrowser.open("https://instagram.com/manan_ae"))
        
        separator = ctk.CTkLabel(
            credits_line,
            text=" • ",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#888888", "#777777")
        )
        separator.pack(side="left", padx=(5, 5))
        
        powered_label = ctk.CTkLabel(
            credits_line,
            text="Powered by ",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color=("#666666", "#aaaaaa")
        )
        powered_label.pack(side="left", padx=(0, 0))
        
        studio_link = ctk.CTkLabel(
            credits_line,
            text="Unimax Studios",
            font=ctk.CTkFont(family="Segoe UI Semibold", size=12, underline=True),
            text_color=("#1E90FF", "#00BFFF"),
            cursor="hand2"
        )
        studio_link.pack(side="left", padx=(0, 0))
        studio_link.bind("<Button-1>", lambda e: webbrowser.open("https://instagram.com/unimax.studios"))        
    
    def create_input_section(self):
        """Create video input section"""
        input_frame = ctk.CTkFrame(self.main_container)
        input_frame.pack(fill="x", pady=(0, 15))
        
        # Video File Selection
        video_label = ctk.CTkLabel(input_frame, text="Video File:", font=ctk.CTkFont(size=14, weight="bold"))
        video_label.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        
        video_entry_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        video_entry_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))
        video_entry_frame.columnconfigure(0, weight=1)
        
        self.video_entry = ctk.CTkEntry(
            video_entry_frame, 
            textvariable=self.video_path,
            placeholder_text="Select a video file...",
            height=40
        )
        self.video_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        browse_video_btn = ctk.CTkButton(
            video_entry_frame,
            text="Browse",
            width=100,
            height=40,
            command=self.browse_video
        )
        browse_video_btn.grid(row=0, column=1)
        
        # Output File Selection
        output_label = ctk.CTkLabel(input_frame, text="Output SRT File:", font=ctk.CTkFont(size=14, weight="bold"))
        output_label.grid(row=2, column=0, sticky="w", padx=20, pady=(10, 5))
        
        output_entry_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        output_entry_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 15))
        output_entry_frame.columnconfigure(0, weight=1)
        
        self.output_entry = ctk.CTkEntry(
            output_entry_frame,
            textvariable=self.output_path,
            placeholder_text="Output subtitle file path...",
            height=40
        )
        self.output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        browse_output_btn = ctk.CTkButton(
            output_entry_frame,
            text="Browse",
            width=100,
            height=40,
            command=self.browse_output
        )
        browse_output_btn.grid(row=0, column=1)
        
        input_frame.columnconfigure(0, weight=1)
    
    def create_model_section(self):
        """Create model selection section"""
        model_frame = ctk.CTkFrame(self.main_container)
        model_frame.pack(fill="x", pady=(0, 15))
        
        model_label = ctk.CTkLabel(
            model_frame, 
            text="Speech Recognition Model:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        model_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Model Type Selection
        model_selection_frame = ctk.CTkFrame(model_frame, fg_color="transparent")
        model_selection_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Default Models Radio Buttons
        default_radio = ctk.CTkRadioButton(
            model_selection_frame,
            text="Default Models",
            variable=self.model_type,
            value="default",
            command=self.on_model_type_change
        )
        default_radio.grid(row=0, column=0, sticky="w", padx=(0, 30))
        
        # Language Selection for Default Models
        self.language_frame = ctk.CTkFrame(model_selection_frame, fg_color="transparent")
        self.language_frame.grid(row=0, column=1, sticky="w")
        
        english_radio = ctk.CTkRadioButton(
            self.language_frame,
            text="English",
            variable=self.language,
            value="en",
            command=self.on_language_change
        )
        english_radio.grid(row=0, column=0, padx=(0, 20))
        
        hindi_radio = ctk.CTkRadioButton(
            self.language_frame,
            text="Hindi",
            variable=self.language,
            value="hi",
            command=self.on_language_change
        )
        hindi_radio.grid(row=0, column=1)
        
        # Custom Model Radio Button
        custom_radio = ctk.CTkRadioButton(
            model_selection_frame,
            text="Custom Model(Optional)",
            variable=self.model_type,
            value="custom",
            command=self.on_model_type_change
        )
        custom_radio.grid(row=1, column=0, sticky="w", pady=(10, 0))
        
        # Custom Model Path Entry
        self.custom_model_frame = ctk.CTkFrame(model_frame, fg_color="transparent")
        self.custom_model_frame.pack(fill="x", padx=20)
        self.custom_model_frame.columnconfigure(0, weight=1)
        
        self.custom_model_entry = ctk.CTkEntry(
            self.custom_model_frame,
            textvariable=self.custom_model_path,
            placeholder_text="Path to custom VOSK model folder...",
            height=40,
            state="disabled"
        )
        self.custom_model_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        self.browse_model_btn = ctk.CTkButton(
            self.custom_model_frame,
            text="Browse",
            width=100,
            height=40,
            command=self.browse_model,
            state="disabled"
        )
        self.browse_model_btn.grid(row=0, column=1)
        
        # Model Info
        model_info = ctk.CTkLabel(
            model_frame,
            text="Download more models from: ",
            font=ctk.CTkFont(size=12),
            text_color="white"
        )
        model_info.pack(anchor="w", padx=20, pady=(5, 0))

        link_label = ctk.CTkLabel(
            model_frame,
            text="https://alphacephei.com/vosk/models",
            font=ctk.CTkFont(size=12, underline=True),
            text_color="#00BFFF",  # light blue
            cursor="hand2"
        )
        link_label.pack(anchor="w", padx=20, pady=(0, 15))
        link_label.bind("<Button-1>", lambda e: webbrowser.open("https://alphacephei.com/vosk/models"))
    
    def create_options_section(self):
        """Create options section"""
        options_frame = ctk.CTkFrame(self.main_container)
        options_frame.pack(fill="x", pady=(0, 15))
        
        options_label = ctk.CTkLabel(
            options_frame,
            text="Options:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        options_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        keep_audio_check = ctk.CTkCheckBox(
            options_frame,
            text="Keep extracted audio file",
            variable=self.keep_audio
        )
        keep_audio_check.pack(anchor="w", padx=20, pady=(0, 15))
    
    def create_action_section(self):
        """Create action buttons section"""
        action_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 15))
        
        # Center the buttons
        button_container = ctk.CTkFrame(action_frame, fg_color="transparent")
        button_container.pack()
        
        self.generate_btn = ctk.CTkButton(
            button_container,
            text="Generate Subtitles",
            width=200,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_processing
        )
        self.generate_btn.grid(row=0, column=0, padx=10)
        
        clear_btn = ctk.CTkButton(
            button_container,
            text="Clear",
            width=120,
            height=45,
            fg_color="gray40",
            hover_color="gray50",
            command=self.clear_fields
        )
        clear_btn.grid(row=0, column=1, padx=10)
        
        open_folder_btn = ctk.CTkButton(
            button_container,
            text="Open Output Folder",
            width=150,
            height=45,
            fg_color="gray40",
            hover_color="gray50",
            command=self.open_output_folder
        )
        open_folder_btn.grid(row=0, column=2, padx=10)
    
    def create_progress_section(self):
        """Create progress section"""
        progress_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        progress_frame.pack(fill="x", pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=400)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            progress_frame,
            text="Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack()
    
    def create_log_section(self):
        """Create log section"""
        log_frame = ctk.CTkFrame(self.main_container)
        log_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        log_label = ctk.CTkLabel(
            log_frame,
            text="Processing Log:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        log_label.pack(anchor="w", padx=20, pady=(15, 10))
        
        self.log_text = ctk.CTkTextbox(
            log_frame,
            height=150,
            font=ctk.CTkFont(family="Consolas", size=12)
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))
    
    def set_default_paths(self):
        """Set default paths based on project structure"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try to find video file in video folder
        video_dir = os.path.join(script_dir, 'video')
        if os.path.exists(video_dir):
            video_files = [f for f in os.listdir(video_dir) 
                          if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv','.webm'))]
            if video_files:
                self.video_path.set(os.path.join(video_dir, video_files[0]))
        
        # Set default output path
        output_dir = os.path.join(script_dir, 'output')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        self.output_path.set(os.path.join(output_dir, "subtitles.srt"))
    
    def on_model_type_change(self):
        """Handle model type change"""
        if self.model_type.get() == "custom":
            self.custom_model_entry.configure(state="normal")
            self.browse_model_btn.configure(state="normal")
            self.language_frame.configure(fg_color="gray20")
            for widget in self.language_frame.winfo_children():
                widget.configure(state="disabled")
        else:
            self.custom_model_entry.configure(state="disabled")
            self.browse_model_btn.configure(state="disabled")
            self.language_frame.configure(fg_color="transparent")
            for widget in self.language_frame.winfo_children():
                widget.configure(state="normal")
        
        if not self.processing:
            self.load_model()
    
    def on_language_change(self):
        """Handle language change"""
        if not self.processing and self.model_type.get() == "default":
            self.load_model()
    
    def browse_video(self):
        """Browse for video file"""
        filetypes = [
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=filetypes
        )
        if filename:
            self.video_path.set(filename)
            # Auto-set output name based on video name
            video_stem = Path(filename).stem
            output_dir = os.path.dirname(self.output_path.get()) or "output"
            self.output_path.set(os.path.join(output_dir, f"{video_stem}_subtitles.srt"))
    
    def browse_output(self):
        """Browse for output location"""
        filename = filedialog.asksaveasfilename(
            title="Save Subtitle File As",
            defaultextension=".srt",
            filetypes=[("SRT files", "*.srt"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def browse_model(self):
        """Browse for custom model folder"""
        folder = filedialog.askdirectory(
            title="Select VOSK Model Folder"
        )
        if folder:
            self.custom_model_path.set(folder)
            if not self.processing:
                self.load_model()
    
    def clear_fields(self):
        """Clear all input fields"""
        if not self.processing:
            self.video_path.set("")
            self.output_path.set("")
            self.custom_model_path.set("")
            self.keep_audio.set(False)
            self.log_text.delete("1.0", "end")
            self.set_default_paths()
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_file = self.output_path.get()
        if output_file and os.path.exists(output_file):
            folder = os.path.dirname(output_file)
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            folder = os.path.join(script_dir, 'output')
        
        if os.path.exists(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                os.system(f"open '{folder}'")
            else:
                os.system(f"xdg-open '{folder}'")
    
    def log_message(self, message):
        """Add message to log area"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        self.root.update_idletasks()
    
    def load_model(self):
        """Load VOSK model based on selection with enhanced UI feedback"""
        try:
            self.log_message("Loading model...")
            self.status_label.configure(text="Loading model...")
            
            # Create a temporary loading dialog with credits
            loading_dialog = ctk.CTkToplevel(self.root)
            loading_dialog.title("Loading Model")
            loading_dialog.geometry("400x200")
            loading_dialog.transient(self.root)
            loading_dialog.grab_set()
            
            # Center the dialog
            loading_dialog.update_idletasks()
            x = (loading_dialog.winfo_screenwidth() // 2) - (400 // 2)
            y = (loading_dialog.winfo_screenheight() // 2) - (200 // 2)
            loading_dialog.geometry(f"400x200+{x}+{y}")
            
            # Main container
            main_frame = ctk.CTkFrame(loading_dialog, fg_color="#2b2b2b", corner_radius=12)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Loading content
            loading_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
            loading_frame.pack(expand=True, fill="both")
            
            # Loading spinner/text
            loading_label = ctk.CTkLabel(
                loading_frame,
                text="🔄 Loading Model...",
                font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
                text_color="#00BFFF"
            )
            loading_label.pack(pady=(20, 10))
            
            # Progress indicator
            progress_bar = ctk.CTkProgressBar(loading_frame, width=300, progress_color="#00BFFF")
            progress_bar.pack(pady=10)
            progress_bar.set(0.5)  # Indeterminate progress
            
            # Credits section (beautifully integrated)
            credits_frame = ctk.CTkFrame(
                loading_frame,
                fg_color="#1e1e1e",
                corner_radius=8,
                height=60
            )
            credits_frame.pack(fill="x", pady=(20, 10))
            credits_frame.pack_propagate(False)
            
            # Credits container
            credits_container = ctk.CTkFrame(credits_frame, fg_color="transparent")
            credits_container.pack(expand=True)
            
            # Single line credits
            credits_line = ctk.CTkFrame(credits_container, fg_color="transparent")
            credits_line.pack()
            
            made_label = ctk.CTkLabel(
                credits_line,
                text="Made with ❤️ by ",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color="#b0b0b0"
            )
            made_label.pack(side="left")
            
            manan_link = ctk.CTkLabel(
                credits_line,
                text="@manan_ae",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold", underline=True),
                text_color="#00BFFF",
                cursor="hand2"
            )
            manan_link.pack(side="left")
            manan_link.bind("<Button-1>", lambda e: webbrowser.open("https://instagram.com/manan_ae"))
            
            separator = ctk.CTkLabel(
                credits_line,
                text=" • ",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color="#707070"
            )
            separator.pack(side="left")
            
            powered_label = ctk.CTkLabel(
                credits_line,
                text="Powered by ",
                font=ctk.CTkFont(family="Segoe UI", size=12),
                text_color="#b0b0b0"
            )
            powered_label.pack(side="left")
            
            studio_link = ctk.CTkLabel(
                credits_line,
                text="Unimax Studios",
                font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold", underline=True),
                text_color="#00BFFF",
                cursor="hand2"
            )
            studio_link.pack(side="left")
            studio_link.bind("<Button-1>", lambda e: webbrowser.open("https://instagram.com/unimax.studios"))
            
            # Update the dialog
            loading_dialog.update()
            
            # Actual model loading logic
            if self.model_type.get() == "custom":
                model_path = self.custom_model_path.get()
                if not model_path:
                    loading_dialog.destroy()
                    self.log_message("Please select a custom model path")
                    self.status_label.configure(text="No custom model selected")
                    return
                
                # Update progress
                progress_bar.set(0.8)
                loading_label.configure(text="🔄 Loading Custom Model...")
                loading_dialog.update()
                
                self.generator = SubtitleGenerator(
                    vosk_model_path=model_path,
                    custom_model=True
                )
                self.log_message(f"Custom model loaded: {os.path.basename(model_path)}")
            else:
                # Update progress
                progress_bar.set(0.8)
                loading_label.configure(text="🔄 Loading Default Model...")
                loading_dialog.update()
                
                self.generator = SubtitleGenerator(language=self.language.get())
                model_name = "Hindi" if self.language.get() == "hi" else "English"
                self.log_message(f"Default {model_name} model loaded")
            
            # Complete loading
            progress_bar.set(1.0)
            loading_label.configure(text="✅ Model Loaded Successfully!", text_color="#00BFFF")
            loading_dialog.update()
            
            # Brief pause to show completion
            loading_dialog.after(1000, loading_dialog.destroy)
            
            self.status_label.configure(text="Ready - Model loaded")
            
        except Exception as e:
            # Close loading dialog if it exists
            try:
                loading_dialog.destroy()
            except:
                pass
                
            self.log_message(f"Error loading model: {str(e)}")
            self.status_label.configure(text="Error - Model not loaded")
            messagebox.showerror("Model Error", f"Failed to load VOSK model:\n{str(e)}")
    
    def validate_inputs(self):
        """Validate user inputs"""
        if not self.video_path.get():
            messagebox.showerror("Error", "Please select a video file")
            return False
        
        if not os.path.exists(self.video_path.get()):
            messagebox.showerror("Error", "Video file does not exist")
            return False
        
        if not self.output_path.get():
            messagebox.showerror("Error", "Please specify output location")
            return False
        
        if self.model_type.get() == "custom" and not self.custom_model_path.get():
            messagebox.showerror("Error", "Please select a custom model path")
            return False
        
        if not self.generator:
            messagebox.showerror("Error", "Model not loaded. Please select a model")
            return False
        
        return True
    
    def start_processing(self):
        """Start the subtitle generation process"""
        if self.processing:
            return
        
        if not self.validate_inputs():
            return
        
        # Start processing
        self.processing = True
        self.generate_btn.configure(text="Processing...", state="disabled")
        self.progress_bar.set(0)
        self.progress_bar.start()
        self.status_label.configure(text="Processing video...")
        
        # Clear log
        self.log_text.delete("1.0", "end")
        
        # Start processing thread
        thread = threading.Thread(target=self.process_video)
        thread.daemon = True
        thread.start()
    
    def update_progress(self, message):
        """Update progress from thread"""
        self.root.after(0, lambda: self.status_label.configure(text=message))
        self.root.after(0, lambda: self.log_message(message))
    
    def process_video(self):
        """Process video in background thread"""
        try:
            self.update_progress("Starting subtitle generation...")
            self.update_progress(f"Video: {os.path.basename(self.video_path.get())}")
            
            if self.model_type.get() == "custom":
                self.update_progress(f"Using custom model: {os.path.basename(self.custom_model_path.get())}")
            else:
                model_name = "Hindi" if self.language.get() == "hi" else "English"
                self.update_progress(f"Using default {model_name} model")
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(self.output_path.get())
            os.makedirs(output_dir, exist_ok=True)
            
            # Process the video with progress callback
            result_path = self.generator.process_video(
                video_path=self.video_path.get(),
                output_srt_path=self.output_path.get(),
                keep_audio=self.keep_audio.get(),
                progress_callback=self.update_progress
            )
            
            # Success
            self.root.after(0, self.processing_complete, result_path, None)
            
        except Exception as e:
            # Error
            self.root.after(0, self.processing_complete, None, str(e))
    
    def processing_complete(self, result_path, error):
        """Handle completion of processing"""
        self.processing = False
        self.progress_bar.stop()
        self.progress_bar.set(100 if not error else 0)
        self.generate_btn.configure(text="Generate Subtitles", state="normal")
        
        if error:
            self.log_message(f"Error: {error}")
            self.status_label.configure(text="Error occurred")
            messagebox.showerror("Processing Error", f"Failed to generate subtitles:\n{error}")
        else:
            self.log_message(f"Success! Subtitle file created: {result_path}")
            self.status_label.configure(text="Completed successfully")
            
            # Show success dialog
            result = messagebox.askyesno(
                "Success", 
                f"Subtitles generated successfully!\n\nFile: {os.path.basename(result_path)}\n\nWould you like to open the output folder?",
                icon="question"
            )
            if result:
                self.open_output_folder()
    
    
def main():
    """Main function to run the GUI application"""
    # Check if customtkinter is installed
    try:
        import customtkinter
    except ImportError:
        root = ctk.CTk()
        root.withdraw()
        messagebox.showerror(
            "Missing Dependency",
            "CustomTkinter is not installed.\n\n"
            "Please install it using:\n"
            "pip install customtkinter"
        )
        sys.exit(1)
    
    # Create and run the application
    root = ctk.CTk()
    app = ModernSubtitleGeneratorGUI(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Handle window closing
    def on_closing():
        if app.processing:
            if messagebox.askokcancel("Quit", "Processing is in progress. Do you want to quit anyway?"):
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()