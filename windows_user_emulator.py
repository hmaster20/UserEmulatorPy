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

# === Настройки ===
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
SAFE_AREA = (100, 100)  # Не перемещаем мышь в (0, 0) — это сигнал аварийной остановки
PAUSE_FACTOR = 0.8      # Уменьшение задержек на 20%

# === Логирование с UTF-8 ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("activity_log.txt", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log_action(action):
    logger.info(f"Действие: {action}")

# === Загрузка конфигурации ===
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# === Проверка времени работы, опционально ===
def is_within_work_hours():
    mode = config.get("enable_work_hours", "enable").lower()
    if mode != "enable":
        return True
    now = datetime.now().time()
    start = datetime.strptime(config["work_hours"]["start"], "%H:%M").time()
    end = datetime.strptime(config["work_hours"]["end"], "%H:%M").time()
    return start <= now <= end

def get_active_process_name():
    try:
        win = gw.getActiveWindow()
        pid = win._getWindowPid() if win else None
        if pid:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.pid == pid:
                    return proc.name().lower()
    except Exception:
        pass
    return "unknown"

def move_mouse_safely():
    screen_width, screen_height = pyautogui.size()
    x = random.randint(SAFE_AREA[0], screen_width - 100)
    y = random.randint(SAFE_AREA[1], screen_height - 100)
    pyautogui.moveTo(x, y, duration=random.uniform(0.4, 0.9))

def move_mouse_in_window(win):
    if not win:
        return
    left, top, width, height = win.left, win.top, win.width, win.height
    for _ in range(random.randint(1, 2)):
        x = random.randint(left + 50, left + width - 50)
        y = random.randint(top + 50, top + height - 50)
        pyautogui.moveTo(x, y, duration=random.uniform(0.4, 1.0))

def scroll_like_reading():
    direction = random.choice([-1, 1])
    pyautogui.scroll(direction * random.randint(100, 300))
    time.sleep(random.uniform(1.5, 3.0) * PAUSE_FACTOR)

def switch_window():
    pyautogui.hotkey('alt', 'tab')
    time.sleep(random.uniform(0.5, 1.5) * PAUSE_FACTOR)

def simulate_unknown_window_behavior():
    # Поведение для неизвестных окон
    action = random.choice(['mouse', 'scroll', 'switch'])
    if action == 'mouse':
        log_action("Движение мыши (unknown)")
        move_mouse_safely()
    elif action == 'scroll':
        log_action("Прокрутка (unknown)")
        scroll_like_reading()
    elif action == 'switch':
        log_action("Переключение окна (unknown)")
        switch_window()

def simulate_behavior():
    proc = get_active_process_name()
    win = gw.getActiveWindow()
    actions = config["apps"].get(proc, {}).get("actions", [])

    if not actions:
        simulate_unknown_window_behavior()
        return

    for action in actions:
        if action == "scroll":
            log_action(f"{proc}: scroll")
            scroll_like_reading()
        elif action == "mouse_move":
            log_action(f"{proc}: mouse_move")
            move_mouse_in_window(win)
        elif action == "mouse_idle":
            log_action(f"{proc}: mouse_idle")
            move_mouse_safely()

def simulate_mail_check():
    log_action("Проверка почты в Outlook")
    for w in gw.getWindowsWithTitle("Outlook"):
        if "outlook" in w.title.lower():
            w.activate()
            time.sleep(1.5 * PAUSE_FACTOR)
            move_mouse_in_window(w)
            for _ in range(random.randint(2, 4)):
                pyautogui.press('down')
                time.sleep(random.uniform(0.5, 1.0) * PAUSE_FACTOR)
            break

    log_action("Проверка ссылки в Chrome")
    for w in gw.getWindowsWithTitle("Chrome"):
        if "chrome" in w.title.lower():
            w.activate()
            time.sleep(1.5 * PAUSE_FACTOR)
            move_mouse_in_window(w)
            scroll_like_reading()
            break

def main():
    print("Эмулятор запущен. Ctrl+Alt+F12 — остановка.")
    last_mail_check = time.time()
    last_thought_pause = time.time()

    try:
        while True:
            if keyboard.is_pressed("ctrl+alt+f12"):
                print("Остановка пользователем")
                log_action("Остановка по Ctrl+Alt+F12")
                break

            if not is_within_work_hours():
                log_action("Ожидание рабочего времени")
                time.sleep(60)
                continue

            if time.time() - last_mail_check > 300:
                simulate_mail_check()
                last_mail_check = time.time()

            if time.time() - last_thought_pause > random.randint(120, 300):
                pause_time = random.uniform(20, 75)
                log_action(f"Размышление ({int(pause_time)} сек)")
                time.sleep(pause_time)
                last_thought_pause = time.time()

            simulate_behavior()
            time.sleep(random.uniform(1, 7))

    except KeyboardInterrupt:
        print("Остановлено вручную.")
        log_action("Остановка по KeyboardInterrupt")
    except pyautogui.FailSafeException:
        print("Fail-safe активация (мышь в угол)")
        log_action("Остановка через FailSafe")

if __name__ == "__main__":
    main()
