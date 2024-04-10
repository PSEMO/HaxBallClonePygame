import pygame
import random
import math
from sys import exit

framerate = 150
width = 1150
height = 800

pygame.init()

clock = pygame.time.Clock()

#region image loading
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ball game")


bg = pygame.image.load('bg.png')
bg_rect = bg.get_rect()
bg_rect.center = (width / 2, height / 2)

icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)
#endregion
#region functions
def degree_to_position(degree):
    """ Convert degree to radian """
    radian = degree * math.pi / 180
    # Calculate x and y coordinates
    x = math.cos (radian)
    y = math.sin (radian)
    # Return coordinates as a tuple
    return (x, y)
def Similarity(n1, n2):
    """ Calculates a similarity score between 2 numbers """
    if n1 + n2 == 0:
        return 1
    else:
        return 1 - abs(n1 - n2) / (n1 + n2)
def draw_text(surface, text, size, color, x, y, relative):
    font = pygame.font.Font(pygame.font.get_default_font(), size)
    text_surf = font.render(str(text), True, color)
    text_rect = text_surf.get_rect()

    if(relative == 'center'):
        text_rect.center = (x, y)
    
    surface.blit(text_surf, text_rect)
def disBetweenPoints(P1, P2):
    dis = (P1[1] - P2[1])**2 + (P1[0] - P2[0])**2
    return dis
def addInRange(val, add, minval, maxval):
    newval = val + add
    
    #(new value, was in bounds)
    if newval < minval: return (minval, False)
    if newval > maxval: return (maxval, False)
    return (newval, True)
#endregion
#region classes
class Vector2:
    x = 0
    y = 0
class Character:
    def __init__(self, startPosX, startPosY, color):
        self.defaultPos = Vector2()
        self.defaultPos.x = startPosX
        self.defaultPos.y = startPosY

        self.pos = Vector2()
        self.pos.x = startPosX
        self.pos.y = startPosY
        
        self.vel = Vector2()
        self.maxVal = 200
        self.acc = 250
        self.size = 25
        self.color = color

    def VelocityUpdate(self, isX: bool, Direction):
        velocity = 0
        if isX: velocity = self.vel.x
        else: velocity = self.vel.y
        
        if(Direction != 0):
            velocity += self.acc * dt * Direction
            if(velocity > self.maxVal):
                velocity = self.maxVal
            if(velocity < -self.maxVal):
                velocity = -self.maxVal
        else:
            if velocity > 0:
                velocity -= self.acc * dt
                if(velocity < 0): velocity = 0
            elif velocity < 0:
                velocity += self.acc * dt
                if(velocity > 0): velocity = 0
        
        if isX: self.vel.x = velocity
        else: self.vel.y = velocity

    def Update(self, dt, up: bool, left: bool, down: bool, right: bool):
        
        horizontal = right - left
        #because up is negative in this engine but I don't like that
        vertical = -1 * (up - down)

        self.VelocityUpdate(True, horizontal)
        self.VelocityUpdate(False, vertical)

        _X = addInRange(self.pos.x, self.vel.x * dt, 50, width - 50)
        if(_X[1] == False): self.vel.x = 0
        self.pos.x = _X[0]
        _Y = addInRange(self.pos.y, self.vel.y * dt, 50, width - 50)
        if(_Y[1] == False): self.vel.y = 0
        self.pos.y = _Y[0]

        pygame.draw.circle(screen, self.color, (self.pos.x, self.pos.y), self.size, 0)
        pygame.draw.circle(screen, (0, 0, 0), (self.pos.x, self.pos.y), self.size, 3)

    def Reset(self):
        self.pos.x = self.defaultPos.x
        self.pos.y = self.defaultPos.y
        self.vel.x = 0
        self.vel.y = 0
#endregion

GameState = 0
MouseHeldDown = False

WHeldDown = False
AHeldDown = False
SHeldDown = False
DHeldDown = False

UpHeldDown = False
LeftHeldDown = False
DownHeldDown = False
RightHeldDown = False

player1 = Character(200, height / 2, (255, 0, 0))
player2 = Character(width - 200, height / 2, (0, 0, 255))

#Update()
while 1:

    #count the time frame took and assign it to dt
    _dt = clock.tick(framerate)
    dt = _dt / 1000

    #resets screen
    screen.fill((255, 0, 0))

    #region detect events including inputs
    MousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            MouseHeldDown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            MouseHeldDown = False
        else: #this is awful fix that
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    WHeldDown = True
                if event.key == pygame.K_a:
                    AHeldDown = True
                if event.key == pygame.K_s:
                    SHeldDown = True
                if event.key == pygame.K_d:
                    DHeldDown = True
                if event.key == pygame.K_UP:
                    UpHeldDown = True
                if event.key == pygame.K_LEFT:
                    LeftHeldDown = True
                if event.key == pygame.K_DOWN:
                    DownHeldDown = True
                if event.key == pygame.K_RIGHT:
                    RightHeldDown = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    WHeldDown = False
                if event.key == pygame.K_a:
                    AHeldDown = False
                if event.key == pygame.K_s:
                    SHeldDown = False
                if event.key == pygame.K_d:
                    DHeldDown = False
                if event.key == pygame.K_UP:
                    UpHeldDown = False
                if event.key == pygame.K_LEFT:
                    LeftHeldDown = False
                if event.key == pygame.K_DOWN:
                    DownHeldDown = False
                if event.key == pygame.K_RIGHT:
                    RightHeldDown = False

                
    #endregion
    #region game states
    if GameState == 0:
        screen.fill((0, 0, 0))

        draw_text(screen, "Press enter key to start",
                  40, (255, 255, 255), width / 2, height / 2, "center")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                GameState = 1

    elif GameState == 1:
        screen.blit(bg, bg_rect)

        player1.Update(dt,
            WHeldDown, AHeldDown, SHeldDown, DHeldDown)
        player2.Update(dt,
            UpHeldDown, LeftHeldDown, DownHeldDown, RightHeldDown)

    elif GameState == 2:
        screen.fill((0, 0, 0))

        draw_text(screen, "Press enter key to restart",
                  40, (255, 255, 255), width / 2, height / 2, "center")
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                GameState = 1
                player1.Reset()
                player2.Reset()
    #endregion
    
    pygame.display.flip()