#!/usr/bin/python
import os, pygame

def loadImage(name, colorkey=None):
    #Loads any PNG, automatically formatting for transparancy/colorkey and converting image to fastest format
    fullname = os.path.join('data', 'images', name)
    if colorkey is None: #Treat it as an image with transparency
        image = pygame.image.load(fullname).convert_alpha()
    else:
        image = pygame.image.load(fullname).convert()
        if colorkey == -1: colorkey = image.get_at((0,0))
        image = image.convert()
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()

def hueShiftImage(img,shift):
    new = pygame.Surface(img.get_size()).convert_alpha()
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            h, s, v, a = img.get_at((x,y)).hsva
            if s > 100: s = 100 #BUGFIX
            newcol = pygame.Color(0); newcol.hsva = h+shift,s,v,a
            new.set_at((x,y),newcol)
    return new
