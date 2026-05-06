import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

from image_utils import save_image, pad_image, split_blocks, merge_blocks
from dct import dct_2d, idct_2d
from compression import quantize, dequantize


# load ảnh
def load_color_image(path):
    img = Image.open(path).convert('RGB')
    return np.array(img, dtype=np.float32)


# nén ảnh màu
def compress_image_array(image):
    image = image.copy()

    channels = []

    # Xử lý từng kênh R, G, B
    for c in range(3):
        channel = image[:, :, c]

        padded = pad_image(channel).copy()
        padded = padded - 128

        blocks = split_blocks(padded)
        processed_blocks = []

        for block in blocks:
            dct_block = dct_2d(block)
            q_block = quantize(dct_block)
            deq_block = dequantize(q_block)
            idct_block = idct_2d(deq_block)

            processed_blocks.append(idct_block)

        reconstructed = merge_blocks(processed_blocks, padded.shape)
        reconstructed = reconstructed + 128

        channels.append(reconstructed)

    # Ghép lại ảnh màu
    result = np.stack(channels, axis=2)

    return np.clip(result, 0, 255)


# GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Nén ảnh màu bằng DCT")

        self.root.geometry("700x450")
        self.root.resizable(False, False)

        self.original_image = None
        self.compressed_image = None

        # Buttons
        tk.Button(root, text="Chọn ảnh", width=20, command=self.open_image).pack(pady=5)
        tk.Button(root, text="Nén ảnh", width=20, command=self.compress_image).pack(pady=5)
        tk.Button(root, text="Lưu ảnh", width=20, command=self.save_compressed_image).pack(pady=5)

        # Frame
        self.frame = tk.Frame(root)
        self.frame.pack()

        tk.Label(self.frame, text="Ảnh gốc (RGB)").grid(row=0, column=0)
        tk.Label(self.frame, text="Ảnh sau nén (DCT)").grid(row=0, column=1)

        # Canvas hiển thị
        self.canvas_original = tk.Canvas(self.frame, width=250, height=250, bg="gray")
        self.canvas_original.grid(row=1, column=0, padx=10)

        self.canvas_compressed = tk.Canvas(self.frame, width=250, height=250, bg="gray")
        self.canvas_compressed.grid(row=1, column=1, padx=10)

    # chọn ảnh
    def open_image(self):
        file_path = filedialog.askopenfilename()

        if not file_path:
            return

        self.original_image = load_color_image(file_path)

        self.show_image(self.original_image, self.canvas_original)

        self.canvas_compressed.delete("all")

    # nén ảnh 
    def compress_image(self):
        if self.original_image is None:
            messagebox.showwarning("Lỗi", "Vui lòng chọn ảnh trước!")
            return

        self.compressed_image = compress_image_array(self.original_image)

        self.show_image(self.compressed_image, self.canvas_compressed)

    # hiển thị ảnh
    def show_image(self, img_array, canvas):
        img_array = np.clip(img_array, 0, 255)

        img = Image.fromarray(img_array.astype("uint8"))
        img = img.resize((250, 250))

        imgtk = ImageTk.PhotoImage(img)

        canvas.delete("all")
        canvas.create_image(0, 0, anchor="nw", image=imgtk)
        canvas.image = imgtk  # giữ reference

    #lưu ảnh
    def save_compressed_image(self):
        if self.compressed_image is None:
            messagebox.showwarning("Lỗi", "Chưa có ảnh để lưu!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[
                ("JPEG", "*.jpg"),
                ("PNG", "*.png")
            ],
            title="Chọn nơi lưu ảnh"
        )

        if not file_path:
            return

        save_image(self.compressed_image, file_path)

        messagebox.showinfo("Thành công", "Đã lưu ảnh!")

# main
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
