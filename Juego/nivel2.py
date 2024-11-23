import pygame
import sys

# inicializamos pygame
pygame.init()

# mostrar una ventana de 800 x 600
size = (900, 700)
screen = pygame.display.set_mode(size)


# colocamos un titulo de ventana
pygame.display.set_caption("BALL GAME")

# creamos variables
width, height = 900, 700
speed = [1, 1]
white = 255, 255, 255

# se crea un objeto ball a partir de una imagen y se obtiene su rectangulo
ballorg = pygame.image.load("Juego/images/ball.png.png")
ballrectorg = ballorg.get_rect()

# bola original
ball = ballorg
ballrect = ballrectorg

# imagen de cambio ball
ball2 = pygame.image.load("Juego/images/ball2.png.jpg")
ballrect2 = ball2.get_rect()

# se crea un objeto bate a partir de una imagen y se obtiene su rectangulo
bateorg = pygame.image.load("Juego/images/bate3.png")
baterectorg = bateorg.get_rect()

bate = bateorg
baterect = baterectorg

# imagen de cambio bate
bate2 = pygame.image.load("Juego/images/bate4.png")
baterect2 = bate2.get_rect()

# poner en bate en el medio
baterect.move_ip(50, 600)

# variable para almacenar la posición de la pelota
posicion = ballrect.topleft

# creamos una variable para controlar el cambio de la imagen del bate
changing_bate = False

# posición inicial de la bola
ballrect.centerx = width // 2
ballrect.centery = height // 2

# iniciamos el bucle del jugo
run = True
while run:
    # eventos producidos en el juego
    # tiempo de 2 miliseg para que la bola vaya despacio
    pygame.time.delay(2)
    for event in pygame.event.get():
        # para salir de la ventana
        if event.type == pygame.QUIT:
            run = False
    # compruebo si se ha pulsado una tecla
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        baterect = baterect.move(-2, 0)
    if keys[pygame.K_d]:
        baterect = baterect.move(2, 0)
    # dentro del bucle while, comprobamos si se ha presionado la barra espaciadora
    if keys[pygame.K_SPACE]:
        # solo cambiamos la imagen del bate una vez mientras se mantiene presionada la barra espaciadora
        if not changing_bate:
            if bate == bateorg:
                bate = bate2
            else:
                bate = bateorg
            changing_bate = True
    else:
        # si se suelta la barra espaciadora, permitimos que se cambie la imagen del bate de nuevo
        changing_bate = False

    # ver si hay colision
    if baterect.colliderect(ballrect) and baterect.collidepoint(ballrect.center):
        speed[0] = -speed[0]
    # movimiento de pelota
    ballrect = ballrect.move(speed)

    # comprobamos si la pelota llega a los limites de la ventana
    if ballrect.top < 0:
        # almacenar la posición actual de la pelota antes de cambiar la imagen
        posicion = ballrect.topleft
        if ball == ballorg:
            ball = ball2
        else:
            ball = ballorg
        # establecer la posición de la pelota a la posición anterior después de cambiar la imagen
        ballrect = ball.get_rect(topleft=posicion)
        # invertir la dirección de la pelota
        speed[1] = -speed[1]
    elif ballrect.bottom > height:
        speed[1] = -speed[1]
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]

    # pinto el fondo de blanco
    screen.fill(white)
    screen.blit(ball, ballrect)

    # Dibujo el bate
    screen.blit(bate, baterect)

    pygame.display.flip()

pygame.quit()