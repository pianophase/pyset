#!/usr/bin/python
import pygame,sys
import cardGrid, gameControl, helpers
from pygame.locals import * 
pygame.init() 

class Main:
    def __init__(self):
	
        self.FPS = 20
        self.clock = pygame.time.Clock()
        self.CARD_SIZE = 120
        [self.W, self.H] = self.size = [self.CARD_SIZE*3, self.CARD_SIZE*4]
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Set, pura joda mental')
        
        self.cardGrid = cardGrid.CardGrid(self)
        self.gameControl = gameControl.GameControl(self)        

    def go(self):
        self.done = 0

        while not self.done:
            self.getInput()
            self.compute()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        
    def getInput(self):
#        '''CONTROLS
#        Left click: select/deselect
#        Right click: deselect all
#        '''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left
                    self.cardGrid.getClickL(pygame.mouse.get_pos())
                elif event.button == 2 or event.button == 4 or event.button == 5: #middle button, scrolling or pressing.
                    self.cardGrid.getClickM(pygame.mouse.get_pos())
                elif event.button == 3: #right
                    self.cardGrid.getClickR(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    self.cardGrid.getClickM(pygame.mouse.get_pos()) #In case user has no middle button.
                elif event.key == pygame.K_p:
                    self.pause() #IMPLEMENT!

    def pause(self):
        pass
    
    def compute(self):
        self.cardGrid.compute(); self.gameControl.compute()

    def draw(self):
        self.screen.fill((255,255,255))
        self.gameControl.draw(self.screen)
        self.cardGrid.draw(self.screen)

    def getScore(self):
        self.gameControl.getScore()


m = Main()
m.go()
