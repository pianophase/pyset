#!/usr/bin/python
import os, pygame

class GameControl:
	def __init__(self,main):
		self.main = main
		self.time = 0.0
		self.score = 0
		self.highScore = 0

		pygame.font.init()
		self.textFontSize = 20
		self.textFont = pygame.font.Font(os.path.join('data','font.ttf'),self.textFontSize)
		self.textY = 10 #Top
		self.numberFontSize =20
		self.numberFont = pygame.font.Font(os.path.join('data','font.ttf'),self.numberFontSize)
		self.bottom = 25 #Where to put it
		self.fontColor = (0,0,0)

        def compute(self):
                self.time += 1.0/self.main.FPS

	def draw(self,surface):
	#time
			timeText = self.textFont.render('Tiempo',1,self.fontColor)
			surface.blit(timeText,timeText.get_rect(left=50,top=self.textY))
			timeNumber = self.numberFont.render(str(int(self.time)),1,self.fontColor)
			surface.blit(timeNumber,timeNumber.get_rect(left=10,bottom=self.bottom))
	#remaining cards
			deckText = self.textFont.render('Cartas restantes',1,self.fontColor)
			surface.blit(deckText,deckText.get_rect(left=50,top=self.textY+25))
			deckNumber = self.numberFont.render(str(int(len(self.main.cardGrid.mazo))),1,self.fontColor)
			surface.blit(deckNumber,deckNumber.get_rect(left=10,bottom=self.bottom+25))
	#score
			scoreText = self.textFont.render('Puntos',1,self.fontColor)
			surface.blit(scoreText,scoreText.get_rect(left=50,top=self.textY+50))
			scoreNumber = self.numberFont.render(str(int(self.score)),1,self.fontColor)
			surface.blit(scoreNumber,scoreNumber.get_rect(left=10,bottom=self.bottom+50))
	#new game
			newText = self.textFont.render('nuevo',1,self.fontColor)
			surface.blit(newText,newText.get_rect(left=160+10,top=25+self.main.H))
	#deal again
			dealText = self.textFont.render('repartir',1,self.fontColor)
			surface.blit(dealText,dealText.get_rect(right=160-10,top=25+self.main.H))
	#/			
#			text = self.textFont.render('',1,self.fontColor)
#			surface.blit(text,text.get_rect(right=160+5,top=25+self.main.H))

	def final(self):
		print "En", self.time, "segundos", "obtuviste", self.score, "puntos"

	def getScore(self):
		self.score += 1

	def intro(self,surface):
		l=200;	h=200;	i=30
		self.textFontSize=40
		done = 0
		rules=0
	        while not done:
			#fondo
			self.fondo=pygame.image.load("data/images/fondo2.png")
			self.main.screen.blit(self.fondo,(0,0))
			#Jugar
			text = self.textFont.render('Jugar',1,self.fontColor)
			surface.blit(text,text.get_rect(left=l,top=h))
			#Reglas
			text = self.textFont.render('Reglas',1,self.fontColor)
			surface.blit(text,text.get_rect(left=l,top=h+i))
			#Acerca
			text = self.textFont.render('Acerca',1,self.fontColor)
			surface.blit(text,text.get_rect(left=l,top=h+2*i))
			#Salir
			#text = self.textFont.render('Salir',1,self.fontColor)
			#surface.blit(text,text.get_rect(left=l,top=h+3*i))

	        	for event in pygame.event.get():
				if event.type == pygame.QUIT:
                			pygame.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1: #left
						if l<pygame.mouse.get_pos()[0]< l+60 and h<pygame.mouse.get_pos()[1]<h+30:
							print "jugar"			
							done=1
						elif l<pygame.mouse.get_pos()[0]< 240 and h+31<pygame.mouse.get_pos()[1]<h+30*2:
							print "reglas"
							self.reglas=pygame.image.load("data/images/reglas.png")
							self.main.screen.blit(self.reglas,(0,0))
							while not rules:
								for event in pygame.event.get():
									if event.type==pygame.MOUSEBUTTONDOWN:	
										if event.button==1:
											rules=1
								pygame.display.flip()
				else: pass #print pygame.mouse.get_pos()
			pygame.display.flip()
