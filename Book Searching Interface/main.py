from tkinter import *
from tkinter import messagebox 
from PIL import ImageTk, Image
import requests
import urllib.parse
import io

# Constants
BLUE = '#2B2E4A'
VALVET = '#E84545'
CHERRY = '#903749'
BROWN = '#53354A'
MODERN_FONT = ("Comic Sans MS", 30, "bold")
MODERN_FONT_2 = ("Kanit", 12, "bold")

def search_internet_archive(query, num_results=5):
    base_url = 'https://archive.org/advancedsearch.php'
    params = {
        'q': query,
        'fl[]': 'identifier,title,creator,year,subject,description',
        'rows': num_results,
        'output': 'json'
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data['response']['docs']
    except requests.RequestException as e:
        print(f"Error: Unable to retrieve data - {e}")
        return []

def get_cover_image(identifier, size=(149, 220)):
    url = f"https://archive.org/services/img/{identifier}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(io.BytesIO(response.content))
        img = img.resize(size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error fetching image for {identifier}: {e}")
        return None

def show_menu(event):
    menu.post(event.x_root, event.y_root)

def search():
    query = search_entry.get()
    results = search_internet_archive(query)
    
    clear_previous_content()

    if not results:
        messagebox.showinfo("No Results", "No books found for the given query.")
        return

    for i, book in enumerate(results[:5]):
        identifier = book.get('identifier', '')
        title = book.get('title', 'Unknown Title')
        year = book.get('year', 'Unknown Year')
        creator = book.get('creator', 'Unknown Author')
        description = book.get('description', 'No description available')

        # Update text fields
        text[f'a{i+1}'].config(text=title)
        text[f'c{i+1}'].config(text=f"Year: {year}")
        text[f'd{i+1}'].config(text=f"Author: {creator}")

        # Fetch and display cover image
        cover_image = get_cover_image(identifier)
        if cover_image:
            image[f'b{i+1}'].config(image=cover_image)
            image[f'b{i+1}'].image = cover_image  # Keep a reference
        else:
            image[f'b{i+1}'].config(text="No Image")

def clear_previous_content():
    for i in range(1, 6):
        text[f'a{i}'].config(text="Book Title")
        text[f'c{i}'].config(text="Year: Unknown")
        text[f'd{i}'].config(text="Author: Unknown")
        image[f'b{i}'].config(image='', text="Loading...")

# Main application setup
root = Tk()
root.title("Page Pilot")
root.geometry('1250x750+200+100')
root.config(bg=BLUE)

screen = Canvas(root, width=1250, height=750, bg=BLUE, highlightthickness=0)
screen.create_text(625, 50, text="Welcome to Page Pilot!", font=MODERN_FONT, fill=VALVET, anchor='n')
screen.grid(row=0, column=0, columnspan=2)

# Load and place images
read_img = Image.open('assets//readerr.png')
res_img = read_img.resize((60, 60), Image.LANCZOS)
read_new = ImageTk.PhotoImage(res_img)
screen.create_image(350, 80, image=read_new)

icon_img = PhotoImage(file='assets//readerr.png')
root.iconphoto(False, icon_img)

read_g = Image.open('assets//std_read.png')
res_girl = read_g.resize((150, 160), Image.LANCZOS)
res_new = ImageTk.PhotoImage(res_girl)
screen.create_image(110, 110, image=res_new)

# Search entry and button
search_entry = Entry(root, text="Search Book", bg='white', fg=CHERRY, font=MODERN_FONT, highlightthickness=0, width=25)
search_entry.place(x=590, y=120, anchor='n')
search_entry.focus()

search_image = Image.open('assets//search.png')
rezise_image_search = search_image.resize((55, 55), Image.LANCZOS)
searcH_new = ImageTk.PhotoImage(rezise_image_search)

search_button = Button(root, image=searcH_new, highlightthickness=0, bg=BLUE, cursor='hand2', command=search)
search_button.place(x=920, y=120, anchor='n')

# Settings button
set_img = Image.open('assets//SETTING.png')
rezise_image_setting = set_img.resize((55, 55), Image.LANCZOS)
set_new = ImageTk.PhotoImage(rezise_image_setting)
set_button = Button(root, image=set_new, highlightthickness=0, bg=BLUE, cursor='hand2')
set_button.place(x=1020, y=120, anchor='n')
set_button.bind("<Button-1>", show_menu)

# Settings menu
menu = Menu(root, tearoff=0)
check_var = BooleanVar()
menu.add_checkbutton(
    label="Publish Date",
    variable=check_var,
    command=lambda: print(f"Check option is {'checked' if check_var.get() else 'unchecked'}")
)
check_var2 = BooleanVar()
menu.add_checkbutton(
    label="Rating",
    variable=check_var2,
    command=lambda: print(f"Rating Check option is {'checked' if check_var2.get() else 'unchecked'}")
)

# Logout button
log = Image.open('assets//logout.png')
reslog = log.resize((35, 35), Image.LANCZOS)
screen.create_text(1210, 60, text="Logout", font=MODERN_FONT_2, fill=CHERRY, anchor='n')
setlog = ImageTk.PhotoImage(reslog)
set_but_log = Button(root, image=setlog, highlightthickness=0, bg=BLUE, cursor='hand2', command=lambda: root.destroy())
set_but_log.place(x=1210, y=20, anchor='n')

# Frames for book display
frames = []
for i in range(1, 6):
    frame = Frame(root, height=240, width=150, bg='white')
    frame.place(x=160 + (i-1)*200, y=350)
    frames.append(frame)

    frame2 = Frame(root, height=50, width=150, bg='white')
    frame2.place(x=160 + (i-1)*200, y=600)
    frames.append(frame2)

# Initialize text and image dictionaries
text = {}
image = {}

for i in range(1, 6):
    text[f'a{i}'] = Label(frames[2*i-2], text="Book Title", font=("Arial", 10), fg='green')
    text[f'c{i}'] = Label(frames[2*i-1], text="Year: Unknown", font=("arial", 10), bg="#e6e6e6")
    text[f'd{i}'] = Label(frames[2*i-1], text="Author: Unknown", font=("Arial", 10), fg='black')
    image[f'b{i}'] = Label(frames[2*i-2], text="Loading...")

    text[f'a{i}'].place(x=10, y=4)
    text[f'c{i}'].place(x=10, y=4)
    text[f'd{i}'].place(x=20, y=30)
    image[f'b{i}'].place(x=3, y=30)

root.mainloop()

''' OLD VERSION
# # Frame
frame1 = Frame(root , height= 240 , width=150 , bg= 'white')
frame2 = Frame(root , height= 240 , width=150 , bg= 'white')
frame3 = Frame(root , height= 240 , width=150 , bg= 'white')
frame4 = Frame(root , height= 240 , width=150 , bg= 'white')
frame5 = Frame(root , height= 240 , width=150 , bg= 'white')
frame1.place(x = 160 , y = 350)
frame2.place(x = 360 , y = 350)
frame3.place(x = 560 , y = 350)
frame4.place(x = 760 , y = 350)
frame5.place(x = 960 , y = 350)

# #second frame

frame11 = Frame(root , height= 50 , width=150 , bg= 'white')
frame22 = Frame(root , height= 50 , width=150 , bg= 'white')
frame33 = Frame(root , height= 50 , width=150 , bg= 'white')
frame44 = Frame(root , height= 50 , width=150 , bg= 'white')
frame55 = Frame(root , height= 50 , width=150 , bg= 'white')
# #book title 
# # Assuming you want to add description labels for the books
# text = {
#     'a1': Label(frame1, text="Book Title", font=("Arial", 10), fg='green'),
#     'a2': Label(frame2, text="Book Title", font=("Arial", 10), fg='green'),
#     'a3': Label(frame3, text="Book Title", font=("Arial", 10), fg='green'),
#     'a4': Label(frame4, text="Book Title", font=("Arial", 10), fg='green'),
#     'a5': Label(frame5, text="Book Title", font=("Arial", 10), fg='green'),
#     'd1': Label(frame11, text="Description", font=("Arial", 10),fg='black'),
#     'd2': Label(frame22, text="Description", font=("Arial", 10), fg='black'),
#     'd3': Label(frame33, text="Description", font=("Arial", 10), fg='black'),
#     'd4': Label(frame44, text="Description", font=("Arial", 10), fg='black'),
#     'd5': Label(frame55, text="Description", font=("Arial", 10), fg='black'),
#     'c1': Label(frame11, text="date", font=("arial", 10), bg="#e6e6e6"),
#     'c2': Label(frame22, text="date", font=("arial", 10), bg="#e6e6e6"),
#     'c3': Label(frame33, text="date", font=("arial", 10), bg="#e6e6e6"),
#     'c4': Label(frame44, text="date", font=("arial", 10), bg="#e6e6e6"),
#     'c5': Label(frame55, text="date", font=("arial", 10), bg="#e6e6e6")
# }

# text['a1'].place(x=10 , y= 4)
# text['a2'].place(x=10 , y= 4)
# text['a3'].place(x=10 , y= 4)
# text['a4'].place(x=10 , y= 4)
# text['a5'].place(x=10 , y= 4)

# # Poster / Image of books
# image = {
#     'b1': Label(frame1),  # Add image or text as necessary
#     'b2': Label(frame2),
#     'b3': Label(frame3),
#     'b4': Label(frame4),
#     'b5': Label(frame5)
# }

# # Placing labels in frames
# for key, label in image.items():
#     label.place(x=3, y=30)
# #----------------------------------------------------------------------------------------------------------------------------------------------
frame11.place(x = 160 , y = 600)
frame22.place(x = 360 , y = 600)
frame33.place(x = 560 , y = 600)
frame44.place(x = 760 , y = 600)
frame55.place(x = 960 , y = 600)


# # Place Rating Labels with adjusted y-values to avoid overlap
# text['d1'].place(x=20, y=30)
# text['d2'].place(x=20, y=30)
# text['d3'].place(x=20, y=30)
# text['d4'].place(x=20, y=30)
# text['d5'].place(x=20, y=30)
# text['c1'].place(x=10, y=4)
# text['c2'].place(x=10, y=4)
# text['c3'].place(x=10, y=4)
# text['c4'].place(x=10, y=4)
# text['c5'].place(x=10, y=4)
'''