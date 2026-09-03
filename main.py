import customtkinter as kc
from deep_translator import GoogleTranslator
import time
from pygame import mixer
from gtts import gTTS
from PIL import Image
import os

class TranslatorApp(kc.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color, **kwargs)
        kc.set_appearance_mode("dark")
        mixer.init()

        self.after(0, lambda: self.state("zoomed"))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        Imagen_Boton = Image.open("Arrow.png")
        Imagen_Boton_Audio = Image.open("Blue_Audio.png")

        self.Imagen_Boton_Audio = kc.CTkImage(
            dark_image=Imagen_Boton_Audio, light_image=Imagen_Boton_Audio, size=(40, 40)
        )

        self.Imagen_Boton = kc.CTkImage(
            dark_image=Imagen_Boton, light_image=Imagen_Boton, size=(40, 40)
        )

        self.MainFrame = kc.CTkFrame(
            self,
            width=900,
            height=400,
            border_width=5,
            corner_radius=24,
            fg_color=(
                "#F5F5F7",
                "#1E1E1E",
            ),
            border_color="#F1E7E7",
        )
        self.MainFrame.grid(row=0, column=0)
        self.MainFrame.grid_propagate(False)
        self.MainFrame.grid_rowconfigure(0, weight=1)
        self.MainFrame.grid_columnconfigure(0, weight=1)

        self.InitialTextFrame = kc.CTkFrame(
            self.MainFrame,
            width=300,
            height=300,
            border_width=0,
            corner_radius=20,
            fg_color=("#FFFFFF", "#2A2A2A"),
        )
        self.InitialTextFrame.grid(row=0, column=0, padx=(40, 0), sticky="w")
        self.InitialTextFrame.grid_propagate(False)

        self.FinalTextFrame = kc.CTkFrame(
            self.MainFrame,
            width=300,
            height=300,
            border_width=0,
            corner_radius=20,
            fg_color=("#FFFFFF", "#2A2A2A"),
        )
        self.FinalTextFrame.grid(row=0, column=1, padx=(0, 40), sticky="e")
        self.FinalTextFrame.grid_propagate(False)
        self.TextEnglishBox = kc.CTkTextbox(
            self.FinalTextFrame,
            width=300,
            height=300,
            border_width=5,
            border_color="#ffffff",
            font=("comic sans", 20, "bold"),
            state="disabled"
        )
        self.TextEnglishBox.place(rely=0.5, relx=0.5, anchor="center")

        self.StuffFrame = kc.CTkFrame(
            self.MainFrame,
            width=150,
            height=300,
            border_width=0,
            corner_radius=20,
            fg_color=("#E5E5EA", "#3A3A3C"),
        )
        self.StuffFrame.place(rely=0.5, relx=0.5, anchor="center")
        self.StuffFrame.grid_propagate(False)
        self.StuffFrame.grid_columnconfigure(0, weight=1)
        self.StuffFrame.grid_rowconfigure(0, weight=1)

        self.SwicthButton = kc.CTkButton(
            self.StuffFrame,
            text="",
            image=self.Imagen_Boton,
            anchor="center",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color=("#D1D1D6", "#48484A"),
            corner_radius=20,
            command=self.Spanish_to_English
        )
        self.SwicthButton.grid(row=0, column=0, sticky="n", pady=(20))

        self.AudioButton = kc.CTkButton(
            self.StuffFrame,
            text="",
            image=self.Imagen_Boton_Audio,
            anchor="center",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color=("#D1D1D6", "#48484A"),
            corner_radius=20,
            command=self.AudioPlay
        )
        self.AudioButton.grid(row=1, column=0, pady=(20))

        self.TextSpanishBox = kc.CTkTextbox(
            self.InitialTextFrame,
            width=300,
            height=300,
            border_width=5,
            border_color="#ffffff",
            font=("comic sans", 20, "bold"),
        )
        self.TextSpanishBox.place(rely=0.5, relx=0.5, anchor="center")
        self.TextSpanishBox.bind("<FocusIn>", self.quitar_placeholder)
        self.TextSpanishBox.configure(text_color="gray")
        self.TextSpanishBox.insert("1.0", "Escribe el texto a traducir...")

        self.TextSpanishBox.bind("<FocusOut>", self.poner_placeholder)

    def quitar_placeholder(self, event):

        if self.TextSpanishBox.get("1.0", "end-1c") == "Escribe el texto a traducir...":
            self.TextSpanishBox.delete("1.0", "end")
            self.TextSpanishBox.configure(text_color=("#000000", "#FFFFFF"))

    def poner_placeholder(self, event):
        if not self.TextSpanishBox.get("1.0", "end-1c").strip():
            self.TextSpanishBox.insert("1.0", "Escribe el texto a traducir...")
            self.TextSpanishBox.configure(text_color="gray")
    def Spanish_to_English(self):
        global Texto_traducido
        
        Spanish_text = self.TextSpanishBox.get("1.0","end")
        
        if Spanish_text:
            self.TextEnglishBox.configure(state="normal")
            Texto_traducido = GoogleTranslator(source="es" ,target="en").translate(Spanish_text)
            self.TextEnglishBox.delete("1.0","end")
            self.TextEnglishBox.insert("1.0",Texto_traducido)
            self.TextEnglishBox.configure(state="disabled")
    def AudioPlay(self):
        Audio_Data = gTTS(text=Texto_traducido,lang="en")
        
        if Audio_Data:
         Audio_Data.save("AudioT.mp3")
        
         mixer.music.load("AudioT.mp3")
         mixer.music.play()
        
         while mixer.music.get_busy():
            time.sleep(0.1)
        
        mixer.music.unload()
        
        os.remove("AudioT.mp3")    
        
            

App = TranslatorApp()
App.mainloop()
