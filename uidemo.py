import pygame
from pygame.locals import *

import pitouch


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 320, 240
        self._clickables = []
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self._default_fontpath = pygame.font.match_font("dejavusansmono")

        self._display_surf.fill( pitouch.colors.BLACK )

        btn = pitouch.button.Button(rect=(10, 200, 300, 30), text="Quit", fontpath=self._default_fontpath, fontsize=12)
        btn.subscribe(quit)
        self._clickables.append(btn)
        btn.draw()

        title = pitouch.text.Text(content="Hello world!", fontpath=self._default_fontpath, alignment="c", bold=True)
        title.draw()

        bodytxt = """Oh freddled gruntbuggly,
Thy micturations are to me
As plurdled gabbleblotchits on a lurgid bee.
Groop, I implore thee, my foonting turlingdromes,
And hooptiously drangle me with crinkly bindlewurdles,
Or I will rend thee in the gobberwarts
With my blurglecruncheon, see if I don't!
"""
        body = pitouch.text.Text(content=bodytxt, y=23, fontpath=self._default_fontpath, fontsize=10, alignment="l")
        body.draw()

 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                for obj in self._clickables:
                    obj.mouseDown(event.pos)
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                for obj in self._clickables:
                    obj.mouseUp(event.pos)


    def on_loop(self):
        pass

    def on_render(self):
        pygame.display.update()
        

    def on_cleanup(self):
        pygame.quit()

    def quit(self, obj):
        self._running = False
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()