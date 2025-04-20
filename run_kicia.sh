#!/bin/bash
# Skrypt uruchomieniowy dla asystenta g�osowego Kicia

# Kolory dla lepszej czytelno�ci
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
NC="\033[0m" # No Color

echo -e "${GREEN}=======================================================${NC}"
echo -e "${GREEN}      Kicia - Interaktywny Asystent G�osowy           ${NC}"
echo -e "${GREEN}=======================================================${NC}"

# Sprawdzenie, czy plik .env istnieje
if [ ! -f .env ]; then
    echo -e "${RED}Brak pliku .env z kluczami API.${NC}"
    echo -e "${YELLOW}Uruchamiam skrypt konfiguracyjny...${NC}"
    python3 kicia_setup.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}Konfiguracja nie powiod�a si�. Przerywam uruchamianie.${NC}"
        exit 1
    fi
fi

# Sprawdzenie, czy plik kicia_assistant.py istnieje
if [ ! -f kicia_assistant.py ]; then
    echo -e "${RED}Brak pliku kicia_assistant.py.${NC}"
    echo -e "${YELLOW}Uruchamiam skrypt konfiguracyjny...${NC}"
    python3 kicia_setup.py
    if [ $? -ne 0 ]; then
        echo -e "${RED}Konfiguracja nie powiod�a si�. Przerywam uruchamianie.${NC}"
        exit 1
    fi
fi

# Uruchomienie asystenta
echo -e "${GREEN}Uruchamiam asystenta g�osowego Kicia...${NC}"
python3 kicia_assistant.py

# Sprawdzenie, czy asystent zako�czy� dzia�anie poprawnie
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Asystent zako�czy� dzia�anie poprawnie.${NC}"
else
    echo -e "${RED}Asystent zako�czy� dzia�anie z b��dem.${NC}"
    echo -e "${YELLOW}Sprawd� logi powy�ej, aby zidentyfikowa� problem.${NC}"
fi
