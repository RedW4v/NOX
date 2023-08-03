import speech_recognition as sr
import subprocess as sub
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard, os
from pygame import mixer

#python .\NOX.py
#Al pasarlo a otro dispositivo hay que cambiar las rutas en files, programs y hay que poner call me little
#sunshine en la misma carpeta de NOX

name="Nox"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# Este puede no funcionar
engine.setProperty('rate', 145)

sites={
            'google' : 'google.com',
            'youtube': 'youtube.com',
            'facebook': 'facebook.com',
            'whatsapp': 'web.whatsapp.com',
            'clases': 'classroom.google.com/u/1/',
            'traductor': 'translate.google.com.mx/'
}

files={
    'seguridad': 'C:\\Users\\zjosh\\Desktop\\RW\\CyberSec\\Apuntes.docx',
    'redes': 'C:\\Users\\zjosh\\Desktop\\RW\\Redes\\Apuntes.docx',
    'trabajo':'C:\\Users\\zjosh\\Desktop\\FormatoTrabajos.docx'
}

#Si no funciona hay que buscar esa dirección, abrir la ubicación del archivo exe y copiar su ruta
programs={
    'telegram': 'C:\\Users\\zjosh\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe',
    'spotify': 'C:\\Users\\zjosh\\AppData\\Local\\Microsoft\\WindowsApps\\Spotify.exe',
    'discord': 'C:\\Users\\zjosh\\AppData\\Local\\Discord\\app-1.0.9015\\Discord.exe'
}


def talk(text):
    engine.say(text)
    engine.runAndWait()





def listen():
    rec = ""  # Asignamos un valor predeterminado a la variable rec
    try:
        with sr.Microphone() as source:
            
            print("Te escucho...")
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
            print("Reproducinedo " + music)
            talk("Reproduciendo " + music)
            #Hace el proceso de reproducción en youtube
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca','')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search,1)
            print(search +": "+wiki)
            talk(wiki)
        elif 'alarma' in rec:
            num = rec.replace('alarma','')
            #Esto sirve para que no haya un espacio de más
            num = num.strip()
            talk("Alarma activada a las " +num+ " horas")
            print("Alarma activada a las " +num+ " horas")
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
                        #El shell es para que se tome como escritura en el shell
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

#Buena práctica de python
if __name__ == '__main__':
    run_nox()

#python .\NOX.py