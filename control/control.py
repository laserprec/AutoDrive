import pygame
from pygame.locals import *
from motor import Motor
from servo import Servo

SCREEN_WIDTH, SCREEN_HEIGHT = 230, 180
FONT, FONT_SIZE             = 'Comic Sans MS', 30 
BLACK, WHITE                = (0, 0, 0), (250, 250, 250)

LEFT_KEY, UP_KEY, RIGHT_KEY, DOWN_KEY = 276, 273, 275, 274
MARGIN                      = 20
PADDING                     = 5
KEY_REC_LEN                 = 60
KEY_REC_BORDER              = 1

MOTOR_PIN = 13
SERVO_PIN = 19

# Initial Setup
pygame.init()
text = pygame.font.SysFont(FONT, FONT_SIZE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0)

def setup():
    screen.fill(BLACK)
    pygame.display.update()
    return Motor(MOTOR_PIN), Servo(SERVO_PIN)

def printPressedKey(key):
    textSurface = text.render("Pressed {}".format(key), True, WHITE)
    screen.fill(BLACK)
    screen.blit(textSurface, (100, 100))
    pygame.display.flip()

def screenRefresh():
    screen.fill(BLACK)
    pygame.display.flip()

def drawKeyBoard(left, top):
    # left key
    leftKeyRec = (left + MARGIN, top + MARGIN + KEY_REC_LEN + PADDING, KEY_REC_LEN, KEY_REC_LEN)
    pygame.draw.rect(screen, WHITE, leftKeyRec, KEY_REC_BORDER)
    # down key
    downKeyRec = (left + MARGIN + KEY_REC_LEN + PADDING,top + MARGIN + KEY_REC_LEN + PADDING, KEY_REC_LEN, KEY_REC_LEN)
    pygame.draw.rect(screen, WHITE, downKeyRec, KEY_REC_BORDER)
    # up key
    upKeyRec = (left + MARGIN + KEY_REC_LEN + PADDING,top + MARGIN, KEY_REC_LEN, KEY_REC_LEN)
    pygame.draw.rect(screen, WHITE, upKeyRec, KEY_REC_BORDER)
    # right key
    rightKeyRec = (left + MARGIN + 2 * (KEY_REC_LEN + PADDING),top + MARGIN + KEY_REC_LEN + PADDING, KEY_REC_LEN, KEY_REC_LEN)
    pygame.draw.rect(screen, WHITE, rightKeyRec, KEY_REC_BORDER)

    pygame.display.update()
    return (leftKeyRec, rightKeyRec, upKeyRec, downKeyRec)

def lightKeyUp(rec):
    pygame.draw.rect(screen, WHITE, rec)
    pygame.display.update()

def main():
    motor, servo = setup()
    forward = False
    backward = False
    turnLeft = False
    turnRight = False
    while 1:
        (leftKeyRec, rightKeyRec, upKeyRec, downKeyRec) = drawKeyBoard(0,0)
        if forward: 
            lightKeyUp(upKeyRec)
            motor.moveForward()
        if backward: 
            lightKeyUp(downKeyRec)
        if turnLeft:
            servo.left()
        elif turnRight:
            servo.right()
        else:
            servo.neutral()
                
        for event in pygame.event.get():
            screenRefresh()
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                print(event.key, 'pressed')
                # printPressedKey(event.key)
                if event.key == LEFT_KEY:
                    turnLeft = True
                    lightKeyUp(leftKeyRec)
                elif event.key == RIGHT_KEY:
                    turnRight = True
                    lightKeyUp(rightKeyRec)
                elif event.key == UP_KEY:
                    forward = True
                    lightKeyUp(upKeyRec)
                elif event.key == DOWN_KEY:
                    backward = True
                    lightKeyUp(downKeyRec) 
                else:
                    pass
            elif event.type == pygame.KEYUP:
                print(event.key, 'released')
                if event.key == UP_KEY:
                    motor.stop()
                    forward = False
                    screenRefresh()
                    pygame.draw.rect(screen, WHITE, upKeyRec, KEY_REC_BORDER)
                    
                elif event.key == DOWN_KEY:
                    backward = False
                    screenRefresh()
                    pygame.draw.rect(screen, WHITE, downKeyRec, KEY_REC_BORDER)
                
                elif event.key == LEFT_KEY:
                    turnLeft = False
                elif event.key == RIGHT_KEY:
                    turnRight = False

                else:
                    pass
            else:
                pass

if __name__ == '__main__':
    main()