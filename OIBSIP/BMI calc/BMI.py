import customtkinter

class MyFrame(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#A9B6FF", width=500, height=600, **kwargs)
        
        self.label = customtkinter.CTkLabel(self, text="BMI Calculator", font=("Helvetica", 48, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, padx=20, pady=(30, 40))

        self.weight_label = customtkinter.CTkLabel(self, text="Weight (kg):", font=("Helvetica", 16, "bold"))
        self.weight_label.grid(row=1, column=0, padx=(30, 10), pady=5, sticky="e")
        
        self.weight_entry = customtkinter.CTkEntry(self, placeholder_text="Enter weight")
        self.weight_entry.grid(row=1, column=1, padx=(0, 30), pady=5)

        self.height_label = customtkinter.CTkLabel(self, text="Height (m):", font=("Helvetica", 16, "bold"))
        self.height_label.grid(row=2, column=0, padx=(30, 10), pady=5, sticky="e")
        
        self.height_entry = customtkinter.CTkEntry(self, placeholder_text="Enter height")
        self.height_entry.grid(row=2, column=1, padx=(0, 30), pady=5)

        self.calculate_button = customtkinter.CTkButton(self, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=3, column=0, columnspan=2, pady=(20, 10))

        self.result_label = customtkinter.CTkLabel(self, text="", font=("Helvetica", 18))
        self.result_label.grid(row=4, column=0, columnspan=2, padx=20, pady=30)
        

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            bmi = weight / (height ** 2)
            self.categorize_bmi(bmi)
        except ValueError:
            self.result_label.configure(text="Please enter valid numbers!", text_color="red")

    def categorize_bmi(self, bmi):
        if bmi < 18.5:
            self.result_label.configure(text=f"BMI: {bmi:.2f} - Underweight", text_color="#FF6347")
        elif 18.5 <= bmi <= 24.9:
            self.result_label.configure(text=f"BMI: {bmi:.2f} - Normal weight", text_color="#32CD32")
        else:
            self.result_label.configure(text=f"BMI: {bmi:.2f} - Overweight", text_color="#FFA500")


class MyFrame2(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#313549")

        self.my_frame = MyFrame(master=self)
        self.my_frame.grid(row=0, column=0, padx=100, pady=50)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("550x500")
        self.title("BMI Calculator App")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.my_frame2 = MyFrame2(master=self)
        self.my_frame2.grid(row=0, column=0, sticky="nsew")


app = App()
app.mainloop()
