import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

""" window vs root """
"""'window' is the local name of the variable inside the run_app() function.
    'root' is the name of the parameter that the class expects to receive in __init__.
    They are two different variables that point to the same object (the main window)."""


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        # self.root.geometry("800x600")

        # Set desired window size
        window_width = 1000
        window_height = 700

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position for centering
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Set geometry and position
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.image_label = tk.Label(self.root)
        self.image_label.pack(pady=10)

        self.original_image = None   # Save the original image

        # Button Select Image
        self.select_button = tk.Button(self.root, text="Select Image", command=self.open_image, width=15)
        self.select_button.pack(pady=20)

        # Watermark Text Field
        self.watermark_text_var = tk.StringVar()
        self.watermark_text_var.set("WATERMARK")  # Default value

        text_entry_label = tk.Label(self.root, text="Watermark Text:")
        text_entry_label.pack()

        text_entry = tk.Entry(self.root, textvariable=self.watermark_text_var, width=40)
        text_entry.pack(pady=5)

        # Font size + position in a single horizontal frame
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=5)

        # Font Size
        self.font_size_var = tk.IntVar()
        self.font_size_var.set(36)
        font_size_label = tk.Label(controls_frame, text="Font Size:")
        font_size_label.pack(side="left", padx=(0, 5))
        font_size_spinbox = tk.Spinbox(controls_frame, from_=10, to=200, textvariable=self.font_size_var, width=5)
        font_size_spinbox.pack(side="left", padx=(0, 20))

        # Watermark Position
        self.position_var = tk.StringVar()
        self.position_var.set("Bottom Right")
        position_label = tk.Label(controls_frame, text="Position:")
        position_label.pack(side="left", padx=(0, 5))
        position_options = ["Top Left", "Top Right", "Bottom Left", "Bottom Right"]
        position_menu = tk.OptionMenu(controls_frame, self.position_var, *position_options)
        position_menu.pack(side="left")

        # Button Watermark
        self.watermark_button = tk.Button(self.root, text="Add Watermark", command=self.add_watermark, width=15)
        self.watermark_button.pack(pady=10)

        # Button Save Image
        self.save_button = tk.Button(self.root, text="Save Image", command=self.save_image, width=15)
        self.save_button.pack(pady=10)

    def open_image(self):
        """ filedialog.askopenfile() - This method returns a file opened in text mode by default.
            Change to filedialog.askopenfilename() """
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])

        if file_path:
            try:
                image = Image.open(file_path)
                print(f"[DEBUG] Image format: {image.format}")

                self.original_image = image.copy()

                # Resize to fit screen if necessary
                image.thumbnail((600, 400))
                photo = ImageTk.PhotoImage(image)

                self.image_label.config(image=photo)
                self.image_label.image = photo

                messagebox.showinfo("Image loaded", f"Image displayed successfully.")

            except Exception as e:
                messagebox.showerror("Error", f"Error opening image:\n{str(e)}")

    def get_font(self, size):
        paths = [
            "/System/Library/Fonts/Supplemental/Arial.ttf",  # macOS
            "/System/Library/Fonts/Helvetica.ttc",  # macOS alt
            "arial.ttf",  # Windows
        ]
        for path in paths:
            try:
                return ImageFont.truetype(path, size)
            except:
                continue
        print("[DEBUG] No custom font found. Using default.")
        return ImageFont.load_default()

    def add_watermark(self):
        if self.original_image is None:
            messagebox.showwarning("No image", "Please load an image first.")
            return

        image = self.original_image.convert("RGBA")
        watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)

        watermark_text = self.watermark_text_var.get()

        try:
            font_size = self.font_size_var.get()
            font = self.get_font(font_size)

        except:
            print("[DEBUG] Failed to load 'arial.ttf'. Using default font.")
            font = ImageFont.load_default()

        width, height = image.size
        bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        position = self.position_var.get()

        if position == "Top Left":
            x, y = 10, 10
        elif position == "Top Right":
            x = width - text_width - 10
            y = 10
        elif position == "Bottom Left":
            x = 10
            y = height - text_height - 10
        else:  # Bottom Right
            x = width - text_width - 10
            y = height - text_height - 10

        draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 70))  # 70 = represents transparency
        """ 70 = represents transparency
        Adjust this value between 0 (completely invisible) and 255 (completely opaque)
        Recommended: between 50 and 80 for that subtle watermark look."""

        # Combine the watermark with the original image
        watermarked_image = Image.alpha_composite(image, watermark_layer)

        # Save the full-res version BEFORE resizing
        self.watermarked_image = watermarked_image.convert("RGB")

        # Display a reduced version (thumbnail for preview)
        preview_image = self.watermarked_image.copy()
        preview_image.thumbnail((600, 400))
        photo = ImageTk.PhotoImage(preview_image)

        self.image_label.config(image=photo)
        self.image_label.image = photo

        messagebox.showinfo("Success", "Watermark added!")

    def save_image(self):
        if not hasattr(self, "watermarked_image"):
            messagebox.showwarning("No watermark", "Please add a watermark before saving.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("BMP files", "*.bmp"),
            ],
            title="Save image as..."
        )

        if file_path:
            try:
                self.watermarked_image.save(file_path)
                messagebox.showinfo("Success", f"Image saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{str(e)}")


def run_app():
    window = tk.Tk()   # Create the main window
    app = WatermarkApp(window)   # Pass the window to our class
    window.mainloop()   # Start the interface loop
