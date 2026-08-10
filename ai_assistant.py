import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate",160)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ai_assistant(root, cursor):
    window=tk.Toplevel(root)
    window.title("AI Pharmacy Assistant")
    window.geometry("650x500")

    tk.Label(window,text="AI Pharmacy Assistant",font=("Arial",16,"bold")).pack(pady=10)

    search_box=tk.Entry(window,width=40,font=("Arial",12))
    search_box.pack(pady=5)

    result=scrolledtext.ScrolledText(window,width=70,height=18)
    result.pack(pady=10)

    def search_medicine():
        name=search_box.get().strip()
        result.delete("1.0",tk.END)

        if not name:
            result.insert(tk.END,"Enter a medicine name.")
            speak("Please enter a medicine name.")
            return

        cursor.execute("""
        SELECT medicine_name, company, price, stock, expiry_date
        FROM Medicines
        WHERE medicine_name LIKE %s
        LIMIT 1
        """,('%'+name+'%',))

        medicine=cursor.fetchone()
        cursor.fetchall()

        if medicine:
            msg=f"""Medicine Details

Name : {medicine[0]}
Company : {medicine[1]}
Price : ₹{medicine[2]}
Stock : {medicine[3]}
Expiry : {medicine[4]}
"""
            result.insert(tk.END,msg)
            speak(f"{medicine[0]} is available. Price {medicine[2]} rupees. Stock {medicine[3]}.")
        else:
            result.insert(tk.END,"Medicine not found.")
            speak("Medicine not found.")

    def voice_search():
        r=sr.Recognizer()
        try:
            with sr.Microphone() as source:
                result.delete("1.0",tk.END)
                result.insert(tk.END,"Listening...\n")
                r.adjust_for_ambient_noise(source,duration=0.5)
                audio=r.listen(source)
            text=r.recognize_google(audio)
            search_box.delete(0,tk.END)
            search_box.insert(0,text)
            search_medicine()
        except Exception as e:
            result.delete("1.0",tk.END)
            result.insert(tk.END,f"Voice Error:\n{e}")
            speak("Sorry, I could not understand.")

    tk.Button(window,text="Search",command=search_medicine,bg="blue",fg="white").pack(pady=5)
    tk.Button(window,text="Voice Search",command=voice_search,bg="green",fg="white").pack(pady=5)
