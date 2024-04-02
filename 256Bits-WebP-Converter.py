import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import threading

class ImageCompressorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compressor to WebP - By 256Bits.tech")

        self.select_button = tk.Button(self.root, text="Select Images", command=self.compress_images)
        self.select_button.pack(pady=20)

        self.quality_label = tk.Label(self.root, text="Select Quality Level:")
        self.quality_label.pack()

        self.quality_scale = tk.Scale(self.root, from_=0, to=100, orient="horizontal")
        self.quality_scale.set(0)  # Default quality value
        self.quality_scale.pack()

        self.quality_description = tk.Label(self.root, text="0: Lowest Quality | 100: Best Quality")
        self.quality_description.pack()

        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.result_label.pack()

        self.progress_bar = ttk.Progressbar(self.root, mode="determinate")
        self.progress_bar.pack(fill=tk.BOTH, padx=20, pady=10)

        self.progress_percent = tk.Label(self.root, text="", font=("Helvetica", 12))
        self.progress_percent.pack()

        self.root.geometry("600x250")  # Set initial window size
        self.root.resizable(False, False)  # Disable window resizing

    def compress_images(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.jfif")])
        quality = self.quality_scale.get()
        self.quality_scale.config(state="disabled")  # Disable quality chooser during conversion
        self.progress_bar["maximum"] = len(file_paths)
        self.progress_bar["value"] = 0
        self.result_label.config(text="")
        self.root.update_idletasks()

        threading.Thread(target=self.process_images, args=(file_paths, quality)).start()

    def process_images(self, file_paths, quality):
        for idx, file_path in enumerate(file_paths, start=1):
            try:
                image = Image.open(file_path)
                output_path = file_path.rsplit(".", 1)[0] + f"_compressed_q{quality}.webp"
                image.save(output_path, "webp", quality=quality)
            except Exception as e:
                self.result_label.config(text=f"Error: {e}")
            finally:
                self.progress_bar["value"] = idx
                progress_percent = (idx / len(file_paths)) * 100
                self.progress_percent.config(text=f"{int(progress_percent)}%")
                self.root.update_idletasks()

        self.quality_scale.config(state="normal")  # Re-enable quality chooser
        self.result_label.config(text="Conversion Complete! (Saved to same folder as original images)")
        self.progress_percent.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressorApp(root)
    root.mainloop()
