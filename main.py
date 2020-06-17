import pygame
import os
import time
import random
pygame.font.init()

WIDTH, HEIGHT = 400, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cars")

#loading images
BLUE_CAR =  pygame.transform.scale(pygame.image.load(os.path.join("assets","blue.png")),(65,120))
GREEN_CAR = pygame.transform.scale(pygame.image.load(os.path.join("assets","green.png")),(65,120))
PURPLE_CAR =pygame.transform.scale(pygame.image.load(os.path.join("assets","purple.png")),(65,120))

ROAD = pygame.transform.scale(pygame.image.load(os.path.join("assets","road1.png")),(WIDTH,HEIGHT))

#Player images
RED_CAR = pygame.transform.scale(pygame.image.load(os.path.join("assets","red.png")),(60,110))


#general Class for Cars
class General:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.car_image = None

    def draw(self, window):
        window.blit(self.car_image, (self.x,self.y))

    def get_width(self):
        return self.car_image.get_width()

    def get_height(self):
        return self.car_image.get_height()


#specific car
class Player(General):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.car_image = RED_CAR
        self.mask = pygame.mask.from_surface(self.car_image)

class Enemy(General):
    COLOR_MAP = {
                "blue":(BLUE_CAR),
                "green":(GREEN_CAR),
                "purple":(PURPLE_CAR)
                }

    def __init__(self,x,y,color):
        super().__init__(x,y)
        self.car_image = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.car_image)

    def move(self, velocity):
        self.y += velocity

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x, offset_y)) != None
   

#main function
def main():

    run = True
    FPS = 60
    level = 0
    score = 0
    main_font = pygame.font.SysFont("comicsans",40)
    lost_font = pygame.font.SysFont("comicsans",30)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    car_velocity = 3

    player_car = Player(70, 250)

    lost = False
    lost_count = 0
    check = 0

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(ROAD,(0,0))
        # drawing text
        level_label = main_font.render(f"Level: {level}", 1, (0, 255, 0))
        score_label = main_font.render(f"Score: {score}", 1, (0, 255, 0))

        WIN.blit(level_label,(50,10))
        WIN.blit(score_label, (WIDTH - score_label.get_width() - 50,10))

        for enemy in enemies:
            enemy.draw(WIN)

        player_car.draw(WIN)

        if lost:
            y_position = 200
            lost_label = lost_font.render("Game Over!", 1, (255,0,0))
            lost_label1 = lost_font.render(f"Your Score: {score}", 1, (0,255,0))
            WIN.blit(lost_label, ((WIDTH/2 - lost_label.get_width()/2), y_position))
            WIN.blit(lost_label1, ((WIDTH/2 - lost_label.get_width()/2), y_position + 40))

        
        pygame.display.update()

    while run:
        clock.tick(FPS)

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy_car = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500,-100), random.choice(["blue","green","purple"]))
                enemies.append(enemy_car)

        if check == 1:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 4:
                run = False
            else:
                redraw_window()
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_car.x > 40:
            player_car.x -= car_velocity
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_car.x < (WIDTH - player_car.get_width() - 40):
            player_car.x += car_velocity
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player_car.y > 0:
            player_car.y -= car_velocity
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player_car.y < (HEIGHT - player_car.get_height()): 
            player_car.y += car_velocity

        for enemy_car in enemies[:]:
            enemy_car.move(enemy_vel)

            if enemy_car.y + enemy_car.get_height() > HEIGHT:
                score += 1
                enemies.remove(enemy_car)
           
            if collide(enemy_car, player_car):
                check = 1
                
        redraw_window()
        

def main_menu():
    menu_font = pygame.font.SysFont("comicsans",40)
    car_font = pygame.font.SysFont("comicsans",90)
    run = True
    while run:
        player_car = Player(0,0)
        y_position = 100
        WIN.blit(ROAD,(0,0))

        car_label0 = car_font.render("CA", 1, (0,255,0))
        WIN.blit(car_label0, (WIDTH/2 - 95, y_position))
        car_label1 = car_font.render("RS", 1, (0,255,0))
        WIN.blit(car_label1, (WIDTH/2 -45 + 50 , y_position))
        
        WIN.blit(RED_CAR, (WIDTH/4 - player_car.get_width()/2 ,y_position + 150))
        WIN.blit(RED_CAR, (WIDTH*0.75 - player_car.get_width()/2 ,y_position + 150))
        menu_label = menu_font.render("Press Space to play", 1, (0,255,0))
        WIN.blit(menu_label, ((WIDTH/2 - menu_label.get_width()/2), y_position + 350))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_SPACE]):
            main()
    pygame.quit()

main_menu()
