import pygame
import sys
import os
import random
import time

# Настройки экрана и цветов
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Начальные значения
money = 0
hunger = 5
poop_count = 0
friendship = 0
pet_name = ""
poop_timer = time.time()  # Таймер для случайного добавления испражнений

# Инициализация Pygame
pygame.init()
font = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тамагочи")
clock = pygame.time.Clock()

# Загрузка изображений
tamagotchi_img = pygame.image.load("tmgc.png")  # Изображение тамагочи
coin_img = pygame.image.load("coin.png")  # Изображение монетки

# Функция для отрисовки текста
def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Функция для сохранения состояния в файл
def save_state():
    if pet_name:
        filename = f"TMGC_{pet_name}.txt"
        data = f"TMGC\n{pet_name}\n{money}\n{hunger}\n{poop_count}\n{friendship}\n"
        with open(filename, "w", encoding='utf-8') as f:  # Используем UTF-8
            f.write(data)
        print(f"Состояние сохранено в {filename}")

# Функция для загрузки состояния из файла
def load_state():
    global pet_name, money, hunger, poop_count, friendship
    found_file = False
    for filename in os.listdir():
        if filename.startswith("TMGC_") and filename.endswith(".txt"):
            found_file = True
            print(f"Найден файл сохранения: {filename}")
            with open(filename, "r", encoding='utf-8') as f:  # Используем UTF-8
                lines = f.read().splitlines()
                if lines[0].strip() == "TMGC":
                    pet_name = lines[1].strip()
                    money = int(lines[2].strip())
                    hunger = int(lines[3].strip())
                    poop_count = int(lines[4].strip())
                    friendship = int(lines[5].strip())
                    print("Состояние успешно загружено.")
                    return True  # Успешная загрузка
    if not found_file:
        print("Файл сохранения не найден.")
    return False  # Файл не найден или не подходит

# Функция ввода имени
def input_pet_name():
    global pet_name
    entering_name = True
    input_text = ""

    while entering_name:
        screen.fill(WHITE)
        draw_text("Введите имя вашего питомца: " + input_text, 150, 150)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN and input_text:
                    pet_name = input_text
                    entering_name = False
                else:
                    input_text += event.unicode

        clock.tick(30)  # Ограничение FPS для цикла ввода имени

# Основной игровой цикл
def main_game():
    global money, hunger, poop_count, friendship, poop_timer

    running = True

    while running:
        screen.fill(WHITE)

        # Отображение изображения тамагочи
        tamagotchi_rect = tamagotchi_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(tamagotchi_img, tamagotchi_rect)

        # Отображение интерфейса и статистики
        draw_text(f"1. Заработок", 50, 50)
        draw_text(f"2. Покормить зверька", 50, 80)
        draw_text(f"3. Убрать испражнения", 450, 50)
        draw_text(f"4. Погладить", 450, 80)
        draw_text(f"5. Сохранить", 50, 110)

        # Статистика
        draw_text(f"Деньги: {money}", 200, 10)
        draw_text(f"Сытость: {hunger}", 300, 10)
        draw_text(f"Испражнения: {poop_count}", 400, 10)
        draw_text(f"Имя зверька: {pet_name}", 10, 10)
        draw_text(f"Дружба: {friendship}", 10, 30)

        pygame.display.flip()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                # Кнопка 1 - заработок (включает кликер)
                if event.key == pygame.K_1:
                    show_clicker()

                # Кнопка 2 - покормить зверька
                elif event.key == pygame.K_2:
                    if money >= 10:
                        money -= 10
                        hunger += 1

                # Кнопка 3 - убрать испражнения
                elif event.key == pygame.K_3:
                    if poop_count > 0:
                        poop_count -= 1

                # Кнопка 4 - погладить
                elif event.key == pygame.K_4:
                    friendship += 1  # Увеличение дружбы

                # Кнопка 5 - сохранить состояние
                elif event.key == pygame.K_5:
                    save_state()

                # Кнопка Delete - выход и сохранение
                elif event.key == pygame.K_DELETE:
                    save_state()  # Сохранение состояния
                    pygame.quit()  # Выход из игры
                    sys.exit()  # Завершение программы

        # Рандомное увеличение испражнений
        if time.time() - poop_timer > random.randint(5, 15):
            poop_count += 1
            poop_timer = time.time()  # Сброс таймера

        clock.tick(30)  # Ограничение FPS для основного игрового цикла

# Кликерный режим
def show_clicker():
    global money
    in_clicker = True

    while in_clicker:
        screen.fill(WHITE)
        draw_text("Нажмите на монетку для заработка!", 180, 100)
        draw_text("Вернуться назад (ESC)", 50, 350)

        # Отображение изображения монетки
        coin_rect = coin_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(coin_img, coin_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_clicker = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка, кликнули ли по монетке
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if coin_rect.collidepoint(mouse_x, mouse_y):
                    money += 10

        clock.tick(30)  # Ограничение FPS для кликерного режима

# Запуск программы
if not load_state():  # Попытка загрузить данные, если нет файла, вводим имя
    input_pet_name()
main_game()  # Основной игровой цикл
