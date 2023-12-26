from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageFilter, ImageChops
from tkinter import filedialog
import os
import cv2
from PIL import ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from ttkbootstrap import Style
from PIL import ImageChops
import cv2
import PIL.ImageFilter as ImageFilter
import tkinter.ttk as ttk
from tkinter import Button, Scale, Tk



#  Add the ADAPTIVE_THRESH_MEAN_C attribute to the ImageFilter module
ImageFilter.ADAPTIVE_THRESH_MEAN_C = 1

# display images
def display_image(img):
    disp_image = ImageTk.PhotoImage(img)
    panel.configure(image=disp_image)
    panel.image = disp_image

def brightness_callback(brightness_pos):
    brightness_pos = float(brightness_pos) # Convert the value to float for processing
    global output_image
    enhancer = ImageEnhance.Brightness(img) # Create an enhancer object
    output_image = enhancer.enhance(brightness_pos) # Apply brightness enhancement
    display_image(output_image)

def zoom_callback(zoom_pos):
    zoom_pos = float(zoom_pos)  # Convert the value to float
    global output_image
    width, height = img.size  # Get the original image size
    new_width = int(width * zoom_pos) #? calculate the new width
    new_height = int(height * zoom_pos) #? calculate the new height
    img_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR) #? convert the image to array numpy
    resized_image = cv2.resize(img_array, (new_width, new_height), interpolation=cv2.INTER_AREA) #? resize the image, interpolation is the method of resizing
    output_image = Image.fromarray(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))

    display_image(output_image)

def contrast_callback(contrast_pos):#! error in install the module torchvision

    contrast_pos = float(contrast_pos)
    global output_image
    enhancer = ImageEnhance.Contrast(img)
    output_image = enhancer.enhance(contrast_pos)
    display_image(output_image)
    
    # ==========  using torchvision.transforms.functional ==========
    # import torchvision.transforms.functional as F
    # contrast_pos = float(contrast_pos)
    # global output_image
    # img_tensor = F.to_tensor(img) # convert the image to tensor
    # img_tensor = F.adjust_contrast(img_tensor, contrast_pos) # adjust the contrast
    # output_image = F.to_pil_image(img_tensor) # convert the tensor to image
    # display_image(output_image)

def rotate():
    global img
    img_array = np.array(img)
    rotated_img = cv2.rotate(img_array, cv2.ROTATE_90_CLOCKWISE)
    img = Image.fromarray(rotated_img)
    display_image(img)

def blur():
    global img
    img_array = np.array(img) #? convert the image to array numpy
    blurred_img = cv2.blur(img_array, (5, 5)) #? represent as numpy array and (5,5) is the kernel size
    img = Image.fromarray(blurred_img) #? create an image from the array numpy
    display_image(img)

def resize():
    global img
    img_array = np.array(img)
    resized_img = cv2.resize(img_array, (200, 300)) #? resize the image to (200,300)
    img = Image.fromarray(resized_img)
    display_image(img)

def crop():
    global img
    img_array = np.array(img)
    cropped_img = img_array[100:400, 100:400] #? crop the image
    img = Image.fromarray(cropped_img)
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
    #* === first way ===
    # img = img.convert("L")
    # display_image(img)
    
    #* ==== second way ====
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY) #? convert the to gray
    img = Image.fromarray(img)
    display_image(img)

def convert_to_rgb():
    global img
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB) #? convert the image to RGB
    img = Image.fromarray(img)
    display_image(img)

def convert_to_binary():
    global img
    # ===== first way ====
    # img = img.convert("1")
    # display_image(img)
    
    # ==== using cv2 module ====
    img_array = np.array(img)
    img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    _, img_binary = cv2.threshold(img_gray, 87, 255, cv2.THRESH_BINARY) #? convert the image to binary
    img = Image.fromarray(img_binary)
    display_image(img)

def close():
    mains.destroy()

def show_histogram(): # show all channel in the images

    global img
    img_array = np.array(img)
    plt.hist(img_array.ravel(), bins=256, color='gray', alpha=0.7)
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.title('Image Histogram')
    plt.show()

def adaptive_threshold():
    global img
    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    img_binary = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 199, 5) #? convert the image to binary
    #* adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize , C )
    #* blockSize: حجم حيز البكسل المستخدم لحساب الحد التكيفي.
    #* C: الثابت المُطرح من المتوسط أو المتوسط المرجح.
    img = Image.fromarray(img_binary) 
    display_image(img)

def image_reflection():
    #* ====== using PIL ======
    # global img
    # img = img.transpose(Image.FLIP_LEFT_RIGHT)
    # display_image(img)

    #* ====== using cv2 =====
    global img
    img = cv2.flip(np.array(img), 1)
    img = Image.fromarray(img)
    display_image(img)

def gamma_correction(): 
    global img
    gamma = 1.5 
    img_array = np.array(img)
    img_gamma_corrected = np.power(img_array / 255.0, gamma) * 255.0 #? Apply gamma correction and 255.0 is the max value of the pixel
    img_gamma_corrected = img_gamma_corrected.astype(np.uint8) #? convert the image to uint8 because the value of the pixel is between 0 and 255
    img = Image.fromarray(img_gamma_corrected) #? create an image from the array numpy
    display_image(img)

def otsu_threshold():
    global img
    img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
    _, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU) #? convert the image 
    # threshold(src, thresh, maxval, type[, dst]) -> retval, dst
    img = Image.fromarray(img_binary) #? create an image from the array numpy
    display_image(img)

def mean_filter():
    global img
    np_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    blurred = cv2.blur(np_img, (5, 5))  #? apply the mean_filter
    img = Image.fromarray(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    display_image(img)

def gaussian_filter():
    global img
    np_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    blurred = cv2.GaussianBlur(np_img, (5, 5), 0)  #? apply the gaussian_filter with kernel size (5,5) and sigma=0
    img = Image.fromarray(cv2.cvtColor(blurred, cv2.COLOR_BGR2RGB))
    display_image(img)

def median_filter():#! error >  (- Argument 'ksize' is required to be an integer)
    global img
    np_img = np.array(img)
    blurred = cv2.medianBlur(np_img, (5, 5))  #? apply the median_filter with kernel size (5,5)
    img = Image.fromarray(blurred)
    print('--------- apply')
    display_image(img)

def blind_image():
    global img
    img1_path = filedialog.askopenfilename(title="Select Image 1")
    img2_path = filedialog.askopenfilename(title="Select Image 2")
    if img1_path and img2_path:
        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)
        # Resize the images to the same size
        img1 = img1.resize((img.width, img.height))
        img2 = img2.resize((img.width, img.height))
        # Convert PIL images to NumPy arrays
        np_img1 = np.array(img1)
        np_img2 = np.array(img2)
        blended = cv2.addWeighted(np_img1, 0.5, np_img2, 0.5, 0) #? Perform blending using cv2.addWeighted
        img = Image.fromarray(blended)
        display_image(img)

def and_operation():
    global img
    img1_path = filedialog.askopenfilename(title="Select Image 1")
    img2_path = filedialog.askopenfilename(title="Select Image 2")
    if img1_path and img2_path:
        img1 = cv2.imread(img1_path, cv2.COLOR_BGR2RGB)
        img2 = cv2.imread(img2_path, cv2.COLOR_BGR2RGB)
        # Resize the images to the same size
        img1 = cv2.resize(img1, (img.width, img.height))
        img2 = cv2.resize(img2, (img.width, img.height))
        img = cv2.bitwise_and(img1, img2) #? Perform AND operation
        # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        img = Image.fromarray(img)
        display_image(img)

def or_operation():
    global img
    img1_path = filedialog.askopenfilename(title="Select Image 1")
    img2_path = filedialog.askopenfilename(title="Select Image 2")
    if img1_path and img2_path:
        img1 = cv2.imread(img1_path, cv2.COLOR_BGR2RGB)
        img2 = cv2.imread(img2_path, cv2.COLOR_BGR2RGB)
        # Resize the images to the same size
        img1 = cv2.resize(img1, (img.width, img.height))
        img2 = cv2.resize(img2, (img.width, img.height))
        img = cv2.bitwise_or(img1, img2) #? Perform OR operation
        # ValueError: The truth value of an array with more than one element is ambiguous. Use a.any() or a.all()
        img = Image.fromarray(img)
        display_image(img)

def divide_operation():
    global img
    img1_path = filedialog.askopenfilename(title="Select Image 1")
    img2_path = filedialog.askopenfilename(title="Select Image 2")
    if img1_path and img2_path:
        img1 = cv2.imread(img1_path, cv2.COLOR_BGR2RGB)
        img2 = cv2.imread(img2_path, cv2.COLOR_BGR2RGB)
        # Resize the images to the same size
        img1 = cv2.resize(img1, (img.width, img.height))
        img2 = cv2.resize(img2, (img.width, img.height))
        img = cv2.divide(img1, img2, scale=255.0) #? Perform pixel-wise division
        img = Image.fromarray(img)
        display_image(img)    

def multipluy_operation():
    global img
    img1_path = filedialog.askopenfilename(title="Select Image 1")
    img2_path = filedialog.askopenfilename(title="Select Image 2")
    if img1_path and img2_path:
        img1 = cv2.imread(img1_path, cv2.COLOR_BGR2RGB)
        img2 = cv2.imread(img2_path, cv2.COLOR_BGR2RGB)
        # Resize the images to the same size
        img1 = cv2.resize(img1, (img.width, img.height))
        img2 = cv2.resize(img2, (img.width, img.height))
        img = cv2.multiply(img1, img2, scale=1/255.0) #? Perform pixel-wise  and scale=1/255.0 mean the value of the pixel is between 0 and 1        
        img = Image.fromarray(img)
        display_image(img)

#  =========== GUI ===========
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

img = Image.open("img1.png")
img = img.resize((700, 600))

panel = Label(mains)
panel.grid(row=0, column=0, rowspan=12, padx=50, pady=50)
display_image(img)

# button hover function
button_bg_color = "#36577a"

def apply_button_style(button):
    button.configure(
        font=('consolas', 10, 'bold'),
        foreground='white',
        cursor='hand2',
        padx=10,  # Padding on the x-axis
        pady=5,   # Padding on the y-axis
    )
    button.bind("<Enter>", lambda event: button.config(bg="BLACK"))
    button.bind("<Leave>", lambda event: button.config(bg=button_bg_color))
    


btn_reset = Button(mains, text="Reset", command=reset, bg="BLACK", activebackground="ORANGE")
apply_button_style(btn_reset)
btn_reset.place(x=360, y=15)

btn_close = Button(mains, text='Close', command=close, bg="BLACK", activebackground="ORANGE")
apply_button_style(btn_close)
btn_close.place(x=450, y=15)

brightness_slider = Scale(mains, label="Brightness", from_=0, to=2, orient=HORIZONTAL, length=200,
                            resolution=0.1, command=brightness_callback, bg="PINK")
brightness_slider.set(1)
brightness_slider.configure(font=('consolas', 10, 'bold'), foreground='black')
brightness_slider.place(x=1070, y=15)

resolution_slider = Scale(mains, label="zoom", from_=0, to=2, orient=HORIZONTAL, length=200,
                            resolution=0.1, command=zoom_callback, bg="PINK")
resolution_slider.set(1)
resolution_slider.configure(font=('consolas', 10, 'bold'), foreground='black')
resolution_slider.place(x=1070, y=90)

contrast_slider = Scale(mains, label="Saturations", from_=0, to=2, orient=HORIZONTAL, length=200,
                        command=contrast_callback, resolution=0.1, bg="light green")
contrast_slider.set(1)
contrast_slider.configure(font=('consolas', 10, 'bold'), foreground='black')
contrast_slider.place(x=1070, y=165)

btn_change_img = Button(mains, text='Change Image', width=25, command=change_image, bg="RED", activebackground="ORANGE")
apply_button_style(btn_change_img)
btn_change_img.place(x=805, y=35)

btn_convert_gray = Button(mains, text='Convert to Gray', width=25, command=convert_to_gray, bg="GRAY")
apply_button_style(btn_convert_gray)
btn_convert_gray.place(x=805, y=90)

btn_convert_rgb = Button(mains, text='Convert to RGB', width=25, command=convert_to_rgb, bg="BLUE")
apply_button_style(btn_convert_rgb)
btn_convert_rgb.place(x=805, y=125)

btn_convert_binary = Button(mains, text='Convert to Binary', width=25, command=convert_to_binary, bg="BROWN")
apply_button_style(btn_convert_binary)
btn_convert_binary.place(x=805, y=160)



btn_rotate = Button(mains, text='Rotate', width=25, command=rotate, bg="GREEN")
apply_button_style(btn_rotate)
btn_rotate.place(x=805, y=195)

btn_resize = Button(mains, text='Resize', width=25, command=resize, bg="YELLOW")
apply_button_style(btn_resize)
btn_resize.place(x=805, y=230)

btn_crop = Button(mains, text='Crop', width=25, command=crop, bg="VIOLET")
apply_button_style(btn_crop)
btn_crop.place(x=805, y=265)

btn_blur = Button(mains, text='Blur', width=25, command=blur, bg="ORANGE")
apply_button_style(btn_blur)
btn_blur.place(x=805, y=300)

btn_add_images = Button(mains, text='blind images', width=25, command=blind_image, bg="ORANGE")
apply_button_style(btn_add_images)
btn_add_images.place(x=805, y=335)

btn_and_operation = Button(mains, text='AND Operation', width=25, command=and_operation, bg="CYAN")
apply_button_style(btn_and_operation)
btn_and_operation.place(x=805, y=370)

btn_or_operation = Button(mains, text='OR Operation', width=25, command=or_operation, bg="PURPLE")
apply_button_style(btn_or_operation)
btn_or_operation.place(x=805, y=405)


btn_histogram = Button(mains, text='Histogram', width=25, command=show_histogram, bg="CYAN")
apply_button_style(btn_histogram)
btn_histogram.place(x=805, y=440)

btn_reflection = Button(mains, text='Reflection', width=25, command=image_reflection, bg="LIGHT BLUE")
apply_button_style(btn_reflection)
btn_reflection.place(x=805, y=475)

btn_gamma_correction = Button(mains, text='Gamma Correction', width=25, command=gamma_correction, bg="LIGHT YELLOW")
apply_button_style(btn_gamma_correction)
btn_gamma_correction.place(x=805, y=510)

btn_adaptive_threshold = Button(mains, text='Adaptive Threshold', width=25, command=adaptive_threshold, bg="MAGENTA")
apply_button_style(btn_adaptive_threshold)
btn_adaptive_threshold.place(x=805, y=545)

btn_otsu_threshold = Button(mains, text='Otsu Threshold', width=25, command=otsu_threshold, bg="PURPLE")
apply_button_style(btn_otsu_threshold)
btn_otsu_threshold.place(x=805, y=580)

btn_mean_filter = Button(mains, text='Mean Filter', width=25, command=mean_filter, bg="LIGHT YELLOW")
apply_button_style(btn_mean_filter)
btn_mean_filter.place(x=805, y=615)

btn_gaussian_filter = Button(mains, text='Gaussian Filter', width=25, command=gaussian_filter, bg="LIGHT BLUE")
apply_button_style(btn_gaussian_filter)
btn_gaussian_filter.place(x=805, y=650)

btn_median_filter = Button(mains, text='Median Filter', width=25, command=median_filter, bg="MAGENTA")
apply_button_style(btn_median_filter)
btn_median_filter.place(x=1070, y=350)


btn_multi_operation = Button(mains, text='multipluy Operation', width=25, command=multipluy_operation, bg="PURPLE")
apply_button_style(btn_multi_operation)
btn_multi_operation.place(x=1070, y=280)

btn_divide_operation = Button(mains, text='Divide Operation', width=25, command=divide_operation, bg="PURPLE")
apply_button_style(btn_divide_operation)
btn_divide_operation.place(x=1070, y=315)


btn_save = Button(mains, text='Save', width=25, command=save, bg="BROWN")
apply_button_style(btn_save)
btn_save.place(x=805, y=710)

mains.mainloop()