import pyautogui
import random
import time

# Настройка pyautogui
pyautogui.FAILSAFE = True  # Перемещение мыши в верхний левый угол останавливает программу
pyautogui.PAUSE = 0.5  # Пауза между действиями pyautogui (в секундах)

def move_mouse_randomly():
    """Перемещает мышь в случайную позицию на экране."""
    screen_width, screen_height = pyautogui.size()
    x = random.randint(100, screen_width - 100)  # Избегаем краев экрана
    y = random.randint(100, screen_height - 100)
    pyautogui.moveTo(x, y, duration=random.uniform(0.1, 0.5))

def click_randomly():
    """Выполняет случайный клик мышью."""
    pyautogui.click()

def switch_window():
    """Эмулирует переключение между окнами с помощью ALT+TAB."""
    pyautogui.hotkey('alt', 'tab')
    time.sleep(random.uniform(0.5, 1.5))  # Пауза после переключения

def click_taskbar():
    """Эмулирует клик по панели задач."""
    screen_width, screen_height = pyautogui.size()
    # Панель задач обычно внизу экрана, выбираем случайную позицию по горизонтали
    x = random.randint(100, screen_width - 100)
    y = screen_height - 20  # Примерно в области панели задач
    pyautogui.moveTo(x, y, duration=random.uniform(0.2, 0.6))
    pyautogui.click()

def main():
    """Основная функция эмулятора."""
    print("Эмулятор запущен. Переместите мышь в верхний левый угол экрана для остановки.")
    time.sleep(3)  # Даем пользователю время подготовиться

    try:
        while True:
            action = random.choice(['move_mouse', 'click', 'switch_window', 'taskbar_click'])
            
            if action == 'move_mouse':
                move_mouse_randomly()
            elif action == 'click':
                click_randomly()
            elif action == 'switch_window':
                switch_window()
            elif action == 'taskbar_click':
                click_taskbar()
            
            # Случайная пауза между действиями
            time.sleep(random.uniform(1, 3))

    except KeyboardInterrupt:
        print("Эмулятор остановлен пользователем.")
    except pyautogui.FailSafeException:
        print("Эмулятор остановлен (мышь в верхнем левом углу).")

if __name__ == "__main__":
    main()