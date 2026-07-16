import speech_recognition as sr
import pyttsx3

from chatbot import answer_question

engine = pyttsx3.init()

engine.setProperty('rate',150)

engine.setProperty('volume',1.0)

voices = engine.getProperty('voices')

engine.setProperty(
    'voice',
    voices[1].id
)

def speak(text):

    print("\nAssistant:", text)

    engine.say(text)

    engine.runAndWait()

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone(device_index=3) as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

        audio = recognizer.listen(source)

    try:

        query = recognizer.recognize_google(audio)

        print("You:", query)

        return query

    except:

        return ""

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone(device_index=3) as source:
#         print("Calibrating for background noise...")
#         recognizer.adjust_for_ambient_noise(source, duration=1)
#         print("Listening... (Speak now)")
        
#         # Add a timeout and phrase_time_limit
#         try:
#             audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
#             print("Processing...")
#             query = recognizer.recognize_google(audio)
#             print("You said:", query)
#             return query
#         except sr.WaitTimeoutError:
#             print("Listening timed out. No speech detected.")
#             return ""
#         except sr.UnknownValueError:
#             print("Could not understand audio.")
#             return ""
#         except Exception as e:
#             print(f"Error: {e}")
#             return ""

def main():

    speak(
        "Welcome to Roshini's Voice Assistant"
    )

    while True:

        query = listen()

        if query == "":
            continue

        if "exit" in query.lower():

            speak("Good Bye")

            break

        answer = answer_question(query)

        speak(answer)

if __name__ == "__main__":

    main()