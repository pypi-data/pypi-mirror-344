
# rtasp [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/docs/README.md)
rtasp.rtasp.com

# rtasp

rtasp is a lightweight programming language embedded in Markdown that runs across multiple platforms including web browsers, terminal environments, desktop applications, and mobile devices.

## What is rtasp?

rtasp allows you to write both documentation and executable code in the same Markdown file. Code blocks tagged with ```rtasp are interpreted and executed by the rtasp runtime.

## Key Features

- **Write Once, Run Anywhere**: The same rtasp code works across all supported platforms
- **Embedded in Markdown**: Combine documentation and executable code in a single file
- **Platform-Specific APIs**: Access platform capabilities like file system, device sensors, etc.
- **Interactive Documents**: Create dynamic, interactive documentation
- **Easy to Learn**: Familiar JavaScript-like syntax

## Platform Implementation Guide

### Browser Implementation

The browser implementation uses JavaScript to interpret and execute rtasp code. It consists of:

1. An HTML file that provides the editor interface
2. A JavaScript interpreter that extracts code blocks and executes them
3. DOM manipulation capabilities for UI rendering

**Running in Browser:**
1. Open `index.html` in any modern browser
2. Write your rtasp code in the editor
3. Click "Run" to execute

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/docs/INSTALL.md)
### Terminal/Python Implementation

The Python implementation allows running rtasp in any terminal environment. It consists of:

1. A Python script (`rtasp.py`) that processes Markdown files
2. A code extractor and interpreter for rtasp code blocks
3. Python-based API for file system access and terminal commands

**Running in Terminal:**
```bash
# Execute a file
python rtasp.py example.md

# Start REPL mode
python rtasp.py --repl

# Create an example file
python rtasp.py --example
```

### Desktop Implementation (Electron)

The desktop implementation provides a native application experience using Electron. It consists of:

1. A main process (`main.js`) that handles application lifecycle
2. A renderer process (`index.html`) with the editor UI
3. IPC communication for file operations
4. Full system access through Node.js APIs

**Building for Desktop:**
```bash
# Install dependencies
npm install

# Run in development mode
npm start

# Build for distribution
npm run build
```

### Mobile Implementation (Android)

The Android implementation runs rtasp on mobile devices. It consists of:

1. A Kotlin-based Android app
2. A WebView for executing rtasp code
3. JavaScript interfaces for accessing device features (camera, sensors, etc.)
4. Integration with the Android filesystem

**Building for Android:**
1. Open the project in Android Studio
2. Connect an Android device or start an emulator
3. Build and run the app

## rtasp Syntax Examples

### Basic Syntax

```markdown
# My rtasp Program

This is a simple program.

```rtasp
// Variables
let name = "World";
let number = 42;

// Output
print("Hello, " + name + "!");
print("The answer is: " + number);
```



## Web

```bash      
cd web
```


1. **Użyj portu powyżej 1024** (najlepiej powyżej 8000):
   ```bash
   python -m http.server 8080
   ```

2. **Używaj poprawnej składni** - port podaje się bezpośrednio jako pierwszy argument:
   ```bash
   python -m http.server 8888
   ```

3. **Jeśli port jest zajęty**, możesz:
   - Użyć innego portu (np. 8001, 8080, 9000)
   - Zakończyć proces używający danego portu:
     ```bash
     # Znajdź proces używający portu 8000
     sudo lsof -i :8000
     # albo
     netstat -tuln | grep 8000
     
     # Zakończ proces (zastąp PID numerem procesu)
     kill PID
     ```

Spróbuj wykonać:
```bash
python -m http.server 8888
```

A następnie otwórz w przeglądarce adres:
```
http://localhost:8888
```

Jeśli nadal masz problemy z uruchomieniem serwera HTTP, możesz także wypróbować inne rozwiązania:

1. **Użyj innego serwera HTTP**, np. Node.js:
   ```bash
   npx serve
   ```

2. **Użyj PHP (jeśli zainstalowane)**:
   ```bash
   php -S localhost:8888
   ```

3. **Sprawdź, czy masz uprawnienia do zapisu w katalogu**, w którym próbujesz uruchomić serwer.



### Aplikacja desktopowa

Instalacja aplikacji desktopowej (bazującej na Electron):

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/rt-asp/rtasp.git
   cd rtasp/desktop
   ```

2. Zainstaluj zależności:
   ```bash
   npm install
   ```

3. Uruchom aplikację:
   ```bash
   npm start
   ```

4. (Opcjonalnie) Zbuduj aplikację dla swojego systemu:
   ```bash
   npm run build
   ```

### Urządzenia mobilne (Android)

Aby zainstalować rtasp na urządzeniu Android:

1. Pobierz plik APK z repozytorium lub sklepu Google Play
2. Uruchom plik APK na swoim urządzeniu
3. Zaakceptuj wymagane uprawnienia (dostęp do plików, kamera, itp.)
4. Aplikacja jest gotowa do użycia!

Alternatywnie, możesz zbudować aplikację z kodu źródłowego:

1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/rt-asp/rtasp.git
   ```

2. Otwórz folder `android` w Android Studio
3. Zbuduj i uruchom aplikację na emulatorze lub fizycznym urządzeniu

## Pierwsze kroki

Po zainstalowaniu rtasp, czas na pierwszy program:

1. Utwórz nowy plik tekstowy o rozszerzeniu `.md` (np. `pierwszy.md`)
2. Wpisz następującą treść:

 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/basic.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/default-example.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/dom.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/factorial-debug.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/files.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/minimal-python-factorial.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/multi-lang.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/number-display-test.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/python-example-with-js-comments.md)


 [<span style='font-size:20px;'>&#x270D;</span>](git@github.com:rt-asp/python/edit/main/web/examples/visualization.md)


---
+ Modular Documentation made possible by the [FlatEdit](http://www.flatedit.com) project.
