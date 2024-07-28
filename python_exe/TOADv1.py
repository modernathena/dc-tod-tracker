######################## Imports ########################

from requests import get
from time import sleep
from datetime import datetime
import ttkbootstrap as ttk # pip install ttkbootstrap
import threading

######################## Global Variables ########################

global running
running = False

######################## Functions ########################

def call_execute(): # multithreading prevents the main window from freezing
    submit_thread = threading.Thread(target=execute)
    submit_thread.daemon = True # ensures thread ends when window is closed

    # initializing & starting progress bar
    progress.grid(row=7, column=3, columnspan=3, padx=10, pady=5) # initializing the progress bar here makes it work
    progress.start()

    # starting the thread
    submit_thread.start()

def cancel_execute(): # cancel execution
    global running
    running = False # setting this to false will stop the while loop

def execute():
    # sets running to True, which allows while loop to run
    global running
    running = True

    # hides any error labels
    msg.grid_forget()

    c = code.get() # retrieves the value of the code field
    k = privKey.get() # retrieves the value of the private key field

    # error checks time interval
    try: # tries to convert to a float
        sleep(float(interval.get()))
    except: # runs if no option is selected
        progress.stop()
        progress.grid_forget()
        msg.config(text="Select a time interval.")
        msg.grid(padx=10, pady=10, row=7, column=3, columnspan=3)
        return
    # proceeds with error checking
    if len(c) == 4 or len(c) == 5: # ensures code is proper length
        # get request
        ref = f'https://dragcave.net/api/v2/dragon/{c}'
        req = get(ref, headers={'Authorization':f'Bearer {k}'}).json()
        if len(req['errors']) > 0: # catches any retrieval errors (such as the code not existing)
            progress.stop()
            progress.grid_forget()
            msg.config(text=f"Error: {req['errors'][0][1]}")
            msg.grid(padx=10, pady=5, row=7, column=3, columnspan=3)
        else:
            orighl = req['dragons'][c]['hoursleft'] # original hours remaining
            if orighl == -1: # fog check
                progress.stop()
                progress.grid_forget()
                msg.config(text="Egg is fogged!")
                msg.grid(padx=10, pady=5, row=7, column=3, columnspan=3)
            else:
                while running:
                    ref = f'https://dragcave.net/api/v2/dragon/{c}'
                    req = get(ref, headers={'Authorization':f'Bearer {k}'}).json()
                    timestamp = datetime.now()
                    newhl = req['dragons'][c]['hoursleft'] # hours remaining in most recent request
                    if newhl == orighl: # checks for tick down in hours remaining
                        sleep(float(interval.get()))
                    else:
                        progress.stop()
                        progress.grid_forget()
                        msg.config(text=f"{c}'s timer changes at XX:{timestamp.strftime("%M")}:{timestamp.strftime("%S")}")
                        msg.grid(padx=10, pady=10, row=7, column=3, columnspan=3)
                        break
                if running == False: # ensures that this block only runs if the cancel button was clicked
                    progress.stop()
                    progress.grid_forget()
                    msg.config(text="Canceled!")
                    msg.grid(padx=10, pady=10, row=7, column=3, columnspan=3)
                    return
    else:
        progress.stop()
        if len(c) == 0:
            msg.config(text="Enter a code.")
            msg.grid(padx=10, pady=5, row=7, column=3, columnspan=3)
            return
        else:
            msg.grid(padx=10, pady=5, row=7, column=3, columnspan=3)
            return
    return

######################## GUI ########################

# creating window & style
win = ttk.Window()
win.geometry("450x500")
style = ttk.Style("superhero")
win.title("TOAD")
win.columnconfigure(1, weight=3)
win.rowconfigure(1, weight=5)
win.columnconfigure(6, weight=5)
win.rowconfigure(8, weight=5)
win.rowconfigure(7, weight=1)

# API key input
ttk.Label(win, text="API Key").grid(sticky=ttk.E, row=3, column=2, padx=10)
privKey = ttk.Entry(win)
privKey.grid(row=3, column=3, columnspan=2, padx=10, pady=5)

# code input
ttk.Label(win, text="Code").grid(sticky=ttk.E, row=4, column=2, padx=10, pady=5)
code = ttk.Entry(win)
code.grid(row=4, column=3, columnspan=2, padx=10, pady=5)

# interval selector (https://www.pythontutorial.net/tkinter/tkinter-menubutton/)
ttk.Label(win, text="Refresh Interval").grid(sticky=ttk.E, row=5, column=2, padx=10, pady=5)
options = ("Time in Seconds",.1,.5,1,5,30,60)
interval = ttk.StringVar(win)
option_Menu = ttk.OptionMenu(win, interval, *options, bootstyle="secondary")
option_Menu.grid(sticky=ttk.W+ttk.E, row=5, column=3, columnspan=2, padx=10, pady=5)

# submit button
codeButton = ttk.Button(win, text="Submit", bootstyle="Success", command=call_execute).grid(sticky=ttk.E, padx=10, pady=10, row=6, column=3)

# cancel button
cancelButton = ttk.Button(win, text="Cancel", bootstyle="danger", command=cancel_execute).grid(sticky=ttk.W, pady=5, row=6, column=4)

# progress bar
progress = ttk.Progressbar(win, bootstyle='success-striped', orient='horizontal', mode='indeterminate')

# message label (for errors, success, etc)
msg = ttk.Label(win, text="default")

# compile the window
win.mainloop()