from tkinter import *
from tkinter.messagebox import showinfo
from gtts import gTTS
import speech_recognition as sr
import os
from textblob import TextBlob  # Import TextBlob for sentiment analysis
import nltk
from nltk.tokenize import word_tokenize

# Download NLTK resources (required for tokenization)
nltk.download('punkt')

mainwindow = Tk()
mainwindow.title('Text-To-Speech and Speech-To-Text Converter')
mainwindow.geometry('500x500')
mainwindow.resizable(0, 0)
mainwindow.configure(bg='#FAEBD7')


def say(text1):
    language = 'en'
    speech = gTTS(text=text1, lang=language, slow=False)
    speech.save("text.mp3")
    os.system("start text.mp3")


def recordvoice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text1 = r.recognize_google(audio, language="en-IN")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            text1 = ""
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            text1 = ""
    return text1


def texttospeech():
    texttospeechwindow = Toplevel(mainwindow)
    texttospeechwindow.title('Text-to-Speech Converter')
    texttospeechwindow.geometry("500x500")
    texttospeechwindow.configure(bg='Light blue')

    Label(texttospeechwindow, text='Text-to-Speech Converter', font=("Comic Sans MS", 15),
          bg='Light green').place(x=110)

    text = Text(texttospeechwindow, height=5, width=30, font=12)
    text.place(x=100,y=60)

    def record_and_analyze():
        spoken_text = str(text.get(1.0, END))
        say(spoken_text)

        # Tokenize the spoken text
        tokens = word_tokenize(spoken_text)

        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(spoken_text)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            sentiment_label = "Positive"
        elif sentiment == 0:
            sentiment_label = "Neutral"
        else:
            sentiment_label = "Negative"

        showinfo("Sentiment Analysis Result", f"Sentiment: {sentiment_label}\nTokens: {tokens}")

    speakbutton = Button(texttospeechwindow, text='listen', bg='coral', command=record_and_analyze)
    speakbutton.place(x=220, y=200)


def speechtotext():
    speechtotextwindow = Toplevel(mainwindow)
    speechtotextwindow.title('Speech-to-Text Converter')
    speechtotextwindow.geometry("500x500")
    speechtotextwindow.configure(bg='pink')

    Label(speechtotextwindow, text='Speech-to-Text Converter', font=("Comic Sans MS", 15),
          bg='IndianRed').place(x=110)

    text = Text(speechtotextwindow, font=12, height=3, width=30)
    text.place(x=100, y=100)

    def record_and_analyze():
        spoken_text = recordvoice()
        text.insert(END, spoken_text)

        # Tokenize the spoken text
        tokens = word_tokenize(spoken_text)

        # Perform sentiment analysis using TextBlob
        analysis = TextBlob(spoken_text)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            sentiment_label = "Positive"
        elif sentiment == 0:
            sentiment_label = "Neutral"
        else:
            sentiment_label = "Negative"

        showinfo("Sentiment Analysis Result", f"Sentiment: {sentiment_label}\nTokens: {tokens}")


    recordbutton = Button(speechtotextwindow, text='Record', bg='Sienna', command= record_and_analyze)
    recordbutton.place(x=200, y=50)


Label(mainwindow, text='Text-To-Speech and Speech-To-Text Converter',
      font=('Times New Roman', 16), bg='#FFD39B', wraplength=450).place(x=50, y=0)
texttospeechbutton = Button(mainwindow, text='Text-To-Speech Conversion', font=('Times New Roman', 16), bg='#E3CF57',
                            command=texttospeech)
texttospeechbutton.place(x=125,y=150)

speechtotextbutton = Button(mainwindow, text='Speech-To-Text Conversion', font=('Times New Roman', 16), bg='#E3CF57',
                            command=speechtotext)
speechtotextbutton.place(x=125, y=250)

mainwindow.update()
mainwindow.mainloop()
