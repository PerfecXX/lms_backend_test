from tkinter import *
from tkinter import ttk, filedialog, messagebox
import mysql.connector
import pandas as pd
from datetime import datetime


# Initialize function

def event_fill(text):
    Log.configure(state="normal")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    Log.insert(INSERT, str("\n({}) {}\n").format(current_time, text))
    Log.configure(state="disabled")


def update_db(target):
    sql = "UPDATE stock SET amount = amount-1 WHERE PDS_KB_NO =" + "\'" + target + "\'"
    event_fill(sql)
    MyCursor.execute(sql)
    MyDatabase.commit()


def start():
    global Index
    InjectButton.configure(state="disable")
    child_id = TreeView.get_children()[Index]
    TreeView.focus(child_id)
    TreeView.selection_set(child_id)
    data1 = TreeView.item(child_id)["values"][0]
    # data2 = TreeView.item(child_id)["values"][1]
    # data3 = TreeView.item(child_id)["values"][2]
    update_db(data1)
    TreeView.see(child_id)
    Index += 1
    if Index != NumberOfRow:
        root.after(60000, start)
    else:
        event_fill("Update complete")
        InjectButton.configure(state="normal")
        return None


def Browse_CSV():
    global CSVFile
    """This Function will open the file explorer and assign the chosen file path to label_file"""
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select A File",
                                          filetype=(("csv files", "*.csv"), ("All Files", "*.*")))
    CSVFile = filename
    if CSVFile != "":
        event_fill("Browsing File>> {}".format(CSVFile))
        event_fill("Ready to Load!")
    return None


def Load_CSV_data():
    global CSVFile
    global NumberOfRow
    """If the file selected is valid this will load the file into the TreeView"""
    file_path = CSVFile
    try:
        csv_filename = r"{}".format(file_path)
        if csv_filename[-4:] == ".csv":
            df = pd.read_csv(csv_filename)
        else:
            df = pd.read_excel(csv_filename)

    except ValueError:
        messagebox.showerror("Information", "The file you have chosen is invalid")
        return None
    except FileNotFoundError:
        messagebox.showerror("Information", f"No such file as {file_path}")
        return None

    clear_data()
    TreeView["column"] = list(df.columns)
    TreeView["show"] = "headings"
    for column in TreeView["columns"]:
        TreeView.heading(column, text=column)  # let the column heading = column name

    df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
    for row in df_rows:
        TreeView.insert("", "end",
                        values=row)  # inserts each list into the TreeView
        NumberOfRow += 1
    event_fill("{} row load Complete!".format(NumberOfRow))
    event_fill("Press Start button to update the database")
    return None


def clear_data():
    TreeView.delete(*TreeView.get_children())
    event_fill("Clear all CSV data")
    return None


# -----------------------------------------------------------
# Initialize variable
MyDatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="lms"
)
MyCursor = MyDatabase.cursor()
NumberOfRow = 0
CSVFile = " "
Index = 0
# -----------------------------------------------------------
# Initializing GUI
# Main Window
root = Tk()
app = ttk
root.title("TPS backend")
root.minsize(800, 600)
root.resizable(0, 0)
root.pack_propagate(False)
# -----------------------------------------------------------
# CSV frame and table
CSVFrame = LabelFrame(master=root, text="CSV data")
CSVFrame.place(height=350, width=600)

TreeView = app.Treeview(CSVFrame)
TreeView.place(relheight=1, relwidth=1)

TreeScrollY = app.Scrollbar(CSVFrame, orient="vertical", command=TreeView.yview)
TreeScrollX = app.Scrollbar(CSVFrame, orient="horizontal", command=TreeView.xview)
TreeView.configure(xscrollcommand=TreeScrollX.set, yscrollcommand=TreeScrollY.set)
TreeScrollX.pack(side="bottom", fill="x")
TreeScrollY.pack(side="right", fill="y")
# -----------------------------------------------------------
# Event log frame
LogFrame = LabelFrame(text="Event Log")
LogFrame.place(rely=0.6, relx=0, height=220, width=795)

LogScrollY = Scrollbar(LogFrame)
LogScrollY.place(y=0, x=765, height=200)
LogScrollX = Scrollbar(LogFrame, orient=HORIZONTAL)
LogScrollX.place(y=183, x=0, width=720)

Log = Text(LogFrame, yscrollcommand=LogScrollY.set, xscrollcommand=LogScrollX.set)
Log.place(x=0, y=0, width=760, height=175)
LogScrollY.config(command=Log.yview)
LogScrollX.config(command=Log.xview)
Log.configure(state="disable")
# -----------------------------------------------------------
# Option frame
OpMenu = LabelFrame(master=root, text="Option")
OpMenu.place(rely=0, relx=0.78, height=350, width=170)

# Button in option frame
OpenCSVButton = Button(OpMenu, text="Browse A File", command=lambda: Browse_CSV())
OpenCSVButton.place(rely=0.01, relx=0, width=165)

LoadCSVButton = Button(OpMenu, text="Load CSV", command=lambda: Load_CSV_data())
LoadCSVButton.place(rely=0.1, relx=0, width=165)

ClearCSVButton = Button(OpMenu, text="Clear CSV", command=lambda: clear_data())
ClearCSVButton.place(rely=0.2, relx=0, width=165)

InjectButton = Button(OpMenu, text="Start", command=lambda: start())
InjectButton.place(rely=0.3, relx=0, width=165)
root.mainloop()
