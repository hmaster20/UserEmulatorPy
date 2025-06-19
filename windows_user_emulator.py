
import pyautogui
import pygetwindow as gw
import psutil
import keyboard
import random
import time
import subprocess

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

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

def scroll_like_reading():
    for _ in range(random.randint(1, 3)):
        pyautogui.scroll(-random.randint(100, 300))
        time.sleep(random.uniform(1.5, 3.5))

def select_and_deselect_text():
    pyautogui.moveRel(0, 20, duration=0.5)
    pyautogui.dragRel(0, 50, duration=1, button='left')
    time.sleep(random.uniform(1, 2))
    pyautogui.click()

def move_mouse_idle():
    for _ in range(random.randint(1, 2)):
        x, y = pyautogui.position()
        pyautogui.moveTo(x + random.randint(-30, 30), y + random.randint(-30, 30), duration=0.5)
        time.sleep(random.uniform(1, 2))

def move_mouse_in_window(win):
    if not win:
        return
    left, top, width, height = win.left, win.top, win.width, win.height
    for _ in range(random.randint(1, 3)):
        x = random.randint(left + 50, left + width - 50)
        y = random.randint(top + 50, top + height - 50)
        pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.2))
        time.sleep(random.uniform(0.5, 1.5))

def simulate_behavior():
    title = get_active_window_title()
    proc = get_active_process_name()
    win = gw.getActiveWindow()

    if any(app in title for app in ['chrome', 'firefox', 'edge']) or 'chrome.exe' in proc:
        scroll_like_reading()
        move_mouse_in_window(win)
        if random.random() < 0.4:
            select_and_deselect_text()
    elif 'notepad++' in title or 'notepad++.exe' in proc:
        scroll_like_reading()
        move_mouse_in_window(win)
    elif 'code' in title or 'code.exe' in proc:
        scroll_like_reading()
        move_mouse_in_window(win)
    elif 'explorer' in title or 'explorer.exe' in proc:
        navigate_explorer()
        move_mouse_in_window(win)
    elif 'outlook' in title or 'teams' in title or proc in ['outlook.exe', 'teams.exe']:
        scroll_like_reading()
        move_mouse_in_window(win)
    elif 'powershell ise' in title or 'powershell_ise.exe' in proc:
        scroll_like_reading()
        move_mouse_in_window(win)
    elif 'word' in title or 'winword.exe' in proc:
        scroll_like_reading()
        move_mouse_in_window(win)
    elif 'excel' in title or 'excel.exe' in proc:
        scroll_like_reading()
        move_mouse_in_window(win)
    elif 'mremote' in title or 'mremote.exe' in proc:
        move_mouse_in_window(win)
    else:
        move_mouse_idle()

def is_start_button_area(x, y):
    return x < 100

def click_taskbar():
    screen_width, screen_height = pyautogui.size()
    y = screen_height - 10
    x = random.randint(200, screen_width - 200)
    pyautogui.moveTo(x, y, duration=0.5)
    if not is_start_button_area(x, y):
        pyautogui.click()

def switch_window():
    pyautogui.hotkey('alt', 'tab')
    time.sleep(random.uniform(0.5, 1.5))

def open_random_app():
    app = random.choice(['calc', 'snippingtool'])
    subprocess.Popen(app)
    time.sleep(3)

def navigate_explorer():
    if random.random() < 0.5:
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.5)
        pyautogui.typewrite('D:\\', interval=0.1)
        pyautogui.press('enter')
        time.sleep(1)

def focus_vscode_terminal_browser():
    apps = ['chrome', 'code', 'powershell']
    wins = [w for w in gw.getWindowsWithTitle('') if any(app in w.title.lower() for app in apps)]
    if wins:
        win = random.choice(wins)
        win.activate()
        time.sleep(random.uniform(1, 2))

def check_exit_key():
    if keyboard.is_pressed('ctrl+alt+f12'):
        print("Остановка по ctrl+alt+f12")
        exit()

def main():
    print("Эмулятор запущен. Ctrl+Alt+F12 для остановки.")
    time.sleep(3)
    last_mail_time = time.time()
    try:
        while True:
            check_exit_key()
            action = random.choices(
                ['simulate', 'switch', 'taskbar', 'apps', 'pause', 'refocus'],
                weights=[40, 10, 10, 10, 10, 20]
            )[0]

            if action == 'simulate':
                simulate_behavior()
            elif action == 'switch':
                switch_window()
            elif action == 'taskbar':
                click_taskbar()
            elif action == 'apps':
                open_random_app()
            elif action == 'pause':
                print("Размышление...")
                time.sleep(random.uniform(20, 60))
            elif action == 'refocus' and time.time() - last_mail_time > 60:
                focus_vscode_terminal_browser()
                last_mail_time = time.time()

            time.sleep(random.uniform(5, 15))
    except KeyboardInterrupt:
        print("Остановлено пользователем.")
    except pyautogui.FailSafeException:
        print("Остановлено (мышь в верхнем левом углу).")

if __name__ == "__main__":
    main()
