# Assignment: Image Watermarking Desktop App
"""
A Desktop program where you can upload images and add a watermark.

Using what you have learnt about Tkinter, you will create a desktop application with a Graphical User Interface (GUI)
where you can upload an image and use Python to add a watermark logo/text.

Normally, you would have to use an image editing software like Photoshop to add the watermark,
but your program is going to do it automatically.

Use case: e.g you want to start posting your photos to Instagram but you want to add your website to all the photos,
you can now use your software to add your website/logo automatically to any image.

A similar online service is: https://watermarkly.com/

You might need:
The Python Imaging Library adds image processing capabilities to your Python interpreter.
https://pypi.org/project/Pillow/
https://docs.python.org/3/library/tkinter.html
and some Googling.
"""
# Approach
import tkinter.filedialog

"""
1. Open/Import photo locally (URL function as bonus feature) --- Show photo in Tkinter GUI instead of photos windoww
tkinter open file explorer;
https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog
2. Allow user to choose what & where to place watermark
pillow python add text (ImageFont)
python pillow add image to image
3. Save photo as new & export/ allow for save
python PIL save image (to specific location) https://stackoverflow.com/questions/31434278/how-do-i-use-python-pil-to-save-an-image-to-a-particular-directory (address too long)
tkinter dialog -- filedialog.askdirectory
               -- filedialog.saveasfilename
>>IMPROVEMENTS -- MORE CONVENIENCE WHEN CREATING THIS APP
-- Can set default layout to pack/unpack as a function so that u dont have to repeatedly pack and unpack all widgets individually

>>Issues:
-- ####IMPORTANT!!!!!!!!!!! Image in GUI not resetting  
-- (FIXED) Buggy program flow if user intentionally dont click options in order
-- (FIXED) Listbox values not updated on first click (solved using button instead of event listener-- that disregards first click)
-- (FIXED) Problem with converting tkinter widget output values to desired value input for functions (string/integer etc for user choice)
   (Tkinter obtain widget output value) #FIXED; ASSIGNED WIDGET OUTPUT TO GLOBAL VAR
--All PIL fonts unavailable 
  How to find fonts available for Pillow?
"""
# MINOR FIXES (time consuming)
"""
--Picture display of specified height and width in Tkinter GUI
--Better widget layout (use grid instead of place) --- VERY TIME CONSUMING - just for aesthetics but functionality unchanged
--Most fonts not available in PIL (aesthetics issue)
--Additional features such as image on image / background styling/shading for watermark + color of watermark text (just add another options box)
--(FIXED) Tkinter listbox dropdown on click- to prevent clutter (workaround- minimize widget aft selection)
   https://stackoverflow.com/questions/45441885/how-can-i-create-a-dropdown-menu-from-a-list-in-tkinter
--(FIXED) Fix watermark location choices (left/right/middle) 
--(FIXED) Saved picture not of original dimensions (stretched); have to revert "im" back to original dimension before saving 
"""

from tkinter import *
from tkinter import ttk
import PIL

"""
To load an image from a file, use the open() function in the Image module:
If successful, this function returns an Image object. 
You can now use instance attributes to examine the file contents:
"""
from PIL import Image, ImageTk, ImageFont, ImageDraw

# im = Image.open("75414.jpg")
# print(im.format, im.size, im.mode)
"""
Once you have an instance of the Image class, you can use the methods defined by this class to process and manipulate the image. 
For example, let’s display the image we just loaded:
"""
# im.show()

window = Tk()
window.title("Image Watermarking App")
window.config(padx=0, pady=0, bg="black")
window.minsize(width=1920, height=1080)
# Tkinter window maximize on default?
window.state('zoomed')

watermark_label = Label(text="Choose any picture to apply a watermark of choice!", bg="#353b36", fg="light blue",
                        font=("Arial", 35))
watermark_label.pack()

im = None
im_unedited = None
img_chosen_display_as_label = None
img_chosen_display_GUI = None

WATERMARK_TEXT = ""
WATERMARK_FONT = ""
WATERMARK_SIZE = 0
watermarkk_size = 10

WATERMARK_X_POS = 0
WATERMARK_Y_POS = 0

selected_font = ""
x_y_pos = ""


def choose_img():
    global im, im_unedited
    # Choose image to apply watermark
    img_chosen = tkinter.filedialog.askopenfilename()
    # Open image
    # But how to let user edit?
    im = Image.open(img_chosen)
    im_unedited = Image.open(img_chosen)
    print("choose_img")
    print(im)
    print(im.format, im.size, im.mode)
    edit_img_button.pack()
    choose_image_button.pack_forget()
    return im


def edit_img():
    global im, img_chosen_display_as_label, img_chosen_display_GUI
    print("EDIT IMAGE")
    print(im)
    # Display chosen image (pillow) in tkinter GUI and allow for edits?
    # https://stackoverflow.com/questions/22802989/displaying-the-selected-image-using-tkinter
    edit_img_button.pack_forget()
    add_watermark_button.pack()

    img_chosen_display_GUI = ImageTk.PhotoImage(im)
    img_chosen_display_as_label = ttk.Label(window, image=img_chosen_display_GUI)
    img_chosen_display_as_label.image = img_chosen_display_GUI

    # How to totally fit picture in window?
    # How to shrink image to ratio 1:1 to fit tkinter window size?
    # https://stackoverflow.com/questions/24061099/tkinter-resize-background-image-to-window-size
    # PIL/Tkinter PhotoImage set size

    img_chosen_display_as_label.bind('<Configure>', resize_image)
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)
    # img_chosen_display_as_label.config(height=1000, width=1000)
    print(img_chosen_display_as_label)


def resize_image(event):
    print("resize_image")
    global im, img_chosen_display_GUI
    new_width = event.width
    new_height = event.height

    copy_of_image = im.copy()

    immg = copy_of_image.resize((new_width, new_height))
    img_chosen_display_GUI = ImageTk.PhotoImage(immg)
    img_chosen_display_as_label.config(image=img_chosen_display_GUI)
    img_chosen_display_as_label.image = img_chosen_display_GUI  # avoid garbage collection


def back():
    # Have to either reload original image or delete added text
    # Image on GUI not resetting
    global im, im_unedited, edit_img_button
    global w_font, w_x_y_pos, size_label, font_label, scale, img_chosen_display_as_label, img_chosen_display_GUI
    im = im_unedited
    img_chosen_display_GUI = ImageTk.PhotoImage(im_unedited)

    font_label.pack_forget()
    font_selected.pack_forget()
    back_button.pack_forget()
    save_image_button.pack_forget()
    fixed_x_y_pos.pack_forget()

    submit_watermark_text_button.pack()
    w_text.pack()
    font_label.pack()
    font_label.config(text="1.Font? Choose with wisdom")
    w_font.pack()
    size_label.pack()
    scale.pack()

    x_y_pos_label.pack()
    custom_position_or_premade.pack()
    custom.config(text="3.1.Custom Positions: TAKE NOTE OF PHOTO DIMENSIONS (eg: X<=1920, Y<=1080)")
    # custom.pack()
    # premade.pack()
    img_chosen_display_as_label.pack_forget()
    img_chosen_display_as_label = ttk.Label(window, image=img_chosen_display_GUI)
    img_chosen_display_as_label.image = img_chosen_display_GUI
    img_chosen_display_as_label.bind('<Configure>', resize_image)
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)


# How to let use save watermarked image/file?
# Tkinter save image as file
def save_img():
    global im
    directory_saved = tkinter.filedialog.askdirectory()  # initialdir="/path/to/start")
    print(directory_saved)
    img_saved = tkinter.filedialog.asksaveasfilename()

    # FILE_PATH = "C:/Users/Chua/Desktop/"
    # FILE_PATH = "C:/Users/Chua/Desktop/WEB DEVELOPER COURSE/#100 Days of Code- The Complete Python Pro Bootcamp for 2022 #ANGELAYU/#84 #PF Image Watermarking Desktop App"
    im.save(f"{img_saved}.png", "PNG")


# Let user choose where and what text to add (Tkinter dropdown box or something)
# pillow python add text
# python pillow add image to image
def add_watermark():
    global scale, im, img_chosen_display_as_label, w_font, w_text, WATERMARK_FONT, WATERMARK_TEXT, WATERMARK_SIZE, WATERMARK_X_POS, WATERMARK_Y_POS
    global submit_watermark_text_button, size_label, font_label, scale, w_x_y_pos

    print("add_watermark")
    print(im)
    print(img_chosen_display_as_label)

    # INSTEAD OF PREDEFINING; LET USER CHOOSE USING TKINTER WIDGETS

    # WATERMARK_FONT = "arial.ttf"
    # WATERMARK_SIZE = 50
    # WATERMARK_X_POS = 1920/2-300
    # WATERMARK_Y_POS = 500
    # WATERMARK_TEXT = "COPYRIGHT WORLD"
    add_watermark_button.pack_forget()
    img_chosen_display_as_label.pack_forget()

    # Lets user enter watermark text; but need submit button
    submit_watermark_text_button.pack()
    # How to delete all text in tkinter text box once user start typing?
    # Tkinter select all text in textbox (All reference text will be cleared once user starts typing)
    w_text.insert(END, "Enter watermark text here")
    w_text.tag_add(SEL, "1.0", END)
    w_text.focus()
    w_text.pack()
    print(w_text.get("1.0", END))
    print(WATERMARK_TEXT)
    print("after submitting watermark text")

    # Message to get user to choose font

    font_label.pack()
    fonts = ["arial.ttf", "bahnschrift.ttf", "calibri.ttf", "consolas.ttf", "constantia.ttf", "gadugi.ttf"]
    for item in fonts:
        w_font.insert(fonts.index(item), item)
    # w_font.insert(END, "Enter watermark font here")
    # w_font.tag_add(SEL, "1.0", END)
    # w_font.focus()
    w_font.pack()
    # WATERMARK_FONT = "arial.ttf"
    # WATERMARK_FONT = "consolas.ttf"

    # WATERMARK_SIZE = 50
    # Message to let user know what the slider is for (size of watermark text)
    size_label.pack()
    scale.pack()
    custom_position_or_premade.pack()

    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)


def save_font_settings():
    # USE A BUTTON BCOS TOO MANY LISTBOXES WILL NOT SAVE CURRENT CURSOR SELECTION FROM EVENTS
    font_label.config(text="1.Font?", fg="light blue", font=("Arial", 20))
    # Tkinter listbox return string value (instead of print)
    global w_font, selected_font, img_chosen_display_as_label
    # Gets current selection from listbox
    print("save_font_settings")
    selected_font = (w_font.get(w_font.curselection()))
    print(selected_font)
    print(type(selected_font))

    img_chosen_display_as_label.pack_forget()
    size_label.pack_forget()
    scale.pack_forget()
    custom_position_or_premade.pack_forget()
    x_y_pos_label.pack_forget()
    w_x_y_pos.pack_forget()
    custom.pack_forget()
    premade.pack_forget()
    x_pos.pack_forget()
    y_pos.pack_forget()
    current_x_y_pos.pack_forget()
    fixed_x_y_pos.pack_forget()
    if selected_font != "":
        w_font.pack_forget()
        font_selected.config(text=f"{selected_font}")
        font_selected.pack()

    size_label.pack()
    scale.pack()
    custom_position_or_premade.pack()
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)
    return selected_font


# Button that spawns 2 buttons to let user choose mode for watermark position
def custom_position_or():
    global img_chosen_display_as_label, x_pos, y_pos, x_y_pos
    img_chosen_display_as_label.pack_forget()
    custom.pack()
    premade.pack()
    x_y_pos = ""
    x_pos.delete(1.0, END)
    x_pos.insert(END, "0")
    x_pos.tag_add(SEL, "1.0", END)
    x_pos.focus()
    y_pos.delete(1.0, END)
    y_pos.insert(END, "0")

    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)


# Returns input box (2x) for user to choose x/y positions for watermark
def custom_position():
    global img_chosen_display_as_label, WATERMARK_X_POS, WATERMARK_Y_POS
    custom_position_or_premade.pack_forget()
    premade.pack_forget()
    img_chosen_display_as_label.pack_forget()
    custom.config(text="3.1.CLICK to submit custom positions- TAKE NOTE OF PHOTO DIMENSIONS (eg: X<=1920, Y<=1080)")
    current_x_y_pos.pack()
    WATERMARK_X_POS = x_pos.get("1.0", END)
    WATERMARK_X_POS = int(WATERMARK_X_POS)
    print(f"CUSTOM POSITION (X= {WATERMARK_X_POS})")
    WATERMARK_Y_POS = y_pos.get("1.0", END)
    WATERMARK_Y_POS = int(WATERMARK_Y_POS)
    print(f"CUSTOM POSITION (Y= {WATERMARK_Y_POS})")
    x_pos.pack()
    y_pos.pack()
    current_x_y_pos.config(text=f"X:{WATERMARK_X_POS} Y:{WATERMARK_Y_POS}")
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)


# Returns list of premade positions ( BUG: LISTBOX NOT OUTPUTTING VALUES FIRST TIME ITS BEING CLICKED)
def premade_position():
    global img_chosen_display_as_label, WATERMARK_X_POS, WATERMARK_Y_POS, fixed_x_y_pos, x_y_pos
    custom_position_or_premade.pack_forget()
    custom.pack_forget()
    img_chosen_display_as_label.pack_forget()
    general_locations_x_y = ["Top Left", "Top Middle", "Top Right", "Middle Left", "Middle", "Middle Right",
                             "Bottom Left", "Bottom Middle", "Bottom Right"]
    for item in general_locations_x_y:
        w_x_y_pos.insert(general_locations_x_y.index(item), item)
    x_y_pos_label.pack()

    w_x_y_pos.pack()
    print(f"x_y_pos: {x_y_pos}?")
    if x_y_pos != "":
        w_x_y_pos.pack_forget()
    if x_y_pos == "Top Left":
        WATERMARK_X_POS = 100
        WATERMARK_Y_POS = 100
    elif x_y_pos == "Top Middle":
        WATERMARK_X_POS = 1920 / 2 - 100
        WATERMARK_Y_POS = 100
    elif x_y_pos == "Top Right":
        WATERMARK_X_POS = 1700
        WATERMARK_Y_POS = 100
    elif x_y_pos == "Middle Left":
        WATERMARK_X_POS = 100
        WATERMARK_Y_POS = 600
    elif x_y_pos == "Middle":
        WATERMARK_X_POS = 1920 / 2 - 100
        WATERMARK_Y_POS = 600
    elif x_y_pos == "Middle Right":
        WATERMARK_X_POS = 1700
        WATERMARK_Y_POS = 600
    elif x_y_pos == "Bottom Left":
        WATERMARK_X_POS = 100
        WATERMARK_Y_POS = 1000
    elif x_y_pos == "Bottom Middle":
        WATERMARK_X_POS = 1920 / 2 - 100
        WATERMARK_Y_POS = 1000
    elif x_y_pos == "Bottom Right":
        WATERMARK_X_POS = 1700
        WATERMARK_Y_POS = 1000
    else:
        print("LOCATION ERROR")
        # WATERMARK_X_POS = 1920 / 2 - 300
        # WATERMARK_Y_POS = 500

    fixed_x_y_pos.config(text=f"{x_y_pos}")
    fixed_x_y_pos.pack()
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)


def scale_used(value):
    global watermarkk_size
    watermarkk_size = value
    print(value)
    return watermarkk_size


def listbox_used_x_y(event):
    # Tkinter listbox return string value (instead of print)
    global w_x_y_pos, x_y_pos
    # Gets current selection from listbox
    print("listbox_used")
    x_y_pos = (w_x_y_pos.get(w_x_y_pos.curselection()))
    print(x_y_pos)
    print(type(x_y_pos))
    return x_y_pos


def listbox_used(event):
    # Tkinter listbox return string value (instead of print)
    global w_font, selected_font
    # Gets current selection from listbox
    print("listbox_used")
    selected_font = (w_font.get(w_font.curselection()))
    print(selected_font)
    print(type(selected_font))
    return selected_font


def submit_watermark_text():
    global im, WATERMARK_FONT, WATERMARK_TEXT, WATERMARK_SIZE, watermarkk_size, WATERMARK_X_POS, WATERMARK_Y_POS, w_text, w_font, img_chosen_display_as_label
    global submit_watermark_text_button, size_label, font_label, scale, selected_font, x_y_pos
    choose_image_button.pack_forget()
    submit_watermark_text_button.pack_forget()
    w_text.pack_forget()
    w_font.pack_forget()
    w_x_y_pos.pack_forget()
    size_label.pack_forget()
    scale.pack_forget()
    back_button.pack()
    x_y_pos_label.pack_forget()
    font_label.pack_forget()
    font_selected.pack_forget()
    custom.pack_forget()
    current_x_y_pos.pack_forget()
    x_pos.pack_forget()
    y_pos.pack_forget()
    premade.pack_forget()
    custom_position_or_premade.pack_forget()
    fixed_x_y_pos.pack_forget()

    print("submit_watermark_text")
    # ADDS TEXT (aft extracting from textbox); Can also add image; image on image then add text (but time consuming. just get the basic framework working)
    WATERMARK_TEXT = w_text.get("1.0", END)
    WATERMARK_FONT = selected_font  # FIXED; ASSIGNED WIDGET OUTPUT TO GLOBAL VAR #listbox function sending weird values 1636832369280listbox_used instead of string
    WATERMARK_SIZE = int(watermarkk_size)

    # WATERMARK_FONT = w_font.get("1.0", END)
    print(f"WATERMARK_TEXT: {WATERMARK_TEXT}")
    print(f"WATERMARK_FONT: {WATERMARK_FONT}")
    print(f"WATERMARK_SIZE: {WATERMARK_SIZE}")
    print(f"WATERMARK_X_POS: {WATERMARK_X_POS}")
    print(type(WATERMARK_X_POS))
    print(f"WATERMARK_Y_POS: {WATERMARK_Y_POS}")
    print(type(WATERMARK_Y_POS))

    img_chosen_display_as_label.pack_forget()  # UPDATE IMAGE WITH WATERMARK TO SHOW ON GUI
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)

    draw = ImageDraw.Draw(im)
    # Python Pillow use font that is not installed?/Python Pillow installed fonts
    try:
        font = ImageFont.truetype(WATERMARK_FONT, WATERMARK_SIZE, encoding="unic")
    except OSError or TypeError:
        font = ImageFont.truetype("arial.ttf", WATERMARK_SIZE, encoding="unic")
        font_label.config(text="Custom font not found! Defaulted to arial.ttf.")
        font_label.pack()
        print("Custom font not found! Defaulted to arial.ttf. ")
    draw.text((WATERMARK_X_POS, WATERMARK_Y_POS), WATERMARK_TEXT, font=font,fill="#6b1143")
    # TEST VALUES
    # draw.text((100, 100), "100, 100", font=font)
    # draw.text((200, 200), "200, 200", font=font)
    # draw.text((300, 300), "300, 300", font=font)
    # draw.text((400, 400), "400, 400", font=font)
    # draw.text((500, 500), "500,500", font=font)
    # draw.text((600, 600), "600, 600", font=font)
    # draw.text((700, 700), "700, 700", font=font)
    # draw.text((800, 800), "800, 800", font=font)
    # draw.text((900, 900), "900, 900", font=font)
    # draw.text((1000, 1000), "1000, 1000", font=font)
    # draw.text((1600, 100), "1600, 100", font=font)

    submit_watermark_text_button.pack_forget()
    w_text.pack_forget()
    save_image_button.pack()

    img_chosen_display_as_label.pack_forget()  # UPDATE IMAGE WITH WATERMARK TO SHOW ON GUI
    img_chosen_display_as_label.pack(fill=BOTH, expand=YES)
    print("watermark added!")


# TKINTER WIDGETS
# choose_image_button = Button(text="Picture of choice?", fg="light blue", bg="brown", font=("Arial", 20),
#                              highlightthickness=0, command=choose_img)
choose_image_button = Button(text="Picture of choice?", fg="red", bg="#353b36", font=("Arial", 20),
                             highlightthickness=0, command=choose_img)
choose_image_button.pack()

back_button = Button(text="EDIT OPTIONS", fg="red", bg="#353b36", font=("Arial", 20),
                     highlightthickness=0, command=back)

add_watermark_button = Button(text="Click to add desired watermark", fg="light blue", bg="#353b36", font=("Arial", 20),
                              highlightthickness=0, command=add_watermark)
submit_watermark_text_button = Button(text="Click to submit watermark text", fg="red", bg="#353b36", font=("Arial", 20),
                                      highlightthickness=0, command=submit_watermark_text)

edit_img_button = Button(text="EDIT YOUR PICTURE!", fg="red", bg="#353b36", font=("Arial", 18),
                         highlightthickness=0, command=edit_img)
save_image_button = Button(text="Save picture?", fg="green", bg="#353b36", font=("Arial", 15),
                           highlightthickness=0, command=save_img)

# TEXT INPUT
w_text = Text(height=5, width=30)

# TEXT FONT
font_label = Button(text="1.CLICK TO SAVE FONT", bg="#353b36", fg="red",
                    font=("Arial", 15), command=save_font_settings)
font_selected = Label(text=f"Font: {selected_font}", bg="#353b36", fg="light blue",
                      font=("Arial", 10))
w_font = Listbox(height=6)
w_font.bind("<<ListboxSelect>>", listbox_used)
# w_font = Text(height=5, width=30)

# TEXT SIZE
size_label = Label(text="2.Watermark Text Size?", bg="#353b36", fg="light blue",
                   font=("Arial", 15))
scale = Scale(from_=8, to=100, orient="horizontal", command=scale_used)

# ALLOW CHOICE OF FIXED OR FLEXIBLE PLACEMENT OF WATERMARK
custom_position_or_premade = Button(text="3.CHOOSE YOUR MODE", fg="red", bg="#353b36", font=("Arial", 15),
                                    highlightthickness=0, command=custom_position_or)

# CUSTOM POSITION PLACING
custom = Button(text="3.1.Custom Positions", fg="red", bg="#353b36",
                font=("Arial", 15),
                highlightthickness=0, command=custom_position)
current_x_y_pos = Label(text=f"X:{WATERMARK_X_POS} Y:{WATERMARK_Y_POS}", bg="#353b36", fg="light blue",
                        font=("Arial", 10))
x_pos = Text(height=1, width=20)
y_pos = Text(height=1, width=20)

# FIXED POSITION PLACING
w_x_y_pos = Listbox(height=9)
w_x_y_pos.bind("<<ListboxSelect>>", listbox_used_x_y)

premade = Button(text="3.2.Premade Positions", fg="red", bg="#353b36", font=("Arial", 15),
                 highlightthickness=0, command=premade_position)
x_y_pos_label = Label(text="Position?", bg="#353b36", fg="light blue",
                      font=("Arial", 10))
fixed_x_y_pos = Label(text=f"{x_y_pos}", bg="#353b36", fg="light blue",
                      font=("Arial", 10))

window.mainloop()
