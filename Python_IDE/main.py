"""THIS IDLE IS CREATED BY ANIRBAN SARKAR @10/10/24"""
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename , asksaveasfilename
import subprocess


file_path = ''
def save_file_path(path):
    global file_path
    file_path = path
def openfile():
    path = askopenfilename(filetypes=[('Python Files','*.py')])
    with open (path, 'r') as file:
        code = file.read()
        code_input.delete('1.0',END)
        code_input.insert('1.0',code)
        save_file_path(path)
def savefile():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files','*.py')])
    else:
        path = file_path
    with open(path,'w') as file:
        code = code_input.get('1.0', END)
        file.write(code)
        save_file_path(path)
def runfile():
    if file_path=='':
        messagebox.showerror('Code on:Error','No file selected, save first!')
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command , stdout=subprocess.PIPE , stderr=subprocess.PIPE , shell= True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0', error)


# Create main window
root = Tk()
root.title("Code On")
root.geometry('1280x720+150+80')
root.configure(bg='#323846')
root.resizable(False, False)

# Code input area
code_input = Text(root, font=('consolas', 14),bg='#0B192C',fg='white')
code_input.place(x=180, y=0, width=680, height=720)

# Output code area
code_output = Text(root, font=('consolas', 15), bg='#323846', fg='lightgreen')
code_output.place(x=860, y=0, width=420, height=720)

# Load images for buttons
Open = PhotoImage(file='open.png')
Save = PhotoImage(file='save.png')
Run = PhotoImage(file='run.png')

# Create buttons with images
Button(root, image=Open, bg='#323846', bd=0, command=openfile).place(x=30, y=30)
Button(root, image=Save, bg='#323846', bd=0, command=savefile).place(x=30, y=145)
Button(root, image=Run, bg='#323846', bd=0,command=runfile).place(x=30, y=260)




root.mainloop()
'''
IDLE is an Integrated Development and Learning Environment (IDE) for Python, while an IDE is a software application that helps programmers develop code
'''