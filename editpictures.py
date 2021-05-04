17






#the height and width of the game window
width = 700
height = 700

#creating a pygame window (width=700, height=700)
win = pygame.display.set_mode((width, height))
#calling the game window Fire Sponge Water Game
pygame.display.set_caption("Fire Sponge Water Game")













#-----------fire
fireImg = pygame.image.load('Fire.png')
fireX = 250
fireY = 490


def fire() :
    win.blit(fireImg, (fireX, fireY))


waterImg = pygame.image.load('water.png')
waterX = 450
waterY = 490


def water() :
    win.blit(waterImg, (waterX, waterY))


spongeImg = pygame.image.load('sponge.png')
spongeX = 50
spongeY = 490


def sponge() :
    win.blit(spongeImg, (spongeX, spongeY))



fire()
water()
sponge()

#-----------