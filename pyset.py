#!/usr/bin/python
import pygame,sys
import cardGrid, gameControl, helpers

class main:
    def __init__(self):
	self.FPS = 20
        self.clock = pygame.time.Clock()
        self.CARD_SIZE_H = 105
        self.CARD_SIZE_W = 75
        [self.W, self.H] = [self.CARD_SIZE_W*3, self.CARD_SIZE_H*4]
	self.size=320,480
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Set, pura joda mental')
	icono=pygame.image.load("data/images/icon.png")
        pygame.display.set_icon(icono)
	self.final=0
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
        for event in pygame.event.get():
	    print pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                self.done = 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: #left
			if 64<pygame.mouse.get_pos()[0]< 150 and 445<pygame.mouse.get_pos()[1]<460:
				print "repartir"			
				correctSet = self.cardGrid.findCorrectSet()
				if correctSet == (None,None,None):
					self.gameControl.score += 1
				else:
					self.gameControl.score -= 1
				if len(self.cardGrid.mazo)==0: 
					self.final=1
					self.gameControl.final()
				else: self.cardGrid.resetCards()	
			elif 170<pygame.mouse.get_pos()[0]< 225 and 445<pygame.mouse.get_pos()[1]<460:
				print "Juego nuevo"
				self.cardGrid = cardGrid.CardGrid(self)
				self.gameControl = gameControl.GameControl(self)
			else:self.cardGrid.getClickL(pygame.mouse.get_pos())			
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
	if self.final==0:	
	        self.cardGrid.compute()
		self.gameControl.compute()

    def draw(self):
        self.screen.fill((255,255,255))
        self.cardGrid.draw(self.screen)
        self.gameControl.draw(self.screen)

    def getScore(self):
        self.gameControl.getScore()

m = main()
m.gameControl.intro(m.screen)
m.go()
