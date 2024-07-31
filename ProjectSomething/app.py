import customtkinter as ctk
from CTkTable import *
from simplex import Tableau

class SimplexApp(ctk.CTk):
    def __init__(self, master=None, tabluex=None):
        super().__init__()
        self.title("Simplex Method")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")  
        self.geometry("1x1")
        ## table 
        self.table_values = []
        self.t = tabluex
        self.t.setup()
        self.create_widgets()
    
    def update_size(self):
        self.big_frame.update_idletasks()
        width = self.big_frame.winfo_reqwidth() 
        height = self.big_frame.winfo_reqheight()
        self.geometry(f"{width}x{height}")

    def create_widgets(self):
        self.big_frame = ctk.CTkFrame(self)
        self.big_frame.pack(fill="both", expand=True)
        ## labels
        self.variables_frame = ctk.CTkFrame(self.big_frame)
        self.variables_frame.pack(pady=10)
        ## labels
        self.entering = ctk.CTkLabel(self.variables_frame, text="Entering: ", fg_color= "green")
        self.entering.pack(side="left", padx=10)
        self.leaving = ctk.CTkLabel(self.variables_frame, text="Leaving: ", fg_color= "red")
        self.leaving.pack(side="right", padx=10)
        ## progress bar
        self.progress = ctk.CTkProgressBar(self.big_frame, orientation="horizontal", width=600, height=13)
        self.progress.pack(pady=10, padx=10)   
        self.progress.set(0)
        ## table 
        self.sync_table_values()
        self.table = CTkTable(master=self.big_frame, values=self.table_values)
        self.table.pack(expand=False, fill="x", pady=10, padx=10)
        self.table.configure(header_color="gray", hover_color="light blue")
        ## button 
        self.button_frame = ctk.CTkFrame(self.big_frame)
        self.button_frame.pack(pady=10)
        self.next_button = ctk.CTkButton(self.button_frame, text="next step", command=self.next_step)
        self.next_button.pack(side="left", pady=10)
        self.reset_button = ctk.CTkButton(self.button_frame, text="X", command=self.reset, state="disabled")
        self.reset_button.configure(width=30, fg_color="red")
        self.reset_button.pack(side="right", pady=10)

        ## window geometry expand to fit
        self.update_size()

    def next_step(self):
        self.t.next_step()
        
        if(self.solution_found()):
            self.change_button_state(self.next_button, state="disabled", text="solved")
        self.change_button_state(self.reset_button, state="normal", text="X")
        self.sync_gui()
    
    def sync_gui(self):
        self.update_table_widget()
        self.update_variable_labels()
        self.update_progress_bar_widget()

    def reset(self):
        self.t.reset()
        self.change_button_state(self.reset_button, state="disabled", text="X")    
        self.change_button_state(self.next_button, state="normal", text="next step")
        self.sync_gui()
     
    ## 
    ## utils
    ## 
    def solution_found(self):
        return self.t._check()
    
    def is_running(self):
        return self.t.cur_step > 0

    def change_button_state(self, button, state="", text=""):
        button.configure(state=state, text=text)

    def update_variable_labels(self):
        self.entering.configure(text = "Entering: " + self.t.livre)
        self.leaving.configure(text = "Leaving: " + self.t.constrained)
    
    def update_progress_bar_widget(self):
        self.progress.set(self.t.cur_step/self.t.n_steps)

    def update_table_widget(self):
        self.sync_table_values()
        self.table.update_values(self.table_values)

    def sync_table_values(self):
        value = []
        value.append(self.t.header_tableau)
        value_row = []
        value_row.extend(self.format_row(self.t.obj))
        value_row[0] = "z"
        value.append(value_row)
        for i in range(len(self.t.rows)):
            value_row = []
            ## convert to string and truncate to 2 decimal places
            value_row.extend(self.format_row(self.t.rows[i]))
            
            value_row[0] = self.t.basic_variables[i]
            value.append(value_row)
        self.table_values = value #
    
    def format_row(self, row):
        return ["{0:.2f}".format(x) for x in row]