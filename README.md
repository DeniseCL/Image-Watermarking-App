# 📝 Project Summary: Image Watermarking Desktop App
## 🎯 Goal:
Build a GUI desktop app that lets the user:
- Upload an image
- Add a customizable text watermark (size, position)
- Preview the result
- Save the watermarked image in high quality

## 🧱 Technologies Used:
- tkinter for the GUI
- Pillow (PIL) for image processing
- Python's os, filedialog, and messagebox for file handling and feedback

## ✅ Features Implemented:
1. Image upload and display in GUI
- Used `filedialog.askopenfilename()` to select images.
- Displayed a scaled-down version using `thumbnail()` for GUI preview.

2. Watermark text input
- Added a `tk.Entry` so the user can type the watermark.

3. Font size selector
- Used a `tk.Spinbox` to allow dynamic font sizing.

4. Watermark positioning
- Allowed the user to choose among 4 positions via a dropdown (`OptionMenu`).
- Calculated the placement using image dimensions and text size.

5. Transparency (alpha channel)
- Created an RGBA layer and drew semi-transparent text using `Image.alpha_composite`.

6. Image saving
- Ensured high-quality output by saving the full-resolution version before applying `.thumbnail()`.
- Allowed saving in multiple formats (`.png, .jpg, .bmp`).

7. User-friendly GUI improvements
- Aligned layout using `tk.Frame` for better aesthetics.
- Resized and centered the main window automatically.

## ⚠️ Common Issues You Faced & Fixed:

| Issue | Solution|
|----------|----------|
| ❌ Used `filedialog.askopenfile()` → opened file in text mode, causing image decoding error    | ✅ Replaced with `askopenfilename()` to get the file path as a string |
| ❌ `Image.open()` failed with UTF-8 decode error  | ✅ Caused by trying to open an image as text, fixed with the point above  |
| ❌ `draw.textsize(...)` returned `None`   | ✅ Replaced with `draw.textbbox()` (required for Pillow 10+)  |
| ❌ `font.getsize()` deprecated   | ✅ Used `draw.textbbox()` to calculate text dimensions  |
| ❌ Font size didn’t change   | ✅ It was falling back to `ImageFont.load_default()` which doesn’t respect size → solved by loading fonts directly from the system  |
| ❌ Saved image was blurry or low-res   | ✅ Caused by calling `.thumbnail()` before saving → fixed by separating preview and full-res images  |




