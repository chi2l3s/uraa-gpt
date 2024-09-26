import flet as ft
from g4f.client import Client
import time

import speech_recognition as sr
import pyttsx3
engine = pyttsx3.init()

voices = engine.getProperty('voices')

# engine.setProperty('voice', voices[1].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()
    time.sleep(1)

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio, language='ru-RU')
            print(f"Вы сказали: {command}")
            return command
        except sr.UnknownValueError:
            print("Не удалось распознать речь")
            return None
        except sr.RequestError:
            print("Ошибка сервиса распознавания")
            return None

def send():
    command = recognize_speech()
    if command:
        if "стоп" in command.lower():
            speak("До свидания!")
            return
        else:
            response = ask(command)
            print(response)
            speak(response)

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = ft.padding.all(value=100)
    page.title = 'URAA-GPT 1.0'
    page.add(
        ft.OutlinedButton(
            text='',
            height=400,
            width=400,
            style=ft.ButtonStyle(color=ft.colors.RED_200, shadow_color=ft.colors.RED_900),
            on_click=lambda e: send()
        )
    )

def ask(text):
    client = Client()
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}],
    )
    return response.choices[0].message.content

ft.app(main)