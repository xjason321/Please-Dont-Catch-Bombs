import pygame, random, math
from pygame.locals import *
from PIL import Image

LISTOFBALLS = ["blue", "green", "orange", "red", "yellow", "purple", "bomb", "bomb", "bomb", "bomb"]

def ScaleImages(images, size):
    for name in images:
        im = Image.open('assets/originals/' + name +'.png')
        newsize = size
        im = im.resize(newsize)
        im.save('assets/scaled/' + name + '.png')

# Classes for Game
class Ball():
    def __init__(self):
        """ The constructor of the class """
        self.color = random.choice(LISTOFBALLS)
        self.image = pygame.image.load('assets/scaled/' + self.color + ".png")

        self.x = random.randint(0, 300)
        self.y = -40
        
        self.angle = 90
        self.tick = 0

        self.y_velocity = 0.3
        self.acceleration = .1

        self.x_velocity = random.choice([1, -1]) * random.choice([0.7, 1.3, 1.6])
        self.collidable = True

    def update(self, score):
        # if self.collidable == True:
        #     self.image = pygame.transform.rotate(self.image, self.angle)
        self.tick += .1
        self.y_velocity += self.acceleration

        self.acceleration = 0.1 + (score / 300)

        if self.color == "bomb":
            if (self.tick % 2) > 1:
                self.image = pygame.image.load("assets/scaled/bomb_flash.png")
            else:
                self.image = pygame.image.load("assets/scaled/bomb.png")

        if self.x > 450 or self.x < -60 or self.y > 800:
            self.reset()

        self.y += self.y_velocity
        self.x += self.x_velocity 
        x = int(self.x)
        y = int(self.y)
        self.hitbox = pygame.Rect(x, y, 60, 60)

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(surface, "green" if self.collidable else "red", self.hitbox, width=3, border_radius=10)

    def reset(self):
        self.color = random.choice(LISTOFBALLS)
        self.image = pygame.image.load('assets/scaled/' + self.color + ".png")
        self.x = random.randint(0, 400)
        self.y = -40
        self.angle = 270
        self.y_velocity = 1
        self.x_velocity = random.choice([1, -1]) * random.choice([0.7, 1.3, 1.6])
        self.collidable = True
    
    def animate(self, case, surface):
        self.collidable = False
        if case == "success":
            self.x_velocity *= 3
            self.y_velocity = -2
            # pygame.mixer.Sound('sounds/bing.wav').play()
        if case == "fail":
            for i in range(300):
                pygame.draw.rect(surface, "white", pygame.Rect(0, 0, 1000, 1000))
                pygame.display.update()
                
                pygame.draw.rect(surface, "orange", pygame.Rect(0, 0, 1000, 1000))
                pygame.display.update()

class Platform():
    def __init__(self):
        """ The constructor of the class """
        self.color = random.choice(["blue", "green", "orange", "red", "yellow", "purple"])
        self.image = pygame.image.load("assets/scaled/platform.png")
        self.x = 200
        self.y = 600

    def handle_keys(self, score):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 7 + (score/10) # distance moved in 1 frame, try changing it to 5

        if key[pygame.K_RIGHT] and self.x < 400: # right key
            self.x += dist # move right
        elif key[pygame.K_LEFT] and self.x > -50: # left key
            self.x -= dist # move left

        self.hitbox = pygame.Rect(int(self.x), int(self.y) + 53, 130, 25)

    def draw(self, surface):
        # blit yourself at your current position
        surface.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(surface, "blue", self.hitbox, width=3, border_radius=10)

class ScoreBoard():
    def __init__(self):
        self.font = pygame.font.SysFont("Trebuchet MS", 30)
        self.tick = 0
    
    def update(self, screen, score):
        self.tick += 0.05
        score_text = self.font.render(str(score), True, (255, 255, 255))
        screen.blit(score_text, (20, math.sin(self.tick) * 10 + 70))

# Classes for Menu
class Title():
    def __init__(self):
        self.image = pygame.image.load("assets/scaled/title.png")
        self.tick = 0
    
    def update(self, surface):
        self.tick += 0.05
        surface.blit(self.image, (90, math.sin(self.tick) * 10 + 100))

class Play_Button():
    def __init__(self): 
        self.image = pygame.image.load("assets/scaled/Play Button.png")
        self.rect = self.image.get_rect(center = (222, 382))
        self.buttonclicked = False

    def change_state(self, mousepos, clicked):
        if self.rect.collidepoint(mousepos):
            self.image = pygame.image.load("assets/scaled/Play Button Hovered.png")
            if clicked:
                self.buttonclicked = True
        else:
            self.image = pygame.image.load("assets/scaled/Play Button.png")

    def draw(self, surface):
        surface.blit(self.image, (123, 360))
        # pygame.draw.rect(surface, "green", self.rect, width=3, border_radius=10)

class Settings_Button():
    def __init__(self): 
        self.image = pygame.image.load("assets/scaled/Settings Button.png")
        self.rect = self.image.get_rect(center = (222, 492))
        self.buttonclicked = False

    def change_state(self, mousepos, clicked):
        if self.rect.collidepoint(mousepos):
            self.image = pygame.image.load("assets/scaled/Settings Button Hovered.png")
            if clicked:
                self.buttonclicked = True
        else:
            self.image = pygame.image.load("assets/scaled/Settings Button.png")

    def draw(self, surface):
        surface.blit(self.image, (123, 470))
        # pygame.draw.rect(surface, "green", self.rect, width=3, border_radius=10)

class Menu_Button():
    def __init__(self): 
        self.image = pygame.image.load("assets/scaled/Menu Button.png")
        self.rect = self.image.get_rect(center = (222, 482))
        self.buttonclicked = False

    def change_state(self, mousepos, clicked):
        if self.rect.collidepoint(mousepos):
            self.image = pygame.image.load("assets/scaled/Menu Button Hovered.png")
            if clicked:
                self.buttonclicked = True
        else:
            self.image = pygame.image.load("assets/scaled/Menu Button.png")

    def draw(self, surface):
        surface.blit(self.image, (123, 460))
        # pygame.draw.rect(surface, "green", self.rect, width=3, border_radius=10)

class App():
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((450, 800))
        pygame.display.set_caption('Balls Only, Please')

        self.score = 0
        self.clicked = False
        self.tick = 0

        self.gamestate = "Menu"

        self.clock = pygame.time.Clock()

        ScaleImages(["blue", "green", "orange", "purple", "red", "yellow"], (60, 60))
        ScaleImages(["bomb", "bomb_flash"], (70, 82))
        ScaleImages(["platform"], (130, 130))
        ScaleImages(["title"], (272, 98))
        ScaleImages(["Play Button", "Play Button Hovered", 
                     "Settings Button", "Settings Button Hovered",
                     "Menu Button", "Menu Button Hovered"], (200, 50))
        ScaleImages(["Game Over"], (300, 90))

        pygame.display.set_icon(pygame.image.load('assets/originals/purple.png'))

        self.MainMenu(screen)

    def MainMenu(self, screen):
        ball = Ball()
        ball2 = Ball()
        ball3 = Ball()

        self.score = 0

        title = Title()
        playbutton = Play_Button()
        settingsbutton = Settings_Button()
        
        running = True

        while running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # quit the screen
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                else:
                    self.clicked = False

            screen.fill((29, 40, 34))

            for balls in [ball, ball2, ball3]:
                balls.update(self.score)
                balls.draw(screen)

            # Add Menu Elements
            title.update(screen)

            for button in [playbutton, settingsbutton]:
                button.change_state(pygame.mouse.get_pos(), self.clicked)
                
                if playbutton.buttonclicked:
                    self.score = 0
                    self.gamestate = "Game"
                    self.RunGame(screen)
                    running = False
                if settingsbutton.buttonclicked:
                    self.gamestate = "Settings"
                    self.SettingsMenu(screen)
                    running = False

                button.draw(screen)

            pygame.display.update()

            self.clock.tick(100)

    def RunGame(self, screen):
        pygame.mixer.Sound('sounds/music.mp3').play()

        ball = Ball()
        ball2 = Ball()
        ball3 = Ball()

        player = Platform()
        
        scoreboard = ScoreBoard()

        running = True

        while running:
            # handle every event since the last frame.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.MainMenu(screen)
                    running = False

            player.handle_keys(self.score)

            ball.update(self.score)

            collision = self.checkCollisions(ball, player)

            if collision:
                if collision == "bomb":
                    ball.animate("fail", screen)
                    self.GameOverScreen(screen)
                    running = False
                else:
                    ball.animate("success", screen)
                    self.score += 1

            if self.score > 10:                
                ball2.update(self.score)
                if ball2.hitbox.colliderect(player.hitbox) and ball2.collidable == True:
                    if ball2.color == "bomb":
                        ball2.animate("fail", screen)
                        self.GameOverScreen(screen)
                        running = False
                    else:
                        ball2.animate("success", screen)
                        self.score += 1      

            if self.score > 20:
                ball3.update(self.score)
                
                if ball3.hitbox.colliderect(player.hitbox) and ball3.collidable == True:
                    if ball3.color == "bomb":
                        ball3.animate("fail", screen)
                        self.GameOverScreen(screen)
                        running = False
                    else:
                        ball3.animate("success", screen)
                        self.score += 1      

            screen.fill((29, 40, 34)) 

            player.draw(screen)
            ball.draw(screen)

            if self.score > 10:
                ball2.draw(screen)
            if self.score > 20:
                ball3.draw(screen)

            scoreboard.update(screen, self.score)

            pygame.display.update()

            self.clock.tick(100)

    def SettingsMenu(self, screen):
        running = True

        self.font = pygame.font.SysFont("Trebuchet MS", 20)

        while running:
            # handle every event since the last frame.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # quit the screen
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.gamestate = "Menu"
                        self.MainMenu(screen)
                        running = False  

            screen.fill((29, 50, 34)) 

            esc_text = self.font.render("< Esc", True, (255, 255, 255))
            screen.blit(esc_text, (10, 40))

            LISTOFIMAGES = ["blue", "green", "orange", "red", "yellow", "purple", "bomb", "bomb_flash"]

            for b in range(len(LISTOFIMAGES)):
                image_b = pygame.image.load("assets/scaled/" + LISTOFIMAGES[b] + ".png")
                
                row_b = math.floor(b/4) * 100
                col_b = (b % 4) * 100

                if LISTOFIMAGES[b] == "bomb" or LISTOFIMAGES[b] == "bomb_flash":
                    row_b -= 20
                screen.blit(image_b, (col_b + 40, row_b + 100))

            pygame.display.update()

            self.clock.tick(100)

    def GameOverScreen(self, screen):
        ball = Ball()
        ball2 = Ball()
        ball3 = Ball()

        playbutton = Play_Button()
        menubutton = Menu_Button()
        
        running = True

        while running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit() # quit the screen
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                else:
                    self.clicked = False

            screen.fill((0, 0, 0))

            for balls in [ball, ball2, ball3]:
                balls.update(self.score)
                balls.draw(screen)

            for button in [playbutton, menubutton]:
                button.change_state(pygame.mouse.get_pos(), self.clicked)
                
                if playbutton.buttonclicked:
                    self.score = 0
                    self.gamestate = "Game"
                    self.RunGame(screen)
                    running = False
                if menubutton.buttonclicked:
                    self.MainMenu(screen)
                    running = False

                button.draw(screen)

            screen.blit(pygame.image.load("assets/scaled/Game Over.png"), (70, 100))

            pygame.display.update()

            self.clock.tick(100)

    def checkCollisions(self, ball, player):
        if ball.hitbox.colliderect(player.hitbox) and ball.collidable == True:
            if ball.color == "bomb" or ball.color == "bomb_flash":
                return "bomb"
            else:
                return "success"  

App()
