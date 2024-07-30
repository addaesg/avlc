import customtkinter
from CTkTable import *


def main(): 
    customtkinter.set_appearance_mode("System")
    customtkinter.set_default_color_theme("blue")  

    app = customtkinter.CTk()  
    app.geometry("800x300")

    value = [["Basic", "Z", "x1", "x2", "s1", "s2", "s3", "Solution", "Intercept"],
                ["Z", 1, -2, -3, 0, 0, 0, 0, 0],
                ["s1", 0, 1, 1, 1, 0, 0, 4, 4],
                ["s2", 0, 3, 1, 0, 1, 0, 6, 6],
                ["s3", 0, 1, 2, 0, 0, 1, 5, 5]]
    
    table = CTkTable(master=app, values=value)
    table.pack(expand=True, fill="x", pady=10, padx=10)
    table.configure(header_color="gray", hover_color="light blue")

    next_button = customtkinter.CTkButton(app, text="Next Step")
    next_button.pack(pady=10)
    app.mainloop()

if __name__ == "__main__":
    main()