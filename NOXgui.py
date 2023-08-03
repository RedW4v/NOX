import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import keyboard
import os
from pygame import mixer
from tkinter import *
from PIL import ImageTk, Image

# python .\NOX.py
# Al pasarlo a otro dispositivo hay que cambiar las rutas en files, programs y hay que poner call me little
# sunshine en la misma carpeta de NOX

main_window = Tk() #Ventana raíz
main_window.title("NOX Assistant")

main_window.geometry("800x450")#Ancho x alto
main_window.resizable(0,0)#Se elimina el resize
main_window.configure(bg="#0F2027")#fondo

comandos = """
        Comandos disponibles:
        - Reproduce ... (canción)
        - Busca ... (algo)
        - Abre ... (pag o app)
        - Alarma ... (hora en 24hrs)
        - Archivo ... (nombre)
        - Escribe ... (info a anotar)
        - Termina para que deje de
          escuchar
"""


label_title = Label(main_window, text="NOX", bg="#203A43", fg="#000000", font=("Arial", 20,'bold'))
label_title.pack(pady=10)#vuelve a la label un bloque y lo pone en el centro con padding de 10 px

canvas_comandos = Canvas(bg="#2c3e50", height=170, width=195)
canvas_comandos.place(x=0,y=0)
canvas_comandos.create_text(90,80, text = comandos, fill="white", font='Arial 10')

text_info = Text(main_window,bg="#2c3e50",fg="white")
text_info.place(x=0,y=175,height=275, width=198)

nox_photo = ImageTk.PhotoImage(Image.open(r"C:\Users\zjosh\Desktop\RW\Proyectoss\AsistentePY\NOX\R.jpg"))
window_photo = Label(main_window, image=nox_photo)
window_photo.pack(pady=5)

def mexico_voice():
    change_voice(2)
def usa_voice():
    change_voice(0)
def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    if id == 2:
        talk("Hola; Soy Nox")
    else:
        talk("Hello; Im Nox")

name = "Nox"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)
engine.setProperty('rate', 145)



sites = {
    'google': 'google.com',
    'youtube': 'youtube.com',
    'facebook': 'facebook.com',
    'whatsapp': 'web.whatsapp.com',
    'clases': 'classroom.google.com/u/1/',
    'traductor': 'translate.google.com.mx/'
}

files = {
    'seguridad': 'C:\\Users\\zjosh\\Desktop\\RW\\CyberSec\\Apuntes.docx',
    'redes': 'C:\\Users\\zjosh\\Desktop\\RW\\Redes\\Apuntes.docx',
    'trabajo': 'C:\\Users\\zjosh\\Desktop\\FormatoTrabajos.docx'
}

# Si no funciona hay que buscar esa dirección, abrir la ubicación del archivo exe y copiar su ruta
programs = {
    'telegram': 'C:\\Users\\zjosh\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe',
    'spotify': 'C:\\Users\\zjosh\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe',
    'discord': 'C:\\Users\\zjosh\\AppData\\Local\\Discord\\app-1.0.9015\\Discord.exe'
}


def talk(text):
    engine.say(text)
    engine.runAndWait()

def read_and_talk():
    text = text_info.get("1.0", "end") #Obtiene el texto de principio a fin
    talk(text)
def write_text(text_wiki):
    text_info.insert(INSERT, text_wiki)

def listen():
    rec = ""  # Asignamos un valor predeterminado a la variable rec
    try:
        with sr.Microphone() as source:

            talk("Te escucho...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')

    except:
        pass
    return rec


def run_nox():
    while True:
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            talk("Reproduciendo " + music)
            # Hace el proceso de reproducción en youtube
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
            write_text(search + ": "+wiki)
            break #Muestra la info después de que deja de escuchar así que hay que darle de nuevo al botón
        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            # Esto sirve para que no haya un espacio de más
            num = num.strip()
            talk("Alarma activada a las " + num + " horas")
            print("Alarma activada a las " + num + " horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M') == num:
                    print("Despierta!!!!")
                    mixer.init()
                    mixer.music.load("Ghost_Call_Me_Little_Sunshine.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
                if keyboard.read_key() == "q":
                    break
        elif 'abre' in rec:
            for site in sites:
                for site in sites:
                    if site in rec:
                        # El shell es para que se tome como escritura en el shell
                        sub.call(f'start msedge.exe {sites[site]}', shell=True)
                        print(f"Abriendo {site}")
                        talk(f'Abriendo {site}')
                for app in programs:
                    if app in rec:
                        os.startfile(programs[app])
                        talk(f"Abriendo {app}")
                        print(f"Abriendo {app}")
        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen(files[file], shell=True)
                    print(f'Abriendo {file}')
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)

            except FileNotFoundError as e:
                file = open("nota.txt", 'w')
                write(file)
        elif 'termina' in rec:
            talk('NOX: ¡over and out!')
            break


def write(f):
    talk("¿Qué quieres que escriba?")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("¡Ready!, chek it out")
    sub.Popen("nota.txt", shell=True)


button_voice_mx = Button(main_window, text="Voz México", fg="white", bg="#38ef7d", 
                         font=("Arial",10,"bold"), command=mexico_voice)
button_voice_mx.place(x=625,y=90, width=100, height=30)

button_voice_us = Button(main_window, text="Voz USA", fg="white", bg="#11998e", 
                         font=("Arial",10,"bold"), command=usa_voice)
button_voice_us.place(x=625,y=50, width=100, height=30)

button_listen = Button(main_window, text="Escuchar", fg="white", bg="#23074d", 
                         font=("Arial",15,"bold"),width=20,height=3 ,command=run_nox)
button_listen.pack(pady=10)

button_speak = Button(main_window, text="Hablar", fg="white", bg="#23074d", 
                         font=("Arial",10,"bold"), command=read_and_talk)
button_speak.place(x=625,y=150, width=100, height=30)


main_window.mainloop()#HAce que el código se ejecute solo cuando la ventana esté ejecutándose