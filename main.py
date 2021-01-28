import pygame
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

font = pygame.font.SysFont("Constantia", 30)

#fondo color
bg = (234, 218, 184)
#texto color
text_col = (78, 81, 139)
#barrita color
paddle_col = (142, 135, 123)
#barrita color linea
paddle_outline = (100, 100, 100)

#colores para los bloques
block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)



#define las variables del juego
cols = 6
rows = 6

live_ball = False
game_over = 0

#funcion para el texto inicial
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

class Wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        #definir una lista de individual block
        block_individual = []
        for row in range(rows):
            #reset block lista
            block_row = []
            #iterar cada columna en el registro 
            for col in range(cols):
                #generate x and y position for each block
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)

                #asignar fortaleza al block 
                if row<2:
                    strength = 3
                elif row<4:
                    strength = 2
                elif row<6:
                    strength = 1

                #crear una lista
                block_individual = [rect, strength]
                #agregar una lista de block horizontalmente
                block_row.append(block_individual)

            #agregar la lista completa de blocks
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #asignar un bloque de color de acuerdo a su fortaleza
                if block[1] == 3:
                    block_color = block_blue
                elif block[1] == 2:
                    block_color = block_green
                elif block[1] == 1:
                    block_color = block_red

                pygame.draw.rect(screen, block_color, block[0])
                pygame.draw.rect(screen, bg, block[0], 2)

class Paddle():
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.height = 20
        self.width = int(screen_width/cols)
        self.x = int((screen_width/2) - self.width/2)
        self.y = screen_height - (self.height*2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left>0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right<screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

class GameBall():
    def __init__(self, x, y):
        self.reset(x, y)
    
    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad), self.ball_rad)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad*2, self.ball_rad*2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0

    def move(self):

        collision_thresh = 5

        #colision con bloques
        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    #colision parte de arriba
                    if abs(self.rect.bottom-item[0].top) < collision_thresh and self.speed_y>0:
                        self.speed_y *= -1
                    #colision parte de abajo
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y<0:
                        self.speed_y *= -1
                    #colision parte de izquierda
                    if abs(self.rect.right-item[0].left) < collision_thresh and self.speed_x>0:
                        self.speed_x *= -1
                    #colision parte de derecha
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x<0:
                        self.speed_x *= -1
                    #reduce fortaleza de bloques
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)
                #checar si el bloque aun existe
                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                #incrementamos el item_count
                item_count+=1
            #incrementamos el row_count
            row_count += 1
        #despues de iterar todos los boques chechar si la pared fue destruida
        if wall_destroyed==1:
            self.game_over = 1

        #colision con paredes
        if self.rect.left<0 or self.rect.right>screen_width:
            self.speed_x *= -1
        #colision con suelo y techo
        if self.rect.top<0:
            self.speed_y *= -1
        if self.rect.bottom>screen_height:
            self.game_over = -1

        #colision con player_paddle
        if self.rect.colliderect(player_paddle):
            #colision parte de arriba
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y>0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x>self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x<-self.speed_max:
                    self.speed_x = self.speed_max
            else:
                self.speed_x *= -1 


        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

clock = pygame.time.Clock()
fps = 60

#creamos paredes
wall = Wall()
wall.create_wall()

player_paddle = Paddle()

ball = GameBall(player_paddle.x + (player_paddle.width//2), player_paddle.y - (player_paddle.height))

run = True
while run:

    clock.tick(fps)

    # pinta el fondo
    screen.fill(bg)

    # pinta los bloques
    wall.draw_wall()

    #pinta al jugador
    player_paddle.draw()    

    #pinta a la bolita
    ball.draw()    

    if live_ball:
        player_paddle.move()
        game_over = ball.move()

        if game_over!=0:
            live_ball = False
            ball.reset(player_paddle.x+(player_paddle.width//2), player_paddle.y-player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    #mostramos player instruciones
    if not live_ball:
        if game_over==0:
            draw_text("Space para comenzar", font, text_col, 150, screen_height//2+100)
        elif game_over==1:
            draw_text("Tu ganaste !!!", font, text_col, 200, screen_height//2+50)
        elif game_over==-1:
            draw_text("Haz perdido", font, text_col, 200, screen_height//2+50)
            draw_text("Space para comenzar", font, text_col, 150, screen_height//2+100)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == K_SPACE and live_ball==False:
                live_ball = True

    pygame.display.update()

pygame.quit()