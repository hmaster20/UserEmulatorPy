import pyautogui
import pygetwindow as gw
import psutil
import keyboard
import random
import time
import os
import sys
import logging
import json
from datetime import datetime
import webbrowser

# === Настройки ===
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
SAFE_AREA = (100, 100)  # Не перемещаем мышь в (0, 0) — это сигнал аварийной остановки
PAUSE_FACTOR = 0.8      # Уменьшение задержек на 20%
MOUSE_SPEED_FACTOR = 2.0

# === Логирование UTF-8 ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler("activity_log.txt", encoding="utf-8")
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# === Статистика окон ===
window_stats = {}
STATS_FILE = "window_stats.json"

def load_window_stats():
    global window_stats
    try:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            window_stats = json.load(f)
    except FileNotFoundError:
        window_stats = {}

def save_window_stats():
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(window_stats, f, ensure_ascii=False, indent=2)

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

def is_self_window(win):
    try:
        current_pid = os.getpid()
        return win and win._getWindowPid() == current_pid
    except:
        return False

def get_usable_windows():
    all_windows = gw.getAllWindows()
    usable = []
    logged_no_title = False
    for win in all_windows:
        title = win.title.strip()
        if not title:
            if not logged_no_title:
                try:
                    pid = win._getWindowPid()
                    proc_name = next((proc.name().lower() for proc in psutil.process_iter(['pid', 'name']) if proc.pid == pid), "unknown")
                    logger.info(f"Пропущено окно без заголовка, процесс: {proc_name}, hwnd: {win._hWnd}")
                    logged_no_title = True
                except:
                    logger.info("Пропущено окно без заголовка, информация о процессе недоступна")
                    logged_no_title = True
            continue
        if is_self_window(win):
            logger.info("Пропущено окно, в котором запущен скрипт.")
            continue
        usable.append(win)
    return usable

def move_mouse_safely():
    screen_width, screen_height = pyautogui.size()
    x = random.randint(SAFE_AREA[0], screen_width - 100)
    y = random.randint(SAFE_AREA[1], screen_height - 100)
    pyautogui.moveTo(x, y, duration=random.uniform(0.8, 1.8) * MOUSE_SPEED_FACTOR)

def move_mouse_in_window(win):
    if not win:
        return
    try:
        left, top, width, height = win.left, win.top, win.width, win.height
        for _ in range(random.randint(1, 2)):
            x = random.randint(left + 50, left + width - 50)
            y = random.randint(top + 50, top + height - 50)
            pyautogui.moveTo(x, y, duration=random.uniform(1.0, 2.5) * MOUSE_SPEED_FACTOR)
    except:
        pass

def scroll_like_reading():
    direction = random.choice([-1, 1])
    pyautogui.scroll(direction * random.randint(100, 300))
    time.sleep(random.uniform(1.5, 3.0) * PAUSE_FACTOR)

def switch_window_many():
    count = random.randint(2, 10)
    pyautogui.keyDown('alt')
    for _ in range(count):
        pyautogui.press('tab')
        time.sleep(random.uniform(0.1, 0.3))
    pyautogui.keyUp('alt')
    time.sleep(random.uniform(1.1, 2.8))

def click_taskbar_random():
    screen_width, screen_height = pyautogui.size()
    y = screen_height - random.randint(5, 40)
    x = random.randint(100, screen_width - 100)
    pyautogui.moveTo(x, y, duration=random.uniform(1.0, 2.5) * MOUSE_SPEED_FACTOR)
    pyautogui.click()
    log_action("Клик по панели задач")

def simulate_browser_tab_switch():
    direction = random.choice(["next", "prev"])
    if direction == "next":
        pyautogui.hotkey('ctrl', 'tab')
        log_action("Переключение на следующую вкладку")
    else:
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        log_action("Переключение на предыдущую вкладку")
    time.sleep(random.uniform(1.0, 2.5))

def simulate_habr_visit_and_scroll():
    log_action("Открытие Habr и прокрутка")
    webbrowser.open("https://habr.com/")
    time.sleep(5)
    for _ in range(random.randint(5, 10)):
        pyautogui.scroll(-300)
        time.sleep(random.uniform(1.0, 3.0))

def simulate_outlook_or_teams():
    for title in ["Outlook", "Teams"]:
        for w in gw.getWindowsWithTitle(title):
            try:
                w.activate()
                time.sleep(2)
                move_mouse_in_window(w)
                for _ in range(random.randint(2, 6)):
                    pyautogui.press(random.choice(['up', 'down']))
                    time.sleep(random.uniform(0.3, 0.7))
                log_action(f"Имитация просмотра {title}")
            except:
                continue

def simulate_explorer_behavior(win):
    action_count = random.randint(1, 5)
    log_action(f"Имитация работы в Проводнике, действий: {action_count}")
    for i in range(action_count):
        try:
            # Одиночный клик в окне
            move_mouse_in_window(win)
            pyautogui.click()
            log_action(f"Проводник: клик #{i+1}")
            time.sleep(random.uniform(2, 4))

            # Случайное действие: проверка или навигация
            if random.random() < 0.5:
                # Проверка: клик в другую область
                move_mouse_in_window(win)
                pyautogui.click()
                log_action("Проводник: клик в другую область для проверки")
            else:
                # Попытка зайти в папку или выйти назад
                if random.random() < 0.7:
                    pyautogui.doubleClick()
                    log_action("Проводник: попытка зайти в папку (двойной клик)")
                    time.sleep(random.uniform(3, 6))
                    if random.random() < 0.5:
                        pyautogui.doubleClick()
                        log_action("Проводник: повторный двойной клик (проверка папки)")
                    else:
                        pyautogui.hotkey('alt', 'up')
                        log_action("Проводник: возврат на уровень выше")
                else:
                    pyautogui.hotkey('alt', 'up')
                    log_action("Проводник: возврат на уровень выше")
            time.sleep(random.uniform(1, 4))
        except:
            log_action("Проводник: ошибка при выполнении действия")
            continue
    # Переход к другому окну
    switch_window_many()

def update_window_stats(proc, title):
    key = f"{proc}:{title}"
    if key not in window_stats:
        window_stats[key] = {"process": proc, "title": title, "interactions": 0, "last_accessed": time.time()}
    window_stats[key]["interactions"] += 1
    window_stats[key]["last_accessed"] = time.time()
    save_window_stats()

def simulate_unknown_window_behavior(win):
    action = random.choice(['mouse', 'scroll', 'switch'])
    if action == 'mouse':
        log_action("Движение мыши (unknown)")
        move_mouse_in_window(win)
    elif action == 'scroll':
        log_action("Прокрутка (unknown)")
        scroll_like_reading()
    elif action == 'switch':
        if random.random() < 0.5:
            switch_window_many()
        else:
            click_taskbar_random()

def simulate_behavior():
    windows = get_usable_windows()
    if not windows:
        log_action("Нет подходящих окон для взаимодействия.")
        return
    # Выбор окна с учётом весов из config.json
    weights = [config["apps"].get(get_active_process_name_for_window(win), {}).get("weight", 1.0) for win in windows]
    win = random.choices(windows, weights=weights, k=1)[0]
    try:
        win.activate()
        time.sleep(1.5)
    except:
        return

    proc = get_active_process_name()
    update_window_stats(proc, win.title)
    log_action(f"Активировано окно: {proc} - {win.title}")

    if proc in ["outlook.exe", "teams.exe"]:
        simulate_outlook_or_teams()
        return
    if proc == "explorer.exe":
        simulate_explorer_behavior(win)
        return

    actions = config["apps"].get(proc, {}).get("actions", [])
    if not actions:
        simulate_unknown_window_behavior(win)
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

def get_active_process_name_for_window(win):
    try:
        pid = win._getWindowPid()
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.pid == pid:
                return proc.name().lower()
    except:
        pass
    return "unknown"

def main():
    print("Эмулятор запущен. Нажмите Scroll Lock для остановки.")
    load_window_stats()
    last_thought_pause = time.time()
    last_switch_time = time.time()
    last_tab_switch = time.time()
    last_habr = time.time()

    try:
        while True:
            if keyboard.is_pressed("scroll lock"):
                print("Остановка пользователем (Scroll Lock)")
                log_action("Остановка по Scroll Lock")
                break

            if not is_within_work_hours():
                log_action("Вне времени работы. Ожидание...")
                time.sleep(60)
                continue

            if time.time() - last_thought_pause > random.randint(90, 180):
                pause_time = random.uniform(20, 75)
                log_action(f"Размышление: пауза {int(pause_time)} сек.")
                time.sleep(pause_time)
                last_thought_pause = time.time()

            if time.time() - last_switch_time > random.uniform(20, 240):
                if random.random() < 0.6:
                    switch_window_many()
                else:
                    click_taskbar_random()
                last_switch_time = time.time()

            if time.time() - last_tab_switch > random.uniform(60, 180):
                simulate_browser_tab_switch()
                last_tab_switch = time.time()

            # if time.time() - last_habr > random.uniform(300, 900):
            #     simulate_habr_visit_and_scroll()
            #     last_habr = time.time()

            simulate_behavior()
            time.sleep(random.uniform(1, 6))

    except KeyboardInterrupt:
        print("Остановлено вручную.")
        log_action("Остановка по KeyboardInterrupt")
    except pyautogui.FailSafeException:
        print("Fail-safe активация")
        log_action("Остановка через FailSafe")
    finally:
        save_window_stats()

if __name__ == "__main__":
    main()