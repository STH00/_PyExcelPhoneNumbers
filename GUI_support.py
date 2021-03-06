# By Stephen Harrison
# GUI generated by PAGE

# This file is used to extend functionality of the form

import sys
import re
import pandas
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global combobox
    combobox = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

# Function which closes the window.
def destroy_window():
    global top_level
    top_level.destroy()
    top_level = None



# Primary File button action classed to clone function easily
# Separate class/function to keep dataframe loaded, prevent variable issues
class PrimaryFile:
    def ComboboxUpdate(self, TextBox, ComboboxName, ComboboxPhone):
        TextBox.delete("1.0", "end")

        file = tk.filedialog.askopenfilename(title="Select A File",filetypes=(("Excel File", "*.xlsx"),("All Files", "*.*")))
        TextBox.insert(tk.INSERT,file)
        filepath = (TextBox.get("1.0", "end")).rstrip()
        
        global df_primary
        df_primary = pandas.read_excel(filepath, sheet_name=0)
        count = 1

        for column in df_primary:
            if count == 1:
                ComboboxName.set(column)
                ComboboxPhone.set(column)
            ComboboxName['values'] = (*ComboboxName['values'], column)
            ComboboxPhone['values'] = (*ComboboxPhone['values'], column)
            count += 1

# New File button action classed to clone function easily
# Separate class/function to keep dataframe loaded, prevent variable issues
class NewFile:
    def ComboboxUpdate(self, TextBox, ComboboxName, ComboboxPhone): 
        TextBox.delete("1.0", "end")

        file = tk.filedialog.askopenfilename(title="Select A File",filetypes=(("Excel File", "*.xlsx"),("All Files", "*.*")))
        TextBox.insert(tk.INSERT,file)
        filepath = (TextBox.get("1.0", "end")).rstrip()
        
        global df_newinfo
        df_newinfo = pandas.read_excel(filepath, sheet_name=0)
        count = 1

        for column in df_newinfo:
            if count == 1:
                ComboboxName.set(column)
                ComboboxPhone.set(column)
            ComboboxName['values'] = (*ComboboxName['values'], column)
            ComboboxPhone['values'] = (*ComboboxPhone['values'], column)
            count += 1

# Run button action class
# Separate class to prevent variable issues
class RunEvent:
    def ButtonRun_Click(self, primary_name, primary_phone, newinfo_name, newinfo_phone, progressbar):
        
        dfp = df_primary
        dfp = dfp.set_index(primary_name)
        
        dfn = df_newinfo
        dfn = dfn.set_index(newinfo_name)

        progress_count = 0

        for pri_name in dfp.index:
            progress_count += 1
            progress_total = (progress_count / len(dfp.index)) * 100
            progressbar['value'] = progress_total
            print(progress_total)
            for new_name in dfn.index:
                result = fuzz.token_set_ratio(str(pri_name), str(new_name))
                
                if pandas.isna(pri_name) == False or pandas.isna(new_name) == False:
                    if result >= 85:
                        newphone_result = dfn.loc[new_name,newinfo_phone]
                        strip_newphone = str(newphone_result).replace("-","")
                        
                        if len(strip_newphone) == 4:
                            dfp.loc[pri_name,primary_phone] = "804523{}".format(strip_newphone)
                            print("{}: {}".format(pri_name, dfp.loc[pri_name,primary_phone]))

                        elif len(strip_newphone) == 7:
                            dfp.loc[pri_name,primary_phone] = "804{}".format(strip_newphone)
                            print("{}: {}".format(pri_name, dfp.loc[pri_name,primary_phone]))

                        elif len(strip_newphone) == 10:
                            dfp.loc[pri_name,primary_phone] = strip_newphone
                            print("{}: {}".format(pri_name, dfp.loc[pri_name,primary_phone]))

                        else:
                            print("**********\nBAD LENGTH MATCH: {}\n**********".format(strip_newphone))
                        
        # Output changes
        # export_file = tk.filedialog.asksaveasfilename(title="Save File",filetypes=(("Excel File", "*.xlsx"),("All Files", "*.*")))
        # dfp.to_excel (export_file, index = True, header = True)
        export_file_path = tk.filedialog.asksaveasfilename(defaultextension='.xlsx')
        dfp.to_excel (export_file_path, index = True, header=True)