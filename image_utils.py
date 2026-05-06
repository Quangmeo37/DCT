from PIL import Image
import numpy as np

# load ảnh
def load_image(path):
    img = Image.open(path).convert('L')
    return np.array(img, dtype=np.float32)


# lưu ảnh
def save_image(image, path):
    image = np.clip(image, 0, 255)
    img = Image.fromarray(image.astype('uint8'))
    img.save(path)


# padding
def pad_image(image):
    image = image.copy()  # ⭐ tránh ảnh hưởng ảnh gốc

    h, w = image.shape
    new_h = (h + 7) // 8 * 8
    new_w = (w + 7) // 8 * 8

    padded = np.zeros((new_h, new_w), dtype=np.float32)
    padded[:h, :w] = image

    return padded


# chia block
def split_blocks(image):
    h, w = image.shape
    blocks = []

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = image[i:i+8, j:j+8].copy()  # ⭐ tránh reference
            blocks.append(block)

    return blocks


# ghép block
def merge_blocks(blocks, shape):
    h, w = shape
    image = np.zeros((h, w), dtype=np.float32)

    idx = 0
    for i in range(0, h, 8):
        for j in range(0, w, 8):
            image[i:i+8, j:j+8] = blocks[idx]
            idx += 1

    return image