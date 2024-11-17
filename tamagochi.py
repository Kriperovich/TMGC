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
selected_pet_image = "tmgc.png"  # По умолчанию изображение тамагочи
poop_timer = time.time()  # Таймер для случайного добавления испражнений

# Инициализация Pygame
pygame.init()
font = pygame.font.Font(None, 24)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Тамагочи")
clock = pygame.time.Clock()

# Загрузка изображений питомцев
pet_images = {
    "cat": pygame.image.load("cat.png"),
    "dog": pygame.image.load("hotdog.png"),
    "human": pygame.image.load("hooman.png")
}

# Функция для отрисовки текста
def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Функция для сохранения состояния в файл
def save_state():
    if pet_name:
        filename = f"TMGC_{pet_name}.txt"
        data = f"TMGC\n{pet_name}\n{money}\n{hunger}\n{poop_count}\n{friendship}\n{selected_pet_image}\n"
        with open(filename, "w", encoding='utf-8') as f:
            f.write(data)
        print(f"Состояние сохранено в {filename}")

# Функция для загрузки состояния из файла
def load_state(filename):
    global pet_name, money, hunger, poop_count, friendship, selected_pet_image
    with open(filename, "r", encoding='utf-8') as f:
        lines = f.read().splitlines()
        if lines[0].strip() == "TMGC":
            pet_name = lines[1].strip()
            money = int(lines[2].strip())
            hunger = int(lines[3].strip())
            poop_count = int(lines[4].strip())
            friendship = int(lines[5].strip())
            selected_pet_image = lines[6].strip()
            print(f"Состояние успешно загружено из {filename}")
            return True
    print("Файл сохранения не найден или поврежден.")
    return False

# Функция для выбора сохранения
def select_save_file():
    save_files = [f for f in os.listdir() if f.startswith("TMGC_") and f.endswith(".txt")]
    if not save_files:
        print("Нет доступных файлов сохранения.")
        return None

    selected_index = 0
    selecting = True

    while selecting:
        screen.fill(WHITE)
        draw_text("Выберите файл сохранения:", 150, 50)

        for i, filename in enumerate(save_files):
            color = BLACK if i != selected_index else (0, 0, 255)  # Синий для выбранного
            draw_text(filename, 200, 100 + i * 30, color)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = (selected_index - 1) % len(save_files)
                elif event.key == pygame.K_DOWN:
                    selected_index = (selected_index + 1) % len(save_files)
                elif event.key == pygame.K_RETURN:
                    return save_files[selected_index]

        clock.tick(30)

# Функция для выбора питомца
def choose_pet():
    global selected_pet_image
    choosing = True

    while choosing:
        screen.fill(WHITE)
        draw_text("Выберите питомца:", 150, 50)
        draw_text("1. Кот", 150, 100)
        draw_text("2. Собака", 150, 130)
        draw_text("3. Человек", 150, 160)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_pet_image = "cat.png"
                    choosing = False
                elif event.key == pygame.K_2:
                    selected_pet_image = "hotdog.png"
                    choosing = False
                elif event.key == pygame.K_3:
                    selected_pet_image = "hooman.png"
                    choosing = False

        clock.tick(30)

# Функция ввода имени
def input_pet_name():
    global pet_name
    input_text = ""
    entering_name = True

    while entering_name:
        screen.fill(WHITE)
        draw_text(f"Введите имя питомца: {input_text}", 150, 150)
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

        clock.tick(30)

# Функция смерти питомца
def pet_died():
    global pet_name
    screen.fill(WHITE)
    draw_text(f"{pet_name} умер", 200, 150, color=(255, 0, 0))
    draw_text("Закройте это окно, чтобы продолжить", 150, 200)
    pygame.display.flip()

    # Удаление сохранения
    save_file = f"TMGC_{pet_name}.txt"
    if os.path.exists(save_file):
        os.remove(save_file)
        print(f"Сохранение {save_file} удалено.")

    # Ожидание закрытия окна
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

# Основной игровой цикл
def main_game():
    global money, hunger, poop_count, friendship, poop_timer

    running = True

    while running:
        screen.fill(WHITE)

        # Отображение изображения питомца
        pet_image = pygame.image.load(selected_pet_image)  # Загружаем изображение из переменной
        pet_rect = pet_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
        screen.blit(pet_image, pet_rect)

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
                save_state()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    show_clicker()
                elif event.key == pygame.K_2:
                    if money >= 10:
                        money -= 10
                        hunger += 1
                elif event.key == pygame.K_3:
                    if poop_count > 0:
                        poop_count -= 1
                elif event.key == pygame.K_4:
                    friendship += 1
                elif event.key == pygame.K_5:
                    save_state()
                elif event.key == pygame.K_DELETE:
                    save_state()
                    pygame.quit()
                    sys.exit()

        # Рандомное увеличение испражнений
        if time.time() - poop_timer > random.randint(5, 15):
            poop_count += 1
            poop_timer = time.time()

        # Проверка на смерть
        if poop_count >= 50:
            pet_died()
            running = False

        clock.tick(30)

# Кликерный режим
def show_clicker():
    global money
    in_clicker = True

    while in_clicker:
        screen.fill(WHITE)
        draw_text("Нажмите на монетку для заработка!", 180, 100)
        draw_text("Вернуться назад (ESC)", 50, 350)

        coin_rect = pygame.image.load("coin.png").get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pygame.image.load("coin.png"), coin_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    in_clicker = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if coin_rect.collidepoint(pygame.mouse.get_pos()):
                    money += 10

        clock.tick(30)

# Запуск программы
save_file = select_save_file()
if save_file:
    load_state(save_file)
else:
    choose_pet()
    input_pet_name()

main_game()
