import pygame
from network import Network
import cv2
import pickle
pygame.font.init()

pygame.font.init()

# the height and width of the game window
width = 700
height = 700

# creating a window
win = pygame.display.set_mode((width, height))
#calling the game window Fire Sponge Water Game
pygame.display.set_caption("Fire Sponge Water Game")


# creating a button
class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    # draws the screen
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        # font= comicsans
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    # a method that returns true if the button was clicked and false if it didn't
    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (240, 0, 255), True)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


# button- (name, starting point, ending point, (color))
btns = [Button("Water", 50, 500, (255, 100, 180)), Button("Fire", 250, 500, (255, 100, 180)),
        Button("Sponge", 450, 500, (255, 100, 180))]

# -----------fire image
fireImg = pygame.image.load('Fire.png')
fireX = 250
fireY = 490


def fire():
    win.blit(fireImg, (fireX, fireY))


waterImg = pygame.image.load('water.png')
waterX = 450
waterY = 490


def water():
    win.blit(waterImg, (waterX, waterY))


spongeImg = pygame.image.load('sponge.png')
spongeX = 50
spongeY = 490


def sponge():
    win.blit(spongeImg, (spongeX, spongeY))
# -----------

def main():
    run = True
    # הוספת שעון
    clock = pygame.time.Clock()
    # connecting
    n = Network()
    # getting the player
    player = int(n.getP())
    print("You are player", player)

    while run:
        # הגדרת 60 לשעון
        clock.tick(60)

        try:
            '''
            data= "get"
            targetId= "3"
            msgType="game"
            target="client"

            message= target+ "," +msgType+","+targetId+","+data
            game = n.send(message)

            user="Jasmine"
            password= "1234"
            msgType= "Login"
            target= "server"
            message= target+ "," +msgType+","+user+","+password
            game = n.send(message)
            '''
            # get the game from the server
            game = n.send("get")
        except:
            run = False
            # if I coudn't get the game from the server- if there was no respond
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            # applying a delay of a 0.5 seconds before deciding on a winner
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            # if player0 won or player1 won
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (240, 0, 255))
                #camara on the winner
                cap = cv2.VideoCapture(0)
                print("camara is opening")
                # while True:
                ret, frame = cap.read()

                const = 50
                edge = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                edge = cv2.Laplacian(frame, cv2.CV_16S, ksize=3)
                cv2.imshow("camera", frame)
                key = cv2.waitKey(0)
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    # break
            # if the function winner returns -1, there is no winner
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (240, 0, 255))
            else:
                text = font.render("You Lost...", 1, (240, 0, 255))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                # ending the game
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        # opening screen color
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, (115, 0, 0))
        #images
        fire()
        water()
        sponge()
        #------

        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


# להכניס לפונקציה
while True:
    menu_screen()