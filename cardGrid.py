#!/usr/bin/python
import pygame, random
import helpers

class Card:
    def __init__(self,main,data):
        self.main = main; self.data = data
        #Data represents shape, number, color, texture
        #Shape - Circle, Triangle, Star
        #Number - 1, 2, 3
	#Texture - Shaded, empty, crossed
        #Color - Red, Yellow, Pink
        self.image = helpers.loadImage(str(self.data[0])+str(self.data[1])+str(self.data[2])+'1')[0]
        if self.data[3] == 2: self.image = helpers.hueShiftImage(self.image,120) #Should be green
        elif self.data[3] == 3: self.image = helpers.hueShiftImage(self.image,240) #Should be blue
        
class CardGrid:
    def __init__(self,main):
        self.main = main
        self.CARD_SIZE_H = self.main.CARD_SIZE_H #Pixels
        self.CARD_SIZE_W = self.main.CARD_SIZE_W #Pixels
        self.drawX, self.drawY = 10, self.CARD_SIZE_H
        self.W = 4
	self.H = 3 #Grid size
        self.size = self.W*self.CARD_SIZE_W, self.H*self.CARD_SIZE_H
        self.mazo=[]
        self.NUM_CARDS = self.H*self.W #se empieza con 12 cartas
	for i in range(1,4):
		for j in range(1,4):
			for k in range(1,4):
				for l in range(1,4):
					self.mazo.append([i,j,k,l])
	self.enjuego = []
        self.resetCards() #Cards are stored as a one-dimensional array, not a grid. Indexed from top to bottom, then left to right.
        self.deselectAll() #Resets self.selectedCards to [None,None,None]
        self.selectedColor = (255,255,0)
        #If user middle-clicks, correct set will be highlighted.
        self.correctSetColor = (100,0,100)
        self.correctSet = None
        self.displayCorrectSet = 0
    	
    def compute(self):
        pass

    def draw(self,surface):
	fondo=pygame.image.load("data/images/fondo3.png"); self.main.screen.blit(fondo,(0,0))
        def highlightLocations(locs,color):
            for i in locs:
                if i is not None:
                    x, y = self.indexToPoint(i)
                    pygame.draw.rect(surface,color,pygame.Rect(x,y,self.CARD_SIZE_W-5,self.CARD_SIZE_H-5))
        #FIRST draw highlights behind selected cards.
        if self.displayCorrectSet ==1 : highlightLocations(self.correctSet,self.correctSetColor)
        highlightLocations(self.selectedCards,self.selectedColor)

        for i in range(len(self.cards)):#self.NUM_CARDS):
		if self.cards[i]!=None:
        		x, y = self.indexToPoint(i)
        		surface.blit(self.cards[i].image,(x,y))

    def resetCards(self):
	self.cards = [None]*self.NUM_CARDS
	for i in range(len(self.enjuego)):
		if self.enjuego != []: self.mazo.append(self.enjuego[i])
	self.enjuego=[]
	for i in range(self.NUM_CARDS): self.putCard(i)

    def deselectAll(self):
        self.selectedCards = [None,None,None]
        self.numSelectedCards = 0

    def putCard(self,whereToPutIt):
        #Puts a new card in that position (and removes it from the deck)
	if len(self.mazo)!=0:
		newCard=random.randint(1,len(self.mazo))-1
		data=self.mazo[newCard]
		self.mazo.remove(data)
		self.cards[whereToPutIt] = Card(self.main, data)
		self.enjuego.append(self.cards[whereToPutIt].data)
	elif len(self.enjuego)==0: 
		self.main.final=1
		self.gameControl.final()

    def indexToPoint(self,i): #Converts a grid index to a point on the drawing surface.
        xi, yi = i/self.H, i%self.H
        return self.drawX + self.CARD_SIZE_W*xi, self.drawY + self.CARD_SIZE_H*yi

    def pointToIndex(self,pos):
        xi = (pos[0] - self.drawX)/self.CARD_SIZE_W
        yi = (pos[1] - self.drawY)/self.CARD_SIZE_H
        if 0 <= xi < self.W and 0 <= yi < self.H:
            return xi*self.H + yi #The position in array self.cards
        else: return None
    
    def getClickL(self,surfPos):
        i = self.pointToIndex(surfPos)
        if i is None: pass #Board was not selected.
        else: self.selectCard(i)

    def getClickR(self,surfPos): self.deselectAll()

    def getClickM(self,surfPos):
        #Show solution.
        self.correctSet = self.findCorrectSet()
	if self.correctSet != (None, None, None):
	        self.displayCorrectSet = 1
	else:
	        self.displayCorrectSet = 2

    def selectCard(self,i): #Puts index i into the list of selected cards, or if that is already selected, deselects it.
        for s in range(self.numSelectedCards):
            if self.selectedCards[s] == i: #Then deselect instead
                del self.selectedCards[s]; self.selectedCards.append(None); self.numSelectedCards -= 1
                return #We are done here.

        #If this is not already selected:
	if self.cards[i]!=None:
	        self.selectedCards[self.numSelectedCards] = i; self.numSelectedCards += 1
        #If you've selected 3, check if this is a set.
        if self.numSelectedCards == 3: self.evaluateSelectedCards()
        
    def evaluateSelectedCards(self):
        if self.isASet(*(self.cards[self.selectedCards[i]] for i in range(3))):
            self.getSet()
            for ci in self.selectedCards: 
		self.enjuego.remove(self.cards[ci].data)
		self.cards[ci] = None
            for ci in self.selectedCards: 
		if len(self.mazo)!=0: self.putCard(ci)
        else: self.main.gameControl.score-=1 #You lose one point.

        self.deselectAll() #Now reset the list of selected cards.
        self.displayCorrectSet = 0 #Because that has (probably) just been evaluated.

    def findCorrectSet(self):
        #Goes through all possibilities until it finds a working set.
        for i1 in range(self.NUM_CARDS):
            for i2 in range(self.NUM_CARDS):
		if self.cards[i2]!= None and self.cards[i1]!= None:
	                if i2 != i1:
	                    for i3 in range(self.NUM_CARDS):
				if self.cards[i3]!= None:
	        	                if i3 != i2 and i3 != i1:
	        	                    if self.isASet(self.cards[i1],self.cards[i2],self.cards[i3]): 
						return (i1,i2,i3)
	return (None,None,None)

    def isASet(self,c1,c2,c3): #Checks whether 3 cards form a set.
        for di in range(4): #Going through each attribute
            if not (c1.data[di] == c2.data[di] == c3.data[di] or \
                (c1.data[di] != c2.data[di] and c1.data[di] != c3.data[di] and c2.data[di] != c3.data[di])):
                return 0 #Some attribute is not right.
        return 1

    def getSet(self):
        self.main.getScore()
