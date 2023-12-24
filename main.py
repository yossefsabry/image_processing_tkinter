from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageFilter
from tkinter import filedialog
import os
import cv2
from PIL import ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from ttkbootstrap import Style

def display_image(img):
    disp_image = ImageTk.PhotoImage(img)
    panel.configure(image=disp_image)
    panel.image = disp_image

# Fix: Import the missing ttk module
import tkinter.ttk as ttk

# Fix: Import the missing ImageFilter module
import PIL.ImageFilter as ImageFilter

# Fix: Add the ADAPTIVE_THRESH_MEAN_C attribute to the ImageFilter module
ImageFilter.ADAPTIVE_THRESH_MEAN_C = 1

def brightness_callback(brightness_pos):
    brightness_pos = float(brightness_pos)
    global output_image
    enhancer = ImageEnhance.Brightness(img)
    output_image = enhancer.enhance(brightness_pos)
    display_image(output_image)

def contrast_callback(contrast_pos):
    contrast_pos = float(contrast_pos)
    global output_image
    enhancer = ImageEnhance.Contrast(img)
    output_image = enhancer.enhance(contrast_pos)
    display_image(output_image)

def rotate():
    global img
    img = img.rotate(90)
    display_image(img)

def blur():
    global img
    img = img.filter(ImageFilter.BLUR)
    display_image(img)

def resize():
    global img
    img = img.resize((200, 300))
    display_image(img)

def crop():
    global img
    img = img.crop((100, 100, 400, 400))
    display_image(img)

def reset():
    mains.destroy()
    os.popen("main.py")

def change_image():
    global img
    imgname = filedialog.askopenfilename(title="Change Image")
    if imgname:
        img = Image.open(imgname)
        img = img.resize((600, 600))
        display_image(img)

def save():
    global img
    savefile = filedialog.asksaveasfile(defaultextension=".jpg")
    output_image.save(savefile)

def convert_to_gray():
    global img
    img = img.convert("L")
    display_image(img)

def convert_to_rgb():
    global img
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    img = Image.fromarray(img)
    display_image(img)

def convert_to_binary():
    global img
    img = img.convert("1")
    display_image(img)

def close():
    mains.destroy()

def show_histogram():
    global img
    img_array = np.array(img)
    plt.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Image Histogram')
    plt.show()

def adaptive_threshold():
    global img
    radius = 15  # You can adjust the radius as needed

    def threshold_function(p):
        threshold_value = 128  # Define the threshold value here
        return 255 if p > threshold_value else 0

    img = img.point(threshold_function)
    display_image(img)
    
def image_reflection():
    global img
    img = img.transpose(Image.FLIP_LEFT_RIGHT)
    display_image(img)

def gamma_correction():
    global img
    gamma = 1.5
    img = ImageEnhance.Contrast(img).enhance(gamma)

    # Convert img to the mode of the original image
    img = img.convert("RGB")  # Adjust the mode as needed
    display_image(img)

def otsu_threshold():
    global img
    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    _, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    img = Image.fromarray(img_binary)
    display_image(img)

def mean_filter():
    global img
    img = img.filter(ImageFilter.MedianFilter)
    display_image(img)

def gaussian_filter():
    global img
    img = img.filter(ImageFilter.GaussianBlur)
    display_image(img)

def median_filter():
    global img
    img = img.filter(ImageFilter.MedianFilter)
    display_image(img)
    

# ====================== GUI ======================

mains = Tk()
space = " " * 215
screen_width = mains.winfo_screenwidth()
screen_height = mains.winfo_screenheight()
mains.geometry(f"{screen_width}x{screen_height}")
mains.title(f"{space}Image Editor")

# Set up ttkbootstrap style with a darkly theme
style = Style(theme="darkly")

# Set the background opacity
mains.attributes("-alpha", 0.95)

# style ttkbootstrap widgets
def set_style():
    style.configure("TLabel", foreground="white", background="#000000")
    style.configure("TButton", foreground="white", font=('consolas', 10, 'bold'), borderwidth=0)
    style.map("TButton", background=[("active", "blue"), ("pressed", "blue")])
    style.configure("Horizontal.TScale", thickness=30, troughcolor="black", sliderlength=30)
    style.configure("Vertical.TScale", thickness=30, troughcolor="black", sliderlength=30)
    style.configure("TFrame", background="#000000")
    style.configure("TNotebook", background="#000000")

# Apply styles
set_style()

img = Image.open("GreenHills.jpg")
img = img.resize((700, 600))

panel = Label(mains)
panel.grid(row=0, column=0, rowspan=12, padx=50, pady=50)
display_image(img)


brightness_slider = Scale(mains, label="Brightness", from_=0, to=2, orient=HORIZONTAL, length=200,
                            resolution=0.1, command=brightness_callback, bg="PINK")
brightness_slider.set(1)
brightness_slider.configure(font=('consolas', 10, 'bold'), foreground='black')
brightness_slider.place(x=1070, y=15)

contrast_slider = Scale(mains, label="Contrast", from_=0, to=2, orient=HORIZONTAL, length=200,
                        command=contrast_callback, resolution=0.1, bg="light green")
contrast_slider.set(1)
contrast_slider.configure(font=('consolas', 10, 'bold'), foreground='black')
contrast_slider.place(x=1070, y=90)

btn_rotate = Button(mains, text='Rotate', width=25, command=rotate, bg="GREEN")
btn_rotate.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_rotate.place(x=805, y=110)

btn_reset = Button(mains, text="Reset", command=reset, bg="BLACK", activebackground="ORANGE")
btn_reset.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_reset.place(x=380, y=15)

btn_change_img = Button(mains, text='Change Image', width=25, command=change_image, bg="RED", activebackground="ORANGE")
btn_change_img.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_change_img.place(x=805, y=35)

btn_resize = Button(mains, text='Resize', width=25, command=resize, bg="YELLOW")
btn_resize.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_resize.place(x=805, y=255)

btn_crop = Button(mains, text='Crop', width=25, command=crop, bg="VIOLET")
btn_crop.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_crop.place(x=805, y=340)

btn_blur = Button(mains, text='Blur', width=25, command=blur, bg="ORANGE")
btn_blur.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_blur.place(x=805, y=425)

btn_convert_gray = Button(mains, text='Convert to Gray', width=25, command=convert_to_gray, bg="GRAY")
btn_convert_gray.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_convert_gray.place(x=805, y=510)

btn_convert_rgb = Button(mains, text='Convert to RGB', width=25, command=convert_to_rgb, bg="BLUE")
btn_convert_rgb.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_convert_rgb.place(x=805, y=595)

btn_convert_binary = Button(mains, text='Convert to Binary', width=25, command=convert_to_binary, bg="BROWN")
btn_convert_binary.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_convert_binary.place(x=805, y=680)

btn_save = Button(mains, text='Save', width=25, command=save, bg="BROWN")
btn_save.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_save.place(x=805, y=765)

btn_close = Button(mains, text='Close', command=close, bg="BLACK", activebackground="ORANGE")
btn_close.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_close.place(x=430, y=15)

btn_histogram = Button(mains, text='Histogram', width=25, command=show_histogram, bg="CYAN")
btn_histogram.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_histogram.place(x=805, y=150)

btn_reflection = Button(mains, text='Reflection', width=25, command=image_reflection, bg="LIGHT BLUE")
btn_reflection.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_reflection.place(x=805, y=300)

btn_gamma_correction = Button(mains, text='Gamma Correction', width=25, command=gamma_correction, bg="LIGHT YELLOW")
btn_gamma_correction.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_gamma_correction.place(x=805, y=385)

btn_adaptive_threshold = Button(mains, text='Adaptive Threshold', width=25, command=adaptive_threshold, bg="MAGENTA")
btn_adaptive_threshold.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_adaptive_threshold.place(x=805, y=470)

btn_otsu_threshold = Button(mains, text='Otsu Threshold', width=25, command=otsu_threshold, bg="PURPLE")
btn_otsu_threshold.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_otsu_threshold.place(x=805, y=555)

btn_mean_filter = Button(mains, text='Mean Filter', width=25, command=mean_filter, bg="LIGHT YELLOW")
btn_mean_filter.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_mean_filter.place(x=805, y=640)

btn_gaussian_filter = Button(mains, text='Gaussian Filter', width=25, command=gaussian_filter, bg="LIGHT BLUE")
btn_gaussian_filter.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_gaussian_filter.place(x=805, y=725)

btn_median_filter = Button(mains, text='Median Filter', width=25, command=median_filter, bg="MAGENTA")
btn_median_filter.configure(font=('consolas', 10, 'bold'), foreground='white')
btn_median_filter.place(x=805, y=810)

mains.mainloop()
