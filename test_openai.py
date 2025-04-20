"""
Test połączenia z API OpenAI
"""

import os
import openai
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    print("❌ Brak klucza API OpenAI w pliku .env")
    print("Proszę dodać klucz API do pliku .env:")
    print("OPENAI_API_KEY=twój_klucz_api")
    exit(1)

# Konfiguracja OpenAI
openai.api_key = openai_api_key

try:
    # Testowanie połączenia z OpenAI
    print("Testowanie połączenia z API OpenAI...")
    
    # Tworzenie prostego zapytania do modelu
    response = openai.chat.completions.create(
        model="gpt-4o",  # Użyj dostępnego modelu (GPT-4o lub inny dostępny)
        messages=[
            {"role": "system", "content": "Jesteś asystentem o imieniu Kicia."},
            {"role": "user", "content": "Przedstaw się krótko."}
        ]
    )
    
    # Wyświetlanie odpowiedzi
    assistant_response = response.choices[0].message.content
    print("\nOdpowiedź od OpenAI:")
    print(f"{assistant_response}")
    
    print("\n✅ Test API OpenAI zakończony pomyślnie!")
    print("Połączenie z OpenAI działa poprawnie.")
    
except Exception as e:
    print(f"❌ Błąd podczas testowania API OpenAI: {e}")
    print("Sprawdź, czy klucz API jest poprawny i czy masz dostęp do API OpenAI.")
