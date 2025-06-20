# Эмулятор присутствия

```shell
# python -m venv --help

# Создаем виртуальное окружение
python -m venv venv

# Активируем его
venv\Scripts\activate

# Устанавливаем зависимости
pip install -r requirements.txt
# pip install pyautogui
# pip freeze > requirements.txt
# pip install --proxy http://server.local:3128 -r requirements.txt

python windows_user_emulator.py
```

## Сборка .exe из Python-скрипта

Будет использоваться PyInstaller:
Создаётся dist/windows_user_emulator.exe — файл, не требующий Python.

Для сборки без консольного окна: замени console=True на console=False в .spec.
Чтобы добавить иконку: в EXE(...) укажи параметр icon='icon.ico'.

В командной строке:
можно скрыть консольное окно (--noconsole),
можно добавить иконку .ico (--icon=icon.ico),

```shell
pip install pyinstaller

pyinstaller windows_user_emulator.spec
# pyinstaller --onefile windows_user_emulator.py

```
