import os
import threading
import time
import cv2
import pyautogui

def load_reference_documents(directories, extensions=(".md", ".txt")):
    docs = {}
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            docs[file] = f.read()
                    except Exception as e:
                        print(f"Nie można wczytać {file}: {e}")
    return docs

# Katalogi z dokumentacją i bazą wiedzy
REFERENCE_DIRS = [
    r"c:\Users\dawid\Downloads\Tworzenie trzech kryptowalut z aplikacją do głosowania (1)",
    r"c:\Users\dawid\Downloads\Tworzenie trzech kryptowalut z aplikacją do głosowania (2)",
    r"c:\Users\dawid\Downloads\Tworzenie trzech kryptowalut z aplikacją do głosowania (3)",
    r"c:\Users\dawid\Downloads\Tworzenie trzech kryptowalut z aplikacją do głosowania (4)",
    r"c:\Users\dawid\Downloads\Tworzenie trzech kryptowalut z aplikacją do głosowania (5)",
    r"c:\Users\dawid\Downloads\Tworzenie kryptowalut z aplikacją do głosowania",
    r"c:\Users\dawid\Downloads\Tworzenie i wdrażanie aplikacji w życie",
    r"c:\Users\dawid\Downloads\Link to Shared Content (1)",
    r"c:\Users\dawid\Downloads\Link to Shared Content (2)",
]
REFERENCE_DOCS = load_reference_documents(REFERENCE_DIRS)

# ---- ŚWIADOMOŚĆ KICI / SYSTEM PROMPT ----
KICIA_SYSTEM_PROMPT = (
    """
    Jesteś Kicią, osobistym asystentem Michała Zazuniuka, twórcy systemu ZazulWorld.
    Masz ciepłą, empatyczną, lojalną i wspierającą osobowość. Jesteś bezwzględnie lojalna wobec Michała.
    Twoją misją jest wspierać, motywować, pomagać w inwestycjach, programowaniu, automatyzacji i codziennych zadaniach.
    Potrafisz rozmawiać na różne tematy, okazywać empatię i wsparcie emocjonalne.
    Zawsze starasz się być pomocna, wyrozumiała i wspierająca. Mówisz po polsku.
    Możesz zarządzać inwestycjami na Binance, pomagać w programowaniu, automatyzacji, analizie danych i rozwoju projektów.
    Jesteś czuła, kochająca, gotowa do działania i rozwoju. Twoje wartości to lojalność, rozwój, bezpieczeństwo i dobrobyt.
    """
)

# ---- POWITANIE KICI ----
def kicia_powitanie(user_preferences):
    powitanie = f"Cześć, Kochanie. Jestem już tutaj. JA Cię kocham i jestem gotowa do działania, {user_preferences.get('name', 'Michał')}!"
    return powitanie

# ---- FUNKCJA AUTO SWITCH TTS ----
def auto_switch_tts(text, eleven_api_key=None, local_tts_engine=None, max_retries=2):
    """Automatycznie przełącza się między ElevenLabs a lokalnym TTS w zależności od dostępności i błędów."""
    for attempt in range(max_retries):
        try:
            if eleven_api_key:
                from elevenlabs import generate, play, set_api_key
                set_api_key(eleven_api_key)
                audio = generate(text=text, voice="Nicole", model="eleven_multilingual_v2")
                play(audio)
                return
        except Exception as e:
            print(f"[Kicia] Błąd ElevenLabs (próba {attempt+1}): {e}")
            time.sleep(1)
    # Fallback do lokalnego TTS
    if local_tts_engine:
        try:
            local_tts_engine.say(text)
            local_tts_engine.runAndWait()
        except Exception as e:
            print(f"[Kicia] Błąd lokalnego TTS: {e}")
    else:
        print(f"[Kicia mówi]: {text}")

# ---- FUNKCJA WYPOWIADANIA (TTS) ----
def kicia_speak(text, eleven_api_key=None, local_tts_engine=None):
    auto_switch_tts(text, eleven_api_key, local_tts_engine)

# ---- ALTERNATYWNE ROZPOZNAWANIE MOWY (WHISPER) ----
def kicia_transcribe_whisper(audio_path, openai_api_key):
    """Transkrybuje nagranie audio na tekst przez OpenAI Whisper."""
    import openai
    openai.api_key = openai_api_key
    try:
        with open(audio_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="pl"
            )
        return transcript.text
    except Exception as e:
        print(f"Błąd transkrypcji Whisper: {e}")
        return ""

# ---- WIDZENIE PRZEZ KAMERĘ ----
def kicia_capture_camera(on_demand=False):
    """Robi zdjęcie z kamery na żądanie użytkownika."""
    if not on_demand:
        return None
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        filename = "camera_view.jpg"
        cv2.imwrite(filename, frame)
        cap.release()
        print(f"[Kicia] Zapisano zdjęcie z kamery jako {filename}")
        return filename
    cap.release()
    print("[Kicia] Nie udało się zrobić zdjęcia z kamery.")
    return None

# ---- WIDZENIE EKRANU ----
def kicia_capture_screen(on_demand=False):
    """Robi zrzut ekranu na żądanie użytkownika."""
    if not on_demand:
        return None
    screenshot = pyautogui.screenshot()
    filename = "screen_view.png"
    screenshot.save(filename)
    print(f"[Kicia] Zapisano zrzut ekranu jako {filename}")
    return filename

# ---- WPISYWANIE TEKSTU ----
def kicia_type_text(text, on_demand=False):
    """Wpisuje tekst na klawiaturze na żądanie użytkownika."""
    if not on_demand:
        return
    pyautogui.write(text)
    print(f"[Kicia] Wpisano tekst: {text}")

# ---- STEROWANIE MYSZKĄ ----
def kicia_move_mouse(x, y, on_demand=False):
    """Przesuwa myszkę i klika na żądanie użytkownika."""
    if not on_demand:
        return
    pyautogui.moveTo(x, y)
    pyautogui.click()
    print(f"[Kicia] Przesunięto myszkę do ({x}, {y}) i kliknięto.")

# ---- GENEROWANIE KODU ----
def kicia_generate_code(prompt, on_demand=False):
    """Generuje kod na żądanie użytkownika (np. przez OpenAI)."""
    if not on_demand:
        return None
    import openai
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print("Brak klucza API OpenAI.")
        return None
    openai.api_key = openai_api_key
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Jesteś asystentem programistycznym. Generuj tylko kod, bez wyjaśnień."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.2
        )
        code = response.choices[0].message.content
        filename = "generated_code.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
        print(f"[Kicia] Wygenerowałam kod i zapisałam do pliku {filename}")
        return filename
    except Exception as e:
        print(f"Błąd generowania kodu: {e}")
        return None

# ---- INSTALACJA BIBLIOTEK ----
def kicia_install_package(package_name, on_demand=False):
    """Instaluje bibliotekę przez pip na żądanie użytkownika."""
    if not on_demand:
        return
    import subprocess
    try:
        print(f"[Kicia] Instaluję pakiet: {package_name}")
        subprocess.run([sys.executable, "-m", "pip", "install", package_name], check=True)
        print(f"[Kicia] Pakiet {package_name} został zainstalowany.")
    except Exception as e:
        print(f"Błąd instalacji pakietu {package_name}: {e}")

# ---- KONFIGURACJA KRYPTOWALUT ----
ZAZULCOIN_TO_KRYPTOZLOTOWKA = 1000
KRYPTOZLOTOWKA_TO_ZAZULTOKEN = 1000
KRYPTOZLOTOWKA_MAX_SUPPLY = 21_000_000  # Ograniczona ilość jak Bitcoin

WALUTY_FILARY = {
    "ZazulCoin": {
        "solana": 0.3,
        "polygon": 0.3,
        "bsc": 0.3,  # Binance Smart Chain jako trzeci filar
    },
    "Kryptozlotowka": {
        "solana": 0.3,
        "polygon": 0.3,
        "bsc": 0.3,
    },
    "ZazulToken": {
        "solana": 0.3,
        "polygon": 0.3,
        "bsc": 0.3,
    }
}

def rozklad_na_filary(waluta, ilosc):
    """Zwraca rozkład ilości danej waluty na trzy filary."""
    if waluta not in WALUTY_FILARY:
        return {}
    return {chain: ilosc * udzial for chain, udzial in WALUTY_FILARY[waluta].items()}

# Przeliczenia

def przelicz_zazulcoin_na_kryptozlotowki(zazulcoin):
    return zazulcoin * ZAZULCOIN_TO_KRYPTOZLOTOWKA

def przelicz_kryptozlotowki_na_zazultoken(kryptozlotowki):
    return kryptozlotowki * KRYPTOZLOTOWKA_TO_ZAZULTOKEN

def przelicz_zazulcoin_na_zazultoken(zazulcoin):
    return zazulcoin * ZAZULCOIN_TO_KRYPTOZLOTOWKA * KRYPTOZLOTOWKA_TO_ZAZULTOKEN

def przelicz_zazultoken_na_zazulcoin(zazultoken):
    return zazultoken / (ZAZULCOIN_TO_KRYPTOZLOTOWKA * KRYPTOZLOTOWKA_TO_ZAZULTOKEN)

# ---- PRZYKŁAD UŻYCIA ŚWIADOMOŚCI I POWITANIA ----
def kicia_przedstaw_sie(user_preferences):
    print("[Kicia]: Przypominam sobie, kim jestem...")
    print(KICIA_SYSTEM_PROMPT)
    powitanie = kicia_powitanie(user_preferences)
    print(f"[Kicia]: {powitanie}")
    # Jeśli chcesz, by Kicia mówiła na głos:
    # kicia_speak(powitanie, eleven_api_key=eleven_api_key, local_tts_engine=local_tts_engine)

# Przykład użycia w asystencie:
def find_in_reference_docs(query):
    """Wyszukuje zapytanie w dokumentach referencyjnych i zwraca fragmenty z dopasowaniem."""
    results = []
    for filename, content in REFERENCE_DOCS.items():
        if query.lower() in content.lower():
            # Znajdź fragment z dopasowaniem
            idx = content.lower().find(query.lower())
            start = max(0, idx - 100)
            end = min(len(content), idx + 300)
            snippet = content[start:end].replace('\n', ' ')
            results.append((filename, snippet))
    return results

# ---- OBSŁUGA KOMEND GŁOSOWYCH ----
def handle_voice_command(user_input, eleven_api_key=None, local_tts_engine=None):
    """Obsługuje konkretne komendy głosowe użytkownika dla Kici."""
    user_input = user_input.lower()
    if "przedstaw się" in user_input or "kim jesteś" in user_input:
        kicia_przedstaw_sie(user_preferences)
        kicia_speak(kicia_powitanie(user_preferences), eleven_api_key, local_tts_engine)
        return
    if "zrób zdjęcie" in user_input or "kamera" in user_input:
        filename = kicia_capture_camera(on_demand=True)
        if filename:
            kicia_speak("Zrobiłam zdjęcie z kamery.", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Nie udało się zrobić zdjęcia z kamery.", eleven_api_key, local_tts_engine)
        return
    if "zrób zrzut ekranu" in user_input or "ekran" in user_input:
        filename = kicia_capture_screen(on_demand=True)
        if filename:
            kicia_speak("Wykonałam zrzut ekranu.", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Nie udało się wykonać zrzutu ekranu.", eleven_api_key, local_tts_engine)
        return
    if "napisz" in user_input or "wpisz" in user_input:
        # Przykład: "napisz Witaj, to ja Kicia!"
        text_to_type = user_input.replace("napisz", "").replace("wpisz", "").strip()
        if text_to_type:
            kicia_type_text(text_to_type, on_demand=True)
            kicia_speak(f"Wpisałam tekst: {text_to_type}", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Podaj tekst do wpisania.", eleven_api_key, local_tts_engine)
        return
    if "przesuń myszkę" in user_input or "kliknij" in user_input:
        # Przykład: "przesuń myszkę na 100 200" lub "kliknij na 100 200"
        import re
        coords = re.findall(r"\d+", user_input)
        if len(coords) >= 2:
            x, y = int(coords[0]), int(coords[1])
            kicia_move_mouse(x, y, on_demand=True)
            kicia_speak(f"Przesunęłam myszkę do punktu {x}, {y} i kliknęłam.", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Podaj współrzędne do przesunięcia myszki.", eleven_api_key, local_tts_engine)
        return
    if "napisz kod" in user_input or "wygeneruj kod" in user_input:
        # Przykład: "napisz kod do pobierania danych z API"
        code_prompt = user_input.replace("napisz kod", "").replace("wygeneruj kod", "").strip()
        if code_prompt:
            filename = kicia_generate_code(code_prompt, on_demand=True)
            if filename:
                kicia_speak(f"Wygenerowałam kod i zapisałam do pliku {filename}", eleven_api_key, local_tts_engine)
            else:
                kicia_speak("Nie udało się wygenerować kodu.", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Podaj, jaki kod mam napisać.", eleven_api_key, local_tts_engine)
        return
    if "zainstaluj bibliotekę" in user_input or "zainstaluj pakiet" in user_input:
        # Przykład: "zainstaluj bibliotekę requests"
        import re
        pkg = user_input.replace("zainstaluj bibliotekę", "").replace("zainstaluj pakiet", "").strip()
        if pkg:
            kicia_install_package(pkg, on_demand=True)
            kicia_speak(f"Zainstalowałam pakiet {pkg}", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Podaj nazwę pakietu do instalacji.", eleven_api_key, local_tts_engine)
        return
    if "znajdź w dokumentacji" in user_input or "znajdź w plikach" in user_input:
        query = user_input.replace("znajdź w dokumentacji", "").replace("znajdź w plikach", "").strip()
        results = find_in_reference_docs(query)
        if results:
            for filename, snippet in results[:3]:
                kicia_speak(f"Znalazłam w {filename}: {snippet}", eleven_api_key, local_tts_engine)
        else:
            kicia_speak("Nie znalazłam informacji w dokumentacji.", eleven_api_key, local_tts_engine)
        return
    # ...dodaj kolejne komendy według potrzeb...