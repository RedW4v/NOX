import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import time
import keyboard
import os
from pygame import mixer
from tkinter import *
from PIL import ImageTk, Image
#import threading as tr

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
        - Alarma ... No disponible
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



sites = {}

files = {}

# Si no funciona hay que buscar esa dirección, abrir la ubicación del archivo exe y copiar su ruta
programs = {}


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
        # elif 'alarma' in rec:
        #     # t = tr.Thread(target=clock, args=(rec,))
        #     # t.start()
        #     num = rec.replace('alarma', '')
        #     # Esto sirve para que no haya un espacio de más
        #     num = num.strip()
        #     talk("Alarma activada a las " + num + " horas")
        #     print("Alarma activada a las " + num + " horas")
        #     if num[0] != '0' and len(num) < 5:
        #         num = '0' + num
        #     print(num)
        #     while True:
        #         if datetime.datetime.now().strftime('%H:%M') == num:
        #             print("Despierta!!!!")
        #             mixer.init()
        #             mixer.music.load("Ghost_Call_Me_Little_Sunshine.mp3")
        #             mixer.music.play()
        #         if keyboard.read_key() == "s":
        #             mixer.music.stop()
        #             break
        elif 'abre' in rec:
            task = rec.replace("abre", "").strip()
            if task in sites:
                for task in sites:
                    if task in rec:
                        # El shell es para que se tome como escritura en el shell
                        sub.call(f'start msedge.exe {sites[task]}', shell=True)
                        print(f"Abriendo {task}")
                        talk(f'Abriendo {task}')
            elif task in programs:
                for task in programs:
                    if task in rec:
                        os.startfile(programs[task])
                        talk(f"Abriendo {task}")
                        print(f"Abriendo {task}")
            else:
                talk("Lo siento, parece que aún no has agregado ese elemento. Usa el botón de agregar")
        elif 'archivo' in rec:
            file = rec.replace("archivo", "").strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen(files[file], shell=True)
                        print(f'Abriendo {file}')
                        talk(f'Abriendo {file}')
            else:
                talk("Lo siento, parece que aún no has agregado ese elemento. Usa el botón de agregar")
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

def open_w_files():
    global filename_entry, pathf_entry
    window_files = Toplevel()#segunda ventana
    window_files.title("Agregar Archivos")
    window_files.configure(bg="#0F2027")
    window_files.geometry("300x200")
    window_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_files)} center')

    title_label = Label(window_files, text="Agrega un archivo",fg="white",bg="#0F2027", font=('Arial', 15,'bold'))
    title_label.pack(paddy=3)
    name_label = Label(window_files, text="Nombre un archivo",fg="white",bg="#0F2027", font=('Arial', 10,'bold'))
    name_label.pack(paddy=2)

    filename_entry = Entry(window_files)
    filename_entry.pack(paddy=1)

    path_label = Label(window_files, text="Ruta del archivo",fg="white",bg="#0F2027", font=('Arial', 10,'bold'))
    path_label.pack(paddy=2)
    pathf_entry = Entry(window_files,width=35)
    pathf_entry.pack(paddy=1)

    save_button = Button(window_files, text="Guardar", bg="#203A43", fg="White",width=8,height=1,command=add_files)
    save_button.pack(paddy=4)
def open_w_apps():
    global app_entry, patha_entry
    window_app = Toplevel()
    window_app.title("Agregar Aplicaciones")
    window_app.configure(bg="#0F2027")
    window_app.geometry("300x200")
    window_app.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_app)} center')

    title_label = Label(window_app, text="Agrega una aplicación",fg="white",bg="#0F2027", font=('Arial', 15,'bold'))
    title_label.pack(paddy=3)
    name_label = Label(window_app, text="Nombre de la aplicación",fg="white",bg="#0F2027", font=('Arial', 10,'bold'))
    name_label.pack(paddy=2)

    app_entry = Entry(window_app)
    app_entry.pack(paddy=1)

    path_label = Label(window_app, text="Dirección de la aplicación",fg="white",bg="#0F2027", font=('Arial', 10,'bold'))
    path_label.pack(paddy=2)
    patha_entry = Entry(window_app,width=35)
    patha_entry.pack(paddy=1)

    save_button = Button(window_app, text="Guardar", bg="#203A43", fg="White",width=8,height=1,command=add_apps)
    save_button.pack(paddy=4)
def open_w_pages():
    global page_entry, pathp_entry
    window_page = Toplevel()
    window_page.title("Agregar Páginas")
    window_page.configure(bg="#0F2027")
    window_page.geometry("300x200")
    window_page.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_page)} center')

    title_label = Label(window_page, text="Agrega una página",fg="white",bg="#0F2027", font=('Arial', 15,'bold'))
    title_label.pack(paddy=3)
    name_label = Label(window_page, text="Nombre de la pag",fg="white",bg="#0F2027", font=('Arial', 10,'bold'))
    name_label.pack(paddy=2)

    page_entry = Entry(window_page)
    page_entry.pack(paddy=1)

    path_label = Label(window_page, text="URL de la página",fg="white",bg="#0F2027", font=('Arial', 10,'bold'))
    path_label.pack(paddy=2)
    pathp_entry = Entry(window_page,width=35)
    pathp_entry.pack(paddy=1)

    save_button = Button(window_page, text="Guardar", bg="#203A43", fg="White",width=8,height=1, command=add_pages)
    save_button.pack(paddy=4)

def add_files():
    name_file = filename_entry.get().strip() #Corta espacio en blanco si está al inicio o al final
    path_file = pathf_entry.get().strip()
    
    files[name_file] = path_file
    filename_entry.delete(0,"end")
    pathf_entry.delete(0,"end")

def add_apps():
    name_app = app_entry.get().strip()
    path_app = patha_entry.get().strip()
    
    programs[name_app] = path_app
    app_entry.delete(0,"end")
    patha_entry.delete(0,"end")
def add_pages():
    name_page = page_entry.get().strip()
    path_page = pathp_entry.get().strip()
    
    sites[name_page] = path_page
    page_entry.delete(0,"end")
    pathp_entry.delete(0,"end")

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




button_add_files = Button(main_window, text="Add files", fg="white", bg="#23074d", 
                         font=("Arial",10,"bold"), command=open_w_files)
button_add_files.place(x=625,y=190, width=100, height=30)
button_add_apps = Button(main_window, text="Add apps", fg="white", bg="#23074d", 
                         font=("Arial",10,"bold"), command=open_w_apps)
button_add_apps.place(x=625,y=230, width=100, height=30)
button_add_pages = Button(main_window, text="Add pages", fg="white", bg="#23074d", 
                         font=("Arial",10,"bold"), command=open_w_pages)
button_add_pages.place(x=625,y=270, width=100, height=30)

main_window.mainloop()#HAce que el código se ejecute solo cuando la ventana esté ejecutándose