#!/bin/bash
# Skrypt uruchomieniowy dla asystenta g³osowego Kicia

# Kolory dla lepszej czytelnoœci
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
NC="\033[0m" # No Color

echo -e "${GREEN}=======================================================${NC}"
echo -e "${GREEN}      Kicia - Interaktywny Asystent G³osowy           ${NC}"
echo -e "${GREEN}=======================================================${NC}"

# Sprawdzenie, czy plik .env istnieje
if [ ! -f .env ]; then
    echo -e "${RED}Brak pliku .env z kluczami API.${NC}"
    echo -e "${YELLOW}Uruchamiam skrypt konfiguracyjny...${NC}"
    python3 kicia_setup.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}Konfiguracja nie powiod³a siê. Przerywam uruchamianie.${NC}"
        exit 1
    fi
fi

# Sprawdzenie, czy plik kicia_assistant.py istnieje
if [ ! -f kicia_assistant.py ]; then
    echo -e "${RED}Brak pliku kicia_assistant.py.${NC}"
    echo -e "${YELLOW}Uruchamiam skrypt konfiguracyjny...${NC}"
    python3 kicia_setup.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}Konfiguracja nie powiod³a siê. Przerywam uruchamianie.${NC}"
        exit 1
    fi
fi

# Uruchomienie asystenta
echo -e "${GREEN}Uruchamiam asystenta g³osowego Kicia...${NC}"
python3 kicia_assistant.py

# Sprawdzenie, czy asystent zakoñczy³ dzia³anie poprawnie
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Asystent zakoñczy³ dzia³anie poprawnie.${NC}"
else
    echo -e "${RED}Asystent zakoñczy³ dzia³anie z b³êdem.${NC}"
    echo -e "${YELLOW}SprawdŸ logi powy¿ej, aby zidentyfikowaæ problem.${NC}"
fi
