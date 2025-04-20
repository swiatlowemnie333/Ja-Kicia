import pyautogui
import threading
import time
import tkinter as tk
from tkinter import simpledialog

class KiciaControl:
    """
    Moduł do przejmowania kontroli nad myszką i klawiaturą oraz wyświetlania pytań użytkownikowi.
    """
    def __init__(self):
        self.active = False

    def start_control(self):
        self.active = True
        # Możesz dodać tu logikę inicjalizującą

    def stop_control(self):
        self.active = False

    def move_mouse(self, x, y, duration=0.2):
        if self.active:
            pyautogui.moveTo(x, y, duration=duration)

    def click_mouse(self, button='left'):
        if self.active:
            pyautogui.click(button=button)

    def type_text(self, text):
        if self.active:
            pyautogui.write(text)

    def ask_user(self, question: str) -> str:
        """Wyświetla okno z pytaniem i czeka na odpowiedź użytkownika."""
        result = {'answer': None}
        def dialog():
            root = tk.Tk()
            root.withdraw()
            answer = simpledialog.askstring("Kicia pyta", question)
            result['answer'] = answer
            root.destroy()
        t = threading.Thread(target=dialog)
        t.start()
        t.join()
        return result['answer']

# Przykład użycia:
# kicia = KiciaControl()
# kicia.start_control()
# kicia.move_mouse(100, 100)
# kicia.click_mouse()
# kicia.type_text('Hello!')
# answer = kicia.ask_user('Czy chcesz kontynuować?')
# print('Odpowiedź:', answer)
# kicia.stop_control()
