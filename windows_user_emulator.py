import pyautogui
import pygetwindow as gw
import psutil
import keyboard
import random
import time
import subprocess
import logging
import json
from datetime import datetime

# === Настройки и логика ===
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
PAUSE_FACTOR = 0.8  # Уменьшение задержек на 20%

# === Логирование ===
logging.basicConfig(
    filename="activity_log.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_action(action):
    logging.info(f"Действие: {action}")

# === Загрузка конфигурации из файла ===
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# === Проверка рабочего времени ===
def is_within_work_hours():
    now = datetime.now().time()
    start = datetime.strptime(config["work_hours"]["start"], "%H:%M").time()
    end = datetime.strptime(config["work_hours"]["end"], "%H:%M").time()
    return start <= now <= end

# === Получение текущего активного окна и процесса ===
def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        return win.title.lower() if win else ''
    except:
        return ''

def get_active_process_name():
    win = gw.getActiveWindow()
    if not win:
        return ""
    try:
        pid = win._getWindowPid()
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.pid == pid:
                return proc.name().lower()
    except Exception:
        return ""
    return ""

# === Перемещение мыши внутри окна ===
def move_mouse_in_window(win):
    if not win:
        return
    log_action("Перемещение мыши внутри окна")
    left, top, width, height = win.left, win.top, win.width, win.height
    for _ in range(random.randint(1, 3)):
        x = random.randint(left + 50, left + width - 50)
        y = random.randint(top + 50, top + height - 50)
        pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.2))
        time.sleep(random.uniform(0.5, 1.5) * PAUSE_FACTOR)

# === Прокрутка как при чтении ===
def scroll_like_reading():
    log_action("Прокрутка")
    for _ in range(random.randint(1, 3)):
        pyautogui.scroll(-random.randint(100, 300))
        time.sleep(random.uniform(1.5, 3.5) * PAUSE_FACTOR)

# === Симуляция чтения почты и перехода в браузер (Идея 2) ===
def simulate_mail_check():
    """Имитация чтения почты и проверки ссылки (Outlook + Chrome)"""
    log_action("Имитируем чтение почты в Outlook")
    for w in gw.getWindowsWithTitle("Outlook"):
        if "outlook" in w.title.lower():
            w.activate()
            time.sleep(2 * PAUSE_FACTOR)
            move_mouse_in_window(w)

            # Имитируем движение по списку писем
            for _ in range(random.randint(2, 4)):
                pyautogui.press('down')
                time.sleep(random.uniform(0.6, 1.2) * PAUSE_FACTOR)
            break

    log_action("Переход в Chrome (проверка ссылки)")
    for w in gw.getWindowsWithTitle("Chrome"):
        if "chrome" in w.title.lower():
            w.activate()
            time.sleep(1.5 * PAUSE_FACTOR)
            move_mouse_in_window(w)
            scroll_like_reading()
            break

# === Симуляция поведения по текущему окну ===
def simulate_behavior():
    title = get_active_window_title()
    proc = get_active_process_name()
    win = gw.getActiveWindow()

    behavior = config["apps"].get(proc, {})
    actions = behavior.get("actions", [])
    for action in actions:
        if action == "scroll":
            scroll_like_reading()
        elif action == "mouse_move":
            move_mouse_in_window(win)

# === Основной цикл ===
def main():
    print("Эмулятор запущен. Ctrl+Alt+F12 для остановки.")
    last_mail_check = time.time()

    try:
        while True:
            if keyboard.is_pressed("ctrl+alt+f12"):
                print("Остановка по Ctrl+Alt+F12")
                log_action("Остановка пользователем")
                break

            if not is_within_work_hours():
                log_action("Вне рабочего времени — ожидание")
                time.sleep(60)
                continue

            # Каждые ~5 минут делаем проверку Outlook + Chrome
            if time.time() - last_mail_check > 300:
                simulate_mail_check()
                last_mail_check = time.time()

            # Основное поведение в текущем окне
            simulate_behavior()

            # Пауза между действиями
            time.sleep(random.uniform(5, 10) * PAUSE_FACTOR)

    except KeyboardInterrupt:
        print("Остановлено вручную.")
        log_action("Остановка вручную")

if __name__ == "__main__":
    main()
