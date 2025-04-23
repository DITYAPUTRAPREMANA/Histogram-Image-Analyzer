import cv2
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog, messagebox

def calc_histogram(img, channel=None, bins=256):
    if channel is not None:
        hist = cv2.calcHist([img], [channel], None, [bins], [0, bins])
    else:
        hist = cv2.calcHist([img], [0], None, [bins], [0, bins])
    hist = hist.flatten()
    return hist

def normalize_histogram(hist, n_pixels):
    norm_hist = hist / n_pixels
    return norm_hist

def stats_histogram(norm_hist):
    gray_levels = np.arange(len(norm_hist))
    mean = np.sum(gray_levels * norm_hist)
    variance = np.sum(((gray_levels - mean) ** 2) * norm_hist)
    stddev = np.sqrt(variance)
    return mean, variance, stddev

def analyze_image_histogram(image_path):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Gambar tidak ditemukan atau format tidak didukung.")
        return

    if len(img.shape) == 2 or (len(img.shape) == 3 and img.shape[2] == 1):
        img_gray = img
        mode = "grayscale"
    else:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mode = "color"

    hist_gray = calc_histogram(img_gray)
    n_pixels = img_gray.shape[0] * img_gray.shape[1]
    norm_hist_gray = normalize_histogram(hist_gray, n_pixels)
    mean_gray, var_gray, stddev_gray = stats_histogram(norm_hist_gray)

    print(f"Statistik Grayscale:")
    print(f"- Mean: {mean_gray:.2f}")
    print(f"- Variansi: {var_gray:.2f}")
    print(f"- Stddev: {stddev_gray:.2f}")

    plt.figure(figsize=(12,4))
    plt.subplot(1, 2 if mode == "color" else 1, 1)
    plt.title('Histogram Grayscale')
    plt.xlabel('Gray level')
    plt.ylabel('Jumlah Pixel')
    plt.bar(range(256), hist_gray, color='black', alpha=0.7)
    plt.tight_layout()

    if mode == "color":
        colors = ('b','g','r')
        for i, col in enumerate(colors):
            hist = calc_histogram(img, channel=i)
            norm_hist = normalize_histogram(hist, n_pixels)
            mean, var, stddev = stats_histogram(norm_hist)
            print(f"Statistik {col.upper()}:")
            print(f"- Mean: {mean:.2f}")
            print(f"- Variansi: {var:.2f}")
            print(f"- Stddev: {stddev:.2f}")

            plt.subplot(1, 2, 2)
            plt.title('Histogram RGB')
            plt.xlabel('Level')
            plt.ylabel('Jumlah Pixel')
            plt.plot(hist, color=col, label=col.upper())
        plt.legend()

    plt.show()

def open_and_analyze():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tif;*.tiff")],
        title="Pilih file gambar untuk dianalisis"
    )
    if file_path:
        analyze_image_histogram(file_path)

root = tk.Tk()
root.title("Histogram Image Analyzer")
root.geometry("300x150")
root.resizable(False, False)

label = tk.Label(root, text="Klik tombol di bawah untuk upload gambar\n dan menganalisis histogramnya.", pady=20)
label.pack()
upload_btn = tk.Button(root, text="Upload dan Analisis Gambar", command=open_and_analyze, padx=10, pady=10)
upload_btn.pack()

root.mainloop()
