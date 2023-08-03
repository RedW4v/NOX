import speech_recognition as sr
import pyttsx3, pywhatkit, wikipedia, datetime, keyboard
from pygame import mixer



name="Nox"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)



def talk(text):
    engine.say(text)
    engine.runAndWait()





def listen():
    try:
        with sr.Microphone() as source:
            talk("Speak to me")
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



#Buena práctica de python
if __name__ == '__main__':
    run_nox()

#python .\AsistenteYTMusic.py