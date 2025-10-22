import pygame,resourceManager

class Button:
    def __init__(self,text = None,x=0,y=0,width=100,height=100,fileName=None,colour=(200,200,200),value = None):
        self.width = width
        self.height = height
        self.colour = colour
        self.posx =x
        self.posy  =y
        self.isClicked = False
        self.text = text
        self.value = value
        self.fillSqr = None
        #create an offset for the border of the image
        offset = 0
        if width > height:
            offset = self.height/20
        else:
            offset = self.width/20
        # only add text, if text is specified upon creation
        if self.text != None:
            self.buttonfont = pygame.font.SysFont("Arial",int((self.height-(2*offset))*3/4))
            self.text = self.buttonfont.render(self.text,False,(0,0,0))
        #create the image of the button
        self.image = pygame.surface.Surface((self.width,self.height))
        #self.image.fill((0,0,0))
        # if a file is specified, use that as the cover image, if not make a rect and colour it
        if fileName!=None:
            coverimage = resourceManager.load_image(fileName).convert_alpha()
            coverimage = pygame.transform.scale(coverimage,(self.width-(2*offset),self.height-(2*offset)))
            self.image.blit(coverimage,(offset,offset))
        else:
            self.fillSqr = pygame.rect.Rect(offset,offset,self.width-(2*offset),self.height-(2*offset))
            pygame.draw.rect(self.image,self.colour,self.fillSqr)
        self.isClicked = False
        self.prevMouse = False
    def draw(self,screen):
        if self.text != None:
            self.image.blit(self.text,((0,0)))
        screen.blit(self.image,(self.posx,self.posy))
    def changeColour(self,newColour):
        if self.fillSqr != None:
            pygame.draw.rect(self.image,newColour,self.fillSqr)
    def checkClicked(self, mousepos, mouseclicked):
        mouseposx,mouseposy = mousepos
        if mouseposx > self.posx and mouseposx < (self.posx+self.width) :
            # in x bounds
            if mouseposy > self.posy and mouseposy < (self.posy+self.height):
                # in y bounds 
                #return true when the mouse goes up to only trigger once
                if mouseclicked == True and self.prevMouse == False:
                    # the button has been pressed
                    return True,self.value
                if self.prevMouse!=mouseclicked:
                    self.prevMouse = mouseclicked
        return False,self.value # return false if any condition was not met      