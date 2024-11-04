import customtkinter
import pyperclip
import random
import math

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#000000", width=500, height=600, **kwargs)
        
        self.label = customtkinter.CTkLabel(self, text="Password Generator", font=("Helvatica", 48, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=(30,40))
        
        self.border_frame = customtkinter.CTkFrame(self, fg_color="#ffffff", width=400, height=50)
        self.border_frame.grid(row=1, column=0, columnspan=2, padx=2, pady=3)
        
        self.border_frame.grid_propagate(False)
        
        self.display_password = customtkinter.CTkLabel(self.border_frame, text="Generate a password", font=("Helvetica", 18), fg_color="#ffffff", text_color="#d9d9d9")
        self.display_password.grid(row=0, column=0, padx=4, pady=8) 
        
        self.copy_password = customtkinter.CTkButton(self, text="copy", command=self.copy, fg_color="#28a745", hover_color="#218838")
        self.copy_password.grid(row=2, column=1, pady=(20, 10))
        
        self.generate_pass = customtkinter.CTkButton(self, text="Generate", command=self.generate_password, fg_color="#28a745", hover_color="#218838")
        self.generate_pass.grid(row=2, column=0, pady=(20, 10))
        
    def generate_password(self):
        length = 12
        UPPER = "ABCDFGHIJKLMNOPQRSTUVWXYZ"
        LOWER = "abcdefghijklmnopqrstuvwxyz"
        NUM = "0123456789"
        SYMBOL = "@#!~%^*()_+<>?-="
        all_char = UPPER + LOWER + NUM + SYMBOL
            
        password = [
            random.choice(UPPER),
            random.choice(LOWER),
            random.choice(NUM),
            random.choice(SYMBOL)
        ]
        
        while len(password) < length:
            password.append(random.choice(all_char))
        
        random.shuffle(password)  
        self.password = ''.join(password)
        self.display_password.configure(text=f"{self.password}" , text_color="#000000")
        
    def copy(self):
        pyperclip.copy(self.password)
        print("Password copied to clipboard!")
        
        
        
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x500")
        self.title("Password Generator")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
            
        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, sticky="nsew")    

app = App()
app.mainloop()