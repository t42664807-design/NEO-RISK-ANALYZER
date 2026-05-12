import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)      #sharpens window
import tkinter as tk
from tkinter import ttk
import requests
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import date
API_KEY = "oomEEyKZlhMoqUQy4IWFx4KwUchNhngUoRtJKJT8"


root = tk.Tk()                      # Create main window
root.title("NEO Risk Analyzer")
root.geometry("1500x900+100+50")
root.resizable(False, False)
root.config(bg="#96b6c5")
#root.iconbitmap("C:\\Users\\HP\\OneDrive\\Desktop\\New folder\\NEO.ico.ico")

top = tk.Frame(root,bg="#fff8f0",height=150,)           #top frame
top.pack(side="top", fill='x',pady=(10,10),padx=(10,10))
top.pack_propagate(False)


bleft = tk.Frame(root, bg='#fff8f0', width=500 ,height=800)     #bottom_left frame
bleft.pack(side='left', fill='y',padx=(10,10),pady=(0,10))
bleft.pack_propagate(False)

bottom = tk.Frame(root, bg='#050e3c',width=1500,height=600 )        #bottom frame
bottom.pack(side='bottom', fill='x',pady=(10,10),padx=(0,10))
bottom.pack_propagate(False)

mright = tk.Frame(root, bg='#050e3c', width=1500, height=150 )      #middle_right frame
mright.pack(side='left',fill='both',expand=True,padx=(0, 10))
mright.pack_propagate(False)

top.grid_columnconfigure(0, weight=0)           #keep frame constant so adding grid won't resize frame
top.grid_columnconfigure(1, weight=0)
top.grid_rowconfigure(1, weight=0)
top.grid_rowconfigure(0, weight=0)
tk.Label(top, text="NEO RISK ANALYZER",font=("Segoe UI", 20, "bold"),bg="#fff8f0",fg="#384959").grid(row=0, column=0,sticky='w',padx=(20,0),pady=(20,10))           #adding data into frame
tk.Label(top, text="Near-Earth Object Threat Detection & Analysis",font=("Segoe UI", 10, "bold"),bg="#fff8f0",fg="#384959",justify='left').pack(side="top",padx=(0, 380), pady=(38,0))
tk.Label(top, text='This application uses NASA’s Near-Earth Object (NEO) API to retrieve real-time asteroid data for monitoring and analyzing impact risks.',font=("Segoe UI", 10, "bold"),bg="#fff8f0",fg="#384959",justify="left",wraplength=800).grid(row=1, column=0,pady=(10,10),padx=(20,0))

tk.Label(bottom, text="Radar chart",font=("Segoe UI", 16, "bold"),bg="#050e3c",fg="white").pack(pady=(20,10),padx=(350,0))

for i in range(3):
    mright.grid_columnconfigure(i, weight=1)

l1=tk.Label(mright, text="Velocity: ", bg="#050e3c", fg="white",font=("Helvetica", 10,"bold"))      #adding data into middle_right frame
l1.grid(row=1, column=2, sticky="w",padx=(20,10),pady=(20,10))
l2=tk.Label(mright, text="Id: ", bg="#050e3c", fg="white",font=("Helvetica", 10,"bold"))
l2.grid(row=0, column=0, sticky="w",padx=(10,10),pady=(20,10))
l3=tk.Label(mright, text="Miss_Distance: ", bg="#050e3c", fg="white",font=("Helvetica", 10,"bold"))
l3.grid(row=0, column=1, sticky="w",padx=(10,10),pady=(20,10),)
l4=tk.Label(mright, text="Hazardous: ", bg="#050e3c", fg="white",font=("Helvetica", 10, "bold","italic"))
l4.grid(row=0, column=2, sticky="w",padx=(20,10),pady=(20,10))
l5=tk.Label(mright, text="Max_Diameter: ", bg="#050e3c", fg="white",font=("Helvetica", 10,"bold"))
l5.grid(row=1, column=0, sticky="w",padx=(10,10),pady=(20,10))
l6=tk.Label(mright, text="Min_Diameter: ", bg="#050e3c", fg="white",font=("Helvetica", 10,"bold"))
l6.grid(row=1, column=1, sticky="w",padx=(10,10),pady=(20,10))

l7=tk.Label(bottom, text=" ", bg="#050e3c", fg="white", font=("Helvetica", 16, "bold"))
l7.pack(side='left',pady=(10,450),padx=20)

top.grid_rowconfigure(1, weight=0)
l8=tk.Label(bottom, text=" ", bg="#050e3c", fg="white", font=("Helvetica", 10),wraplength=350)
l8.grid(row=0,column=0,pady=(250,0),padx=20)
l9=tk.Label(bottom, text=" ", bg="#050e3c", fg="white", font=("Helvetica", 10),wraplength=400)
l9.grid(row=1,column=0,pady=(220,0))


tk.Label(bleft, text="Enter Date :",bg='#fff8f0',fg='#384959').grid(row=0,column=0,padx=(10,0),pady=(10,5))     #left_bottom frame

style = ttk.Style()
style.configure(
    "Modern.TEntry",
    relief="flat"
)
entry=ttk.Entry(bleft,width=15,style="Modern.TEntry", font=("Segoe UI", 10))    #entry search box
today = date.today().strftime("%Y-%m-%d")
entry.insert(0, today)   # puts current date in entry box by default yyyy-mm-dd
entry.grid(row=0,column=1,pady=(10,5),padx=(5,10))


listbox = tk.Listbox(           #adds listbox into bottom_left frame
    bleft,
    font=("Segoe UI", 12),
    width=500,
    bg="#96b6c5",        # dark background
    fg="#2c2c2c",
    selectbackground="#f3f4f4",
    selectforeground="black",
    activestyle="none",  # removes dotted selection box
    bd=0,                # remove border
    highlightthickness=0, # remove focus border
    relief="raised"
)
listbox.pack(side='top', fill="y",expand=True, pady=(60, 20), padx=(10, 10))

def on_motion(event):           #hover animation
    index = listbox.nearest(event.y)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
listbox.bind("<Motion>", on_motion)

canvas=None
def get_input():        #gets input from entry box
    d = entry.get()
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={d}&end_date={d}&api_key={API_KEY}"
    response = requests.get(url)
    data = response.json()
    neo_data = data["near_earth_objects"]
    asteroids = neo_data[d]


    listbox.delete(0, tk.END)

    for asteroid in range(len(asteroids)):          #adds data (asteroid names) into listbox
        listbox.insert(tk.END, "  "+asteroids[asteroid]['name'])

    def on_select(event):       #gets data from API and makes radar graph
        global canvas
        plt.close('all')
        if canvas:
            canvas.get_tk_widget().destroy()

        selected = listbox.get(listbox.curselection())
        selected=selected[2:]
        for asteroid in range (len(asteroids)): #data extraction
            if asteroids[asteroid]['name'] == selected:
                a=asteroids[asteroid]
                min_dia = a["estimated_diameter"]["meters"]["estimated_diameter_min"]
                max_dia = a["estimated_diameter"]["meters"]["estimated_diameter_max"]

                # Take first close approach data
                approach = a["close_approach_data"][0]

                # Miss distance (in lunar distance)
                miss_distance = float(approach["miss_distance"]["lunar"])
                miss_distancekm=float(approach["miss_distance"]["kilometers"])

                # Relative velocity (km/h)
                velocity = float(approach["relative_velocity"]["kilometers_per_second"])

                # Absolute magnitude (brightness)
                magnitude = a["absolute_magnitude_h"]
                labels = ["Min Dia", "Max Dia", "Miss Dist", "Velocity", "Magnitude"]

                # Values corresponding to labels
                values = [min_dia, max_dia, miss_distance, velocity, magnitude]

                l1.config(text=f"Velocity: {velocity:.2f} km/s")
                l2.config(text="Id: " + a['id'])
                l3.config(text=f"Miss_Distance: {miss_distancekm:.2f} km" )
                if a['is_potentially_hazardous_asteroid']:
                    l4.config(text="Hazardous: High Risk", fg="red")
                else:
                    l4.config(text="Hazardous: No Risk", fg="#7fff00")
                l5.config(text=f"Max_Diameter: {max_dia:.2f} m")
                l6.config(text=f"Min_Diameter: {min_dia:.2f} m")
                l7.config(text=f"Name: {selected}")
                l8.config(text=f'This spider plot visualizes normalized asteroid parameters on a 1–10 scale, including velocity, minimum and maximum diameter, miss distance (in lunar distance), and magnitude, enabling effective comparative analysis')



                #Making Radar Graph using matplotlib
                values.append(values[0])
                labels.append(labels[0])
                max_val = max(values)
                values = [(v / max_val)*10 for v in values]

                num_vars = len(labels)

                angles = np.linspace(0, 2 * np.pi, num_vars)

                fig=plt.figure(figsize=(6, 4))
                ax = fig.add_subplot(111, polar=True)

                ax.plot(angles, values)
                ax.fill(angles, values, alpha=0.1)
                ax.set_xticks(angles)
                ax.set_xticklabels(labels)
                ax.set_yticks([0, 2, 4, 6, 8, 10])
                canvas = FigureCanvasTkAgg(fig, master=bottom)
                canvas.draw()
                canvas.get_tk_widget().pack(side="right",padx=(0,20),pady=(0,50))


    listbox.bind("<<ListboxSelect>>", on_select)

# Button to trigger function
btn = tk.Button(bleft,text="Submit",command=get_input,font=("Arial", 7),width=6,height=1,bg="#1abc9c",fg="white",
    activebackground="#16a085",
    activeforeground="white",
    bd=0,
    relief="flat",
    cursor="hand2",
    highlightthickness=0
)
btn.grid(row=0,column=2,pady=(15,10),padx=(0,5))

#color change when clicking on botton
def on_enter(e):
    btn.config(bg="#16a085")

def on_leave(e):
    btn.config(bg="#1abc9c")

btn.bind("<Enter>", on_enter)
btn.bind("<Leave>", on_leave)

get_input()

def on_closing():
    plt.close('all')
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()  # Run the window