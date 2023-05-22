import tkinter
import algorithm
import threading
import customtkinter

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Auto Correct Bahasa Indonesia")
        self.geometry(f"{720}x{480}")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)

        self.frame = customtkinter.CTkFrame(self)
        self.frame.grid(row=0, column=0, pady=20, padx=20, sticky="nsew")
        
        self.label = customtkinter.CTkLabel(
            self.frame, text="Auto Correct Bahasa Indonesia", fg_color="transparent", font=("Arial", 16))
        self.label.grid(row=0, column=0, padx=20, pady=(20,0), sticky="nsew")

        # create main textbox
        self.label_text_1 = customtkinter.CTkLabel(
            self.frame, text="Insert text below:", fg_color="transparent")
        self.label_text_1.grid(row=1, column=0, padx=22, pady=(20, 0), sticky="w")
        self.textbox1 = customtkinter.CTkTextbox(
            self.frame, width=640, height=135, text_color="#A6A6A6")
        self.textbox1.grid(row=2, column=0, padx=20, pady=(5,10), sticky="nsew")
        self.textbox1.insert("0.0", "Enter text here . . .")
        self.textbox1.configure(state="disabled")
        self.textbox1.bind("<FocusIn>", self.on_click)
        self.textbox1.bind("<FocusOut>", self.on_focus_out)
            
        # create result textbox
        self.label_text_2 = customtkinter.CTkLabel(
            self.frame, text="Result: ", fg_color="transparent")
        self.label_text_2.grid(row=3, column=0, padx=22,
                               pady=(0, 5), sticky="w")
        self.textbox2 = customtkinter.CTkTextbox(
            self.frame, width=640, height=135, state="disabled")
        self.textbox2.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # bind event to update second textbox
        self.textbox1.bind("<KeyRelease>", self.update_textbox2)

    def on_click(self, event):
        if not self.textbox2.get("0.0", "end-1c"):
            self.textbox1.configure(state="normal", text_color="#ffffff")
            self.textbox1.delete("0.0", "end-1c")
        self.textbox1.configure(border_width=2, border_color="#0E4C78")

    def on_focus_out(self, event):
        if not self.textbox1.get("0.0", "end-1c"):
            self.textbox1.insert("0.0", "Masukan text ...")
            self.textbox1.configure(state="disabled", text_color="#A6A6A6")
        self.textbox1.configure(border_width=0)

    def update_textbox2(self, event):
        # Cancel any existing timer
        if hasattr(self, 'timer'):
            self.timer.cancel()

        # Start a new timer to update the textbox after 500 milliseconds
        self.timer = threading.Timer(1.0, self.perform_spell_check)
        self.timer.start()

    def perform_spell_check(self):
        # Get the text from the first textbox
        text = self.textbox1.get("0.0", "end")

        # Clear the second textbox and insert the text from the first textbox
        self.textbox2.configure(state="normal")
        self.textbox2.delete("0.0", "end")

        suggestions, corrected_sentence = algorithm.spell_checker(text)
        
        self.textbox2.insert("0.0", corrected_sentence)
        
        # Apply red color to suggested words
        self.textbox2.tag_config("red", foreground="red")  # Define the tag once
        for word, index in suggestions:
            start_index = f"1.{index}"
            end_index = f"1.{index + len(word)}"
            self.textbox2.tag_add("red", start_index, end_index)

        # Insert the corrected sentence into the second textbox
        self.textbox2.configure(state="disabled")

if __name__ == "__main__":
    app = App()
    app.mainloop()
