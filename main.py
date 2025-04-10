import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import threading


class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Image Converter")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="#2c3e50")

        # Default output folder (dynamic path based on OS)
        self.output_folder = os.path.join(os.path.expanduser("~"), "Pictures", "converted")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Load images for the interface
        self.load_images()

        # Create the user interface
        self.create_widgets()

        # Center the window on the screen
        self.center_window()

    def load_images(self):
        """Load images used in the interface"""
        try:
            self.logo_img = Image.open("logo.png") if os.path.exists("logo.png") else None
            if self.logo_img:
                self.logo_img = self.logo_img.resize((150, 150), Image.LANCZOS)
                self.logo_img = ImageTk.PhotoImage(self.logo_img)
            # Default logo if no logo image exists
            self.default_logo = self.create_default_logo()
        except Exception as e:
            print(f"Error loading images: {e}")
            self.default_logo = self.create_default_logo()

    def create_default_logo(self):
        """Create a default logo if none exists"""
        img = Image.new('RGB', (150, 150), color='#3498db')
        return ImageTk.PhotoImage(img)

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create the user interface widgets"""
        # Header frame
        header_frame = tk.Frame(self.root, bg="#3498db", height=180)
        header_frame.pack(fill=tk.X)

        # Logo
        logo_label = tk.Label(header_frame, image=self.logo_img if self.logo_img else self.default_logo,
                              bg="#3498db")
        logo_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Title
        title_label = tk.Label(header_frame, text="Professional Image Converter",
                               font=("Arial", 24, "bold"), fg="white", bg="#3498db")
        title_label.pack(side=tk.LEFT, padx=10, pady=40)

        # Content frame
        content_frame = tk.Frame(self.root, bg="#2c3e50")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Output path information
        path_info_frame = tk.Frame(content_frame, bg="#34495e", bd=2, relief=tk.GROOVE)
        path_info_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(path_info_frame, text="Converted Images Path:", font=("Arial", 10, "bold"),
                 fg="#ecf0f1", bg="#34495e").pack(side=tk.LEFT, padx=10, pady=5)
        self.output_path_label = tk.Label(path_info_frame, text=self.output_folder,
                                          font=("Arial", 10), fg="#bdc3c7", bg="#34495e",
                                          wraplength=500, justify=tk.LEFT)
        self.output_path_label.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        # Select destination folder
        dest_folder_frame = tk.Frame(content_frame, bg="#2c3e50")
        dest_folder_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(dest_folder_frame, text="Select Destination Folder:", font=("Arial", 12),
                 fg="#ecf0f1", bg="#2c3e50").pack(side=tk.LEFT, padx=(0, 10))
        self.dest_folder_path = tk.StringVar(value=self.output_folder)
        dest_folder_entry = tk.Entry(dest_folder_frame, textvariable=self.dest_folder_path,
                                     font=("Arial", 10), width=40, state='readonly')
        dest_folder_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        browse_dest_btn = tk.Button(dest_folder_frame, text="Browse...", command=self.browse_dest_folder,
                                    bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                                    relief=tk.FLAT, activebackground="#2980b9")
        browse_dest_btn.pack(side=tk.LEFT)

        # Folder selection
        folder_frame = tk.Frame(content_frame, bg="#2c3e50")
        folder_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(folder_frame, text="Select Source Folder:", font=("Arial", 12),
                 fg="#ecf0f1", bg="#2c3e50").pack(side=tk.LEFT, padx=(0, 10))
        self.folder_path = tk.StringVar()
        folder_entry = tk.Entry(folder_frame, textvariable=self.folder_path,
                                font=("Arial", 10), width=40, state='readonly')
        folder_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        browse_btn = tk.Button(folder_frame, text="Browse...", command=self.browse_folder,
                               bg="#3498db", fg="white", font=("Arial", 10, "bold"),
                               relief=tk.FLAT, activebackground="#2980b9")
        browse_btn.pack(side=tk.LEFT)

        # Progress bar
        progress_frame = tk.Frame(content_frame, bg="#2c3e50")
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        self.progress_label = tk.Label(progress_frame, text="Ready", font=("Arial", 10),
                                       fg="#ecf0f1", bg="#2c3e50")
        self.progress_label.pack(side=tk.TOP, anchor=tk.W)
        self.progress = ttk.Progressbar(progress_frame, orient=tk.HORIZONTAL,
                                        length=100, mode='determinate')
        self.progress.pack(fill=tk.X)

        # Statistics
        stats_frame = tk.Frame(content_frame, bg="#34495e", bd=2, relief=tk.GROOVE)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        tk.Label(stats_frame, text="Conversion Stats:", font=("Arial", 10, "bold"),
                 fg="#ecf0f1", bg="#34495e").pack(side=tk.LEFT, padx=10, pady=5)
        self.stats_label = tk.Label(stats_frame, text="0 Images Converted | 0 Success | 0 Fail",
                                    font=("Arial", 10), fg="#bdc3c7", bg="#34495e")
        self.stats_label.pack(side=tk.LEFT, padx=5, pady=5)

        # Convert button
        self.convert_btn = tk.Button(content_frame, text="Start Conversion", command=self.start_conversion,
                                     bg="#2ecc71", fg="white", font=("Arial", 14, "bold"),
                                     relief=tk.FLAT, activebackground="#27ae60",
                                     width=20, height=2)
        self.convert_btn.pack(pady=(10, 0))

        # Version info
        version_label = tk.Label(content_frame, text="Version 1.0 | © 2023 TechnoMaster",
                                 font=("Arial", 8), fg="#7f8c8d", bg="#2c3e50")
        version_label.pack(side=tk.BOTTOM, pady=(20, 0))

    def browse_folder(self):
        """Open a dialog to select the source folder"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.progress_label.config(text="Folder selected, ready to convert")

    def browse_dest_folder(self):
        """Open a dialog to select the destination folder"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.output_folder = folder_selected
            self.dest_folder_path.set(folder_selected)
            self.output_path_label.config(text=self.output_folder)

    def start_conversion(self):
        """Start the image conversion process"""
        if not self.folder_path.get():
            messagebox.showwarning("Warning", "Please select a source folder first")
            return

        # Disable the convert button while processing
        self.convert_btn.config(state=tk.DISABLED)
        self.progress_label.config(text="Processing images...")

        # Start conversion in a separate thread
        threading.Thread(target=self.convert_images, daemon=True).start()

    def convert_images(self):
        """Actual image conversion logic"""
        input_folder = self.folder_path.get()
        success_count = 0
        fail_count = 0

        try:
            files = [f for f in os.listdir(input_folder) if f.lower().endswith(
                ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff'))]
            total_files = len(files)
            if total_files == 0:
                self.update_progress("No images found in the selected folder", 0)
                return

            for i, filename in enumerate(files):
                try:
                    # Update progress
                    self.update_progress(f"Processing: {filename}", (i + 1) / total_files * 100)

                    # Open and resize the image
                    with Image.open(os.path.join(input_folder, filename)) as img:
                        img.thumbnail((500, 500), Image.LANCZOS)

                        # Create a new image with a black background
                        new_img = Image.new("RGB", (500, 500), (0, 0, 0))
                        new_img.paste(img, (
                            (500 - img.width) // 2,
                            (500 - img.height) // 2
                        ))

                        # Save the image
                        new_filename = os.path.splitext(filename)[0] + ".png"
                        output_path = os.path.join(self.output_folder, new_filename)
                        new_img.save(output_path, "PNG")
                        success_count += 1
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
                    fail_count += 1

                # Update statistics
                self.update_stats(success_count, fail_count)

            # Show completion message
            self.update_progress(f"Finished processing {total_files} images", 100)
            messagebox.showinfo("Success",
                                f"{success_count} images converted successfully\n{fail_count} failed to convert")
        except Exception as e:
            self.update_progress(f"Error: {str(e)}", 0)
            messagebox.showerror("Error", f"An error occurred while processing images: {str(e)}")
        finally:
            # Re-enable the convert button
            self.root.after(0, lambda: self.convert_btn.config(state=tk.NORMAL))

    def update_progress(self, message, value):
        """Update the progress bar and status message"""
        self.root.after(0, lambda: self.progress_label.config(text=message))
        self.root.after(0, lambda: self.progress.config(value=value))

    def update_stats(self, success, fail):
        """Update conversion statistics"""
        total = success + fail
        self.root.after(0, lambda: self.stats_label.config(
            text=f"{total} Images Converted | {success} Success | {fail} Fail"
        ))


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()