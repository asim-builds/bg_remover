# Background Remover

A simple desktop application to remove backgrounds from images using AI.  
Built with Python, CustomTkinter, and [rembg](https://github.com/danielgatis/rembg).

## Features

- Add multiple images for batch background removal
- Output images in your chosen format and folder

## How to Use

1. **Run the app**  
   - Or run `python main.py` if you have Python and dependencies installed

2. **Select images**  
   - Click select images to open the file picker

3. **Choose output folder and format**  
   - Set your desired output directory and image format

4. **Click "Remove Background"**  
   - Processed images will be saved to the output folder

## How to Build the Executable

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Find your Python site-packages path:**  
   - Example: `C:\Users\YourUser\AppData\Local\Programs\Python\Python3x\Lib\site-packages`

3. **Build with PyInstaller:**
   ```
   pyinstaller --onedir --clean --windowed ^
     --hidden-import=customtkinter ^
     --hidden-import=ctkmessagebox ^
     --hidden-import=tkinterdnd2 ^
     --hidden-import=PIL ^
     --hidden-import=rembg ^
     --hidden-import=onnxruntime ^
     --add-data "config;config" ^
     --add-data "ui;ui" ^
     --add-data "<path_to_site_packages>\\onnxruntime;onnxruntime" ^
     main.py
   ```
   Replace `<path_to_site_packages>` with your actual path.

4. **Distribute the `dist` folder**  
   - Share the `dist` folder with users. They can run the `.exe` without installing Python.

## Notes

- If you run into errors on a new machine, ensure the [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) is installed.
- For best results, use high-quality input images.

---

**Enjoy removing backgrounds!**