import pygame

clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((626, 240))
pygame.display.set_caption("Бездна")
icon = pygame.image.load("изображения/icon.png").convert_alpha()  # изображение + иконка игры
pygame.display.set_icon(icon)

bg = pygame.image.load("изображения/обои2.jpg").convert_alpha()

walk_right = [
    pygame.image.load("изображения/право/герои1.png").convert_alpha(),
    pygame.image.load("изображения/право/герои2.png").convert_alpha(),
    pygame.image.load("изображения/право/герои3.png").convert_alpha(),
    pygame.image.load("изображения/право/герои4.png").convert_alpha()
]

walk_left = [
    pygame.image.load("изображения/лево/герои1.png").convert_alpha(),
    pygame.image.load("изображения/лево/герои2.png").convert_alpha(),
    pygame.image.load("изображения/лево/герои3.png").convert_alpha(),
    pygame.image.load("изображения/лево/герои4.png").convert_alpha()
]
# конвентировать в формат pygame convert()


monster = pygame.image.load("изображения/monster.png").convert_alpha()
monster_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 5
player_x = 250
player_y = 150

is_jump = False  # переменная для прыжка
jump_count = 9

bg_song = pygame.mixer.Sound("song/od.mp3")  # подключение звука
bg_song.play()

monster_time = pygame.USEREVENT + 1
pygame.time.set_timer(monster_time, 4500)

label = pygame.font.Font("text/Sixtyfour-Regular.ttf", 35)
lose_label = label.render("Gameover", False, (0, 0, 0))
restart_label = label.render("restart", False, (0, 0, 0))
restart_label_rect = restart_label.get_rect(topleft=(188, 180))

bullets_left = 5
bullet = pygame.image.load("изображения/bullet.png").convert_alpha()
bullets = []

gameplay = True

running = True
while running:

    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 626, 0))  # второй задний фон

    if gameplay:

        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))  # невидемый квадрат для персонажа
        if monster_list_in_game:
            for (i, el) in enumerate(monster_list_in_game):  # enumerate получает индекс этого элемента
                screen.blit(monster, el)  # код для прикосновение с монстром выводить lose
                el.x -= 10

                if el.x < -10:
                    monster_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    # при соприкосновении с монстром выводиться you lose
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))
        # та кнопка которую нажимает пользователь для предвижения вправо влево
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 200:
            player_x += player_speed

        # программа для прыжка
        if not is_jump:
            if keys[pygame.K_SPACE]:  # если нажали пробел
                is_jump = True
        else:
            if jump_count >= -9:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2  # более сглаженный прыжок, летит наверх
                else:
                    player_y += (jump_count ** 2) / 2  # летит вниз
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 9

        if player_anim_count == 3:
            player_anim_count = 0  # выводим каждый элемент и задаём условие если картинки заканчиваются,
            # то обнуляем ,если нет то продолжаем прибавлять
        else:
            player_anim_count += 1

        bg_x -= 2
        if bg_x == -626:  # движение экрана
            bg_x = 0

        if bullets:
            for (i, el) in enumerate(bullets):  # рисуем под каждый элемент кртинку со снарядом + передвижение по оси x
                screen.blit(bullet, [el.x, el.y])
                el.x += 4

                if el.x > 640:  # мы выпустили потрон перебираем всех монстров, если столкнулся с ним то мы удаляем
                    bullets.pop(i)  # и монстра и потрон
                if monster_list_in_game:
                    for (index, monster_el) in enumerate(monster_list_in_game):
                        if el.colliderect(monster_el):
                            monster_list_in_game.pop(index)
                            bullets.pop(i)


    else:
        screen.fill((102, 0, 0))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            # соприкосновекин с координатами мышки
            gameplay = True
            player_x = 250
            monster_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # кнопка для правильного закрытия
            running = False
            pygame.quit()
        if event.type == monster_time:  # когда сробатывает таймер добовляется элемент
            monster_list_in_game.append(monster.get_rect(topleft=(628, 150)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_q and bullets_left > 0:
            # один раз при нажатии q и не больше 6 потронов
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 22)))  # event обращение к событию
            bullets_left -= 1

    clock.tick(7)
