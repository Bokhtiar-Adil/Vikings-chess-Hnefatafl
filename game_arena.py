import pygame as pg


WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "VIKINGS_CHESS"
GAME_ICON = pg.image.load("images/vh.jpg")

def main():
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(GAME_NAME)
    pg.display.set_icon(GAME_ICON)
    
    game_on = True
    
    while game_on:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
    
    pg.quit()
    
    
if __name__ == "__main__":
    main()

