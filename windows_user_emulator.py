import pyautogui
import pygetwindow as gw
import random
import time

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        return win.title.lower() if win else ''
    except:
        return ''

def scroll_like_reading():
    for _ in range(random.randint(1, 3)):
        pyautogui.scroll(-random.randint(100, 300))
        time.sleep(random.uniform(1.5, 3.5))

def select_and_deselect_text():
    pyautogui.moveRel(0, 20, duration=0.5)
    pyautogui.dragRel(0, 50, duration=1, button='left')  # выделение
    time.sleep(random.uniform(1, 2))
    pyautogui.click()  # снятие выделения

def move_mouse_idle():
    for _ in range(random.randint(1, 2)):
        x, y = pyautogui.position()
        pyautogui.moveTo(x + random.randint(-30, 30), y + random.randint(-30, 30), duration=0.5)
        time.sleep(random.uniform(1, 2))

def simulate_behavior():
    title = get_active_window_title()
    
    if 'chrome' in title or 'firefox' in title or 'edge' in title:
        scroll_like_reading()
        if random.random() < 0.5:
            select_and_deselect_text()
    elif 'notepad++' in title or 'vscode' in title:
        scroll_like_reading()
    elif 'explorer' in title:
        move_mouse_idle()
    elif 'outlook' in title or 'teams' in title:
        scroll_like_reading()
    else:
        move_mouse_idle()

def click_taskbar():
    screen_width, screen_height = pyautogui.size()
    x = random.randint(100, screen_width - 100)
    y = screen_height - 10
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()

def switch_window():
    pyautogui.hotkey('alt', 'tab')
    time.sleep(random.uniform(0.5, 1.5))

def main():
    print("Эмулятор запущен. Переместите мышь в верхний левый угол экрана для остановки.")
    time.sleep(3)

    try:
        while True:
            action = random.choice(['simulate_behavior', 'switch_window', 'taskbar_click'])

            if action == 'simulate_behavior':
                simulate_behavior()
            elif action == 'switch_window':
                switch_window()
            elif action == 'taskbar_click':
                click_taskbar()

            time.sleep(random.uniform(5, 10))

    except KeyboardInterrupt:
        print("Остановлено пользователем.")
    except pyautogui.FailSafeException:
        print("Остановлено: мышь в верхнем левом углу.")

if __name__ == "__main__":
    main()
