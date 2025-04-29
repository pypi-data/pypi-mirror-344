
# [RTASP - Real-Time Annotation and Stream Processing](http://www.rtasp.com) [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/docs/README.md)

RTASP to modularny system do wykrywania, przetwarzania i analizy strumieni wideo w czasie rzeczywistym. System umożliwia łatwą integrację z kamerami IP, mikrofonami i innymi źródłami sygnału, a także zapewnia zaawansowane możliwości adnotacji i analizy przy użyciu modułów AI.

## Główne funkcje

- **Automatyczne wykrywanie kamer RTSP** w sieci lokalnej
- **Zarządzanie strumieniami wideo** z różnych źródeł
- **Przetwarzanie AI** (wykrywanie ruchu, obiektów, twarzy, rozpoznawanie mowy)
- **Interfejs webowy** do zarządzania systemem
- **Protokół komunikacyjny MCP** (Message Communication Protocol) do integracji modułów
- **Nagrywanie i wykonywanie zrzutów ekranu**
- **Modułowa architektura** umożliwiająca łatwe rozszerzanie funkcjonalności

## Szybka instalacja

Aby zainstalować RTASP na systemie Debian/Ubuntu/Raspberry Pi OS, wykonaj następującą komendę:

```bash
curl -sSL https://raw.githubusercontent.com/rt-asp/python/main/scripts/quick-install.sh | sudo bash
```

System zostanie zainstalowany w katalogu `/opt/rtasp` i uruchomiony jako usługa systemd.

## Wymagania systemowe

- Python 3.8 lub nowszy
- System operacyjny: Debian, Ubuntu, Raspberry Pi OS (lub inny oparty na Linuxie)
- Minimum 2GB RAM (4GB zalecane)
- Minimum 1GB wolnego miejsca na dysku (więcej w przypadku nagrywania strumieni)

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/docs/INSTALL.md)
## Ręczna instalacja

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/rt-asp/python.git rtasp
   cd rtasp
   ```

2. Uruchom skrypt instalacyjny:
   ```bash
   sudo bash scripts/install.sh
   ```

3. Po instalacji, RTASP zostanie uruchomiony jako usługa systemd. Możesz uzyskać dostęp do interfejsu webowego pod adresem `http://localhost:8080` lub `http://<adres-ip-serwera>:8080`.

## Konfiguracja

Główny plik konfiguracyjny znajduje się w `/opt/rtasp/config/config.yaml`. Możesz go edytować, aby dostosować system do swoich potrzeb. Po dokonaniu zmian, uruchom ponownie usługę:

```bash
sudo systemctl restart rtasp.service
```

## Ręczne uruchamianie

RTASP można również uruchomić ręcznie:

```bash
rtasp  # Używa domyślnej konfiguracji

# Lub z określonym plikiem konfiguracyjnym:
rtasp -c /ścieżka/do/config.yaml

# Tryb skanowania sieci w poszukiwaniu kamer RTSP:
rtasp -s
```

## Struktura projektu

```
rtasp/
├── config/                    # Katalog konfiguracyjny
├── core/                      # Główne moduły systemu
├── ai_modules/                # Moduły przetwarzania AI
├── web/                       # Interfejs webowy
├── models/                    # Folder na modele AI
├── tools/                     # Narzędzia pomocnicze
├── scripts/                   # Skrypty pomocnicze
├── tests/                     # Testy jednostkowe
├── docs/                      # Dokumentacja
├── main.py                    # Główny plik uruchomieniowy
└── requirements.txt           # Zależności Pythona
```

## Protokół komunikacyjny MCP

System wykorzystuje wewnętrzny protokół komunikacyjny MCP (Message Communication Protocol) oparty na wzorcu Publish-Subscribe. Umożliwia to luźne powiązanie komponentów systemu i łatwą rozbudowę. 

Przykład użycia MCP:

```python
from core.mcp import MCPClient

# Utworzenie klienta MCP
client = MCPClient(broker, client_id="my_module")

# Subskrypcja zdarzeń
client.subscribe("stream/+/frame", handle_frame)
client.subscribe("ai/face_recognition/result", handle_face_result)

# Publikowanie zdarzeń
client.publish("command/stream/start/camera1", {})
```

## Moduły AI

System zawiera następujące moduły AI:

- **motion_detection** - wykrywanie ruchu w strumieniu wideo
- **object_detection** - wykrywanie i klasyfikacja obiektów
- **face_recognition** - rozpoznawanie twarzy
- **speech_recognition** - rozpoznawanie mowy
- **audio_processor** - analiza dźwięku

## Rozszerzanie systemu

RTASP został zaprojektowany z myślą o łatwej rozbudowie. Możesz tworzyć własne moduły AI, dodawać nowe źródła strumieni i integrować system z innymi aplikacjami.

### Tworzenie własnego modułu AI

1. Utwórz nowy plik w katalogu `ai_modules`:

```python
# ai_modules/my_custom_module.py
import cv2
import numpy as np

class MyCustomModule:
    def __init__(self, config=None):
        self.config = config or {}
        
    def process_frame(self, frame):
        # Przetwarzanie klatki wideo
        processed_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        return {
            "processed_frame": processed_frame,
            "result": "Przykładowy wynik"
        }
        
    def process_audio(self, audio_chunk):
        # Opcjonalne przetwarzanie audio
        return None
```

2. Zarejestruj moduł w `ai_modules/__init__.py`:

```python
from .my_custom_module import MyCustomModule

available_modules = {
    # Inne moduły...
    "my_custom_module": MyCustomModule
}
```

3. Włącz moduł w konfiguracji:

```yaml
ai:
  enabled_modules: ["motion_detection", "my_custom_module"]
```

## Rozwiązywanie problemów

Jeśli napotkasz problemy:

1. Sprawdź logi systemowe:
   ```bash
   journalctl -u rtasp.service -f
   ```

2. Sprawdź status usługi:
   ```bash
   systemctl status rtasp.service
   ```

3. Sprawdź logi aplikacji:
   ```bash
   cat /opt/rtasp/logs/rtasp.log
   ```

## Licencja

RTASP jest udostępniany na licencji MIT. Szczegóły znajdziesz w pliku LICENSE.

## Kontakt i zgłaszanie problemów

Jeśli napotkasz problemy lub masz sugestie, utwórz zgłoszenie na GitHub.

---

Projekt RTASP (Real-Time Audio and Stream Processing)

---
+ Modular Documentation made possible by the [FlatEdit](http://www.flatedit.com) project.
