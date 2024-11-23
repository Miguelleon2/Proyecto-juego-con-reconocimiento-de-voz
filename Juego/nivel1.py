import pygame
import sys

# initialize pygame
pygame.init()

# show a window of 800 x 600
size = (900, 700)
screen = pygame.display.set_mode(size)  # set window caption
pygame.display.set_caption("BALL GAME")

# create variables
width, height = 900, 700
speed = [1, 1]
white, black = 255, 0
font = pygame.font.Font('freesansbold.ttf', 32)

# create a ball object from an image and get its rectangle
ballorg = pygame.image.load("Juego/images/ball.png.png")
ballrectorg = ballorg.get_rect()  # original ball
ball = ballorg
ballrect = ballrectorg  # ball change image
ball2 = pygame.image.load("Juego/images/ball2.png.jpg")
ballrect2 = ball2.get_rect()

# create a bat object from an image and get its rectangle
bateorg = pygame.image.load("Juego/images/Bate1.png")
baterectorg = bateorg.get_rect()
bate = bateorg
baterect = baterectorg

# bat change image
bate2 = pygame.image.load("Juego/images/bate2.png")
baterect2 = bate2.get_rect()

# place bat in the middle
baterect.move_ip(800, 260)

# variable to store ball position
posicion = ballrect.topleft

# create a variable to control the bat image change
changing_bate = False

# posición inicial de la bola
ballrect.left = 0  # Establece el borde izquierdo de la bola en el lado más izquierdo de la pantalla
ballrect.centery = height // 2

# Contador de toques de pelota en la barra
contador_toques = 0

# set game over window and reset button dimensions
game_over_rect = None

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
reset_button_rect = pygame.Rect(width//2-BUTTON_WIDTH//2, height//2-BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)


ballC="naranja"
bateC="naranja"

# main game loop
run = True
while run:
    # events produced during the game
    # time of 2 milliseconds to make ball move slowly
    pygame.time.delay(5)

    for event in pygame.event.get():
        # to exit the game window
        if event.type == pygame.QUIT:
            run = False

    # check if a key has been pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        baterect = baterect.move(0, -4)
    if keys[pygame.K_s]:
        baterect = baterect.move(0, 4)
    if keys[pygame.K_a]:
        baterect = baterect.move(-4, 0)
    if keys[pygame.K_d]:
        baterect = baterect.move(4, 0)
    # check if the space bar has been pressed
    if keys[pygame.K_SPACE]:       # change bat image only once while the space bar is pressed
        if not changing_bate:
            if bate == bateorg:
                bate = bate2
                bateC= "verde"
                print (bateC )
            else:
                bate = bateorg
                bateC= "naranja"
                print (bateC)
            changing_bate = True
            
            #print (ballC+"bate naranja")
    else:
        # allow bat image change again if space bar is released
        changing_bate = False

    # check for collision
    if baterect.colliderect(ballrect) and baterect.collidepoint(ballrect.center):
        speed[0] = -speed[0]
        contador_toques += 1

        if (bateC == "naranja" and ballC == "naranja") or (bateC == "verde" and ballC == "verde"):
            pass
        else:
            if game_over_rect is None:
                game_over_rect = pygame.Rect(0, 0, width, height)
                reset_button_rect = pygame.Rect(width//2-BUTTON_WIDTH//2, height//2-BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)

            # fill screen with black, show game over message and reset button
            screen.fill((black, black, black))
            text_surface = font.render('GAME OVER', True, (white, white, white))
            text_rect = text_surface.get_rect(
            center=(width//2, height//2-BUTTON_HEIGHT))
            screen.blit(text_surface, text_rect)
            pygame.draw.rect(screen, white, reset_button_rect)
            reset_button_text = font.render('RESET', True, (black, black, black))
            reset_button_text_rect = reset_button_text.get_rect(
            center=reset_button_rect.center)
            screen.blit(reset_button_text, reset_button_text_rect)
            pygame.display.flip()

            # wait for reset button to be pressed
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        if reset_button_rect.collidepoint(mouse_x, mouse_y):
                            ballrect.left = 0  # Set the left edge of the ball to the left side of the screen
                            ballrect.centery = height // 2
                            speed = [1, 1]
                            game_over_rect = None
                            contador_toques = 0  # Reinicia el contador de toques
                if game_over_rect is None:
                    break

    # ball movement
    ballrect = ballrect.move(speed)
    # check if ball reaches limits of window
    if ballrect.left < 0:
        posicion = ballrect.topleft
        if ball == ballorg:
            ball = ball2
            ballC = "verde"
            print (ballC + "ball "" verde")
        else:
            ball = ballorg
            ballC = "naranja"
            print (ballC+"ball "" naranja")
        ballrect = ball.get_rect(topleft=posicion)
        
        
        speed[0] = -speed[0]
    elif ballrect.right > width:
        # if ball hits right side of canvas, show game over window and reset button
        if game_over_rect is None:
            game_over_rect = pygame.Rect(0, 0, width, height)
            reset_button_rect = pygame.Rect(width//2-BUTTON_WIDTH//2, height//2-BUTTON_HEIGHT//2, BUTTON_WIDTH, BUTTON_HEIGHT)

        # fill screen with black, show game over message and reset button
        screen.fill((black, black, black))
        text_surface = font.render('GAME OVER', True, (white, white, white))
        text_rect = text_surface.get_rect(
        center=(width//2, height//2-BUTTON_HEIGHT))
        screen.blit(text_surface, text_rect)
        pygame.draw.rect(screen, white, reset_button_rect)
        reset_button_text = font.render('RESET', True, (black, black, black))
        reset_button_text_rect = reset_button_text.get_rect(
        center=reset_button_rect.center)
        screen.blit(reset_button_text, reset_button_text_rect)
        pygame.display.flip()

        # wait for reset button to be pressed
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if reset_button_rect.collidepoint(mouse_x, mouse_y):
                        ballrect.left = 0  # Set the left edge of the ball to the left side of the screen
                        ballrect.centery = height // 2
                        speed = [1, 1]
                        game_over_rect = None
                        contador_toques = 0  # Reinicia el contador de toques
            if game_over_rect is None:
                break

    # if reset button has not been pressed, keep showing game canvas
    if game_over_rect is None:
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]
    

        screen.fill((255, 255, 255))
        screen.blit(ball, ballrect)

        screen.blit(bate, baterect)
        
        # display the number of hits on the screen
        hits_text = font.render(f"Hits: {contador_toques}", True, (0, 0, 0))
        screen.blit(hits_text, (10, 10))

        pygame.display.flip()  
    # Verificar si se ha ganado el juego
    if contador_toques >= 5:
        ganaste_texto = font.render("¡Ganaste!", True, (255, 0, 0))
        ganaste_rect = ganaste_texto.get_rect(center=(width // 2, height // 2))
        screen.blit(ganaste_texto, ganaste_rect)
        pygame.display.flip()
        pygame.time.delay(2000)  # Mostrar el mensaje durante 2 segundos
        run = False     
pygame.quit()
