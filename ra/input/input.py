#Input Dialog via Text file or TextBox, retrieve_text is not yet working  properly. Eric(14-11-11)

import Tkinter as tk
import tkMessageBox

from readability.readabilityanalyzer import *
from tkFileDialog import *

name = ""
text = ""
url = "" 

def retrieve_text():
    name = pol_name.get()
    url = pol_url.get()
    text = pol_text.get("1.0",tk.END)
    name = str(name)
    url = str(url)
    text = str(text)
    finish_input(name, url, text)


def open_file():
    name = pol_name.get()
    url = pol_url.get()
    path = askopenfilename(filetypes=[("Text", ".txt")])
    path = str(path)
    f = open(path, 'r')
    text = f.read()
    f.close()

    finish_input(name, url, text)
 

def finish_input(name, url, text):
    if name != "" and text != "" and url != "":
        name = str(name)
        text = str(text)
        url = str(url)
        save_db = True
        ra = ReadabilityAnalyzer()
        ra.generate_report(text, name, url, save_db)
        inp_wind.destroy()

    else:
        tkMessageBox.showwarning("Input Error", "Name or text of the Policy is empty.")


if __name__ == "__main__":
 
 save = -1
 # Create window 
inp_wind = tk.Tk()

pol_space1 = tk.Label(inp_wind, text="")
pol_space1.pack()

pol_labeln = tk.Label(inp_wind, text="Enter name of the Policy you want to add:")
#pol_labeln.grid(row=0, column=1)
pol_labeln.pack()

# Creat Iput for name
pol_name = tk.Entry(inp_wind, width=70) 
pol_name.grid(row=1, column=1)
pol_name.pack()

pol_space1 = tk.Label(inp_wind, text="")
pol_space1.pack()

pol_labeln = tk.Label(inp_wind, text="Enter the URL of the Policy you want to add:")
pol_labeln.pack()

# Create Iput for url
pol_url = tk.Entry(inp_wind, width=70) 
pol_url.pack()

pol_space1 = tk.Label(inp_wind, text="")
pol_space1.pack()

# Create label
pol_labelt = tk.Label(inp_wind, text="Enter the Policy text")
pol_labelt.pack()

# Create text box
pol_text = tk.Text(inp_wind, width=70)
pol_text.pack()

pol_space1 = tk.Label(inp_wind, text="")
pol_space1.pack()

# Create button
pol_button = tk.Button(inp_wind, text="Save Policy Text", command=retrieve_text)
pol_button.pack()

pol_labelor = tk.Label(inp_wind, text="or")
pol_labelor.pack()

# Create button
pol_button2 = tk.Button(inp_wind, text="Open Text File (*.txt) to import text", command=open_file)
pol_button2.pack()

pol_space1 = tk.Label(inp_wind, text="")
pol_space1.pack()

pol_checkbox = tk.Checkbutton(inp_wind, text = "Speichern?",  variable = save, onvalue = 1, offvalue = 0)
pol_checkbox.pack()

pol_space1 = tk.Label(inp_wind, text="")
pol_space1.pack()

# Initialize GUI loop
inp_wind.title("Privacy Policy - Input")
inp_wind.minsize(640, 400)
inp_wind.mainloop()