import tkinter as tk
from tkinter import filedialog, Label, Button
from PIL import Image, ImageTk
import cv2
import os
from utils import analyze_ripeness

class FruitApp:
    def __init__(self, root):
        self.bg_color = "#D8BFD8"
        root.configure(bg=self.bg_color)
        self.root = root
        self.root.title("Deteksi Kematangan Buah")
        self.root.geometry("400x600")

        self.selected_fruit = tk.StringVar(root)
        self.selected_fruit.set("Pisang")

        # Dropdown Buah
        self.fruit_menu = tk.OptionMenu(root, self.selected_fruit, "Pisang", "Jeruk", "Apel", "Mangga")
        self.fruit_menu.config(font=("Arial", 12), bg="white", fg="#333333", highlightbackground=self.bg_color)
        self.fruit_menu.pack(pady=10)

        # Judul
        self.label = Label(root, text="Pilih gambar buah untuk dianalisis", font=("Arial", 14, "bold"),
                           bg=self.bg_color, fg="#222222")
        self.label.pack(pady=10)

        # Tempat gambar tampil
        self.image_label = Label(root, bg=self.bg_color)
        self.image_label.pack(pady=5)

        # Hasil
        self.result_label = Label(root, text="", font=("Arial", 12), bg=self.bg_color, fg="#006400")
        self.result_label.pack(pady=15)

        # Tombol Pilih Gambar
        self.select_button = Button(root, text="Pilih Gambar", command=self.select_image,
                                    font=("Arial", 12), bg="#4CAF50", fg="white")
        self.select_button.pack(pady=10)

        # Tombol Kamera
        self.camera_button = Button(root, text="Deteksi dengan Kamera", command=self.capture_from_camera,
                                    font=("Arial", 12), bg="#2196F3", fg="white")
        self.camera_button.pack(pady=10)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.display_and_analyze(file_path)

    def display_and_analyze(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((300, 300))
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

        fruit_type = self.selected_fruit.get()
        result = analyze_ripeness(file_path, fruit_type)
        self.result_label.config(text=f"Hasil: {result}")

    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)
        cv2.namedWindow("Tekan 's' untuk Simpan dan Deteksi")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("Tekan 's' untuk Simpan dan Deteksi", frame)
            key = cv2.waitKey(1)
            if key & 0xFF == ord('s'):
                save_path = "captured_fruit.jpg"
                cv2.imwrite(save_path, frame)
                break
            elif key & 0xFF == ord('q'):
                save_path = None
                break

        cap.release()
        cv2.destroyAllWindows()

        if save_path:
            self.display_and_analyze(save_path)
            os.remove(save_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = FruitApp(root)
    root.mainloop()
